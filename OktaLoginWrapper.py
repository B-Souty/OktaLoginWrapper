from lxml import html, etree
from base64 import b64decode
from getpass import getpass
import requests
import json
import time


class OktaSession(object):

    def __init__(self, organization):
        self.organization = str(organization).lower()
        self.okta_session = requests.session()
        self.okta_session.headers.update({
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
        })
        self._session_token = None
        self._user_id = None

    def okta_auth(self, username, password):
        url_authn = 'https://{}.okta.com/api/v1/authn'.format(self.organization)
        payload_authn = json.dumps({
            "username": username,
            "password": password,
            "options": {"warnBeforePasswordExpired": True,
                        "multiOptionalFactorEnroll": True},
        })
        response = self.okta_session.post(url_authn, data=payload_authn)

        factors = json.loads(response.text).get('_embedded').get('factors')
        auth_params = {
            'state_token': json.loads(response.text).get('stateToken'),
            'factor_id': [i['id'] for i in factors if i.get('factorType') == 'push'][0]
        }
        return self._okta_verify(auth_params)

    def _okta_verify(self, auth_params):
        url_push = "https://{}.okta.com/api/v1/authn/factors/{}/verify".format(self.organization, auth_params['factor_id'])
        payload_push = json.dumps({"stateToken": auth_params['state_token'],
                                   "factorType": "push",
                                   "provider": "OKTA"})
        response = self.okta_session.post(url_push, data=payload_push)
        push_state = json.loads(response.text).get('status')
        while push_state != 'SUCCESS':
            print("push_state is: ", push_state)
            time.sleep(2)
            response = self.okta_session.post(url_push, data=payload_push)
            push_state = json.loads(response.text).get('status')
            print("slept 2 sec, push_state is now: ", push_state)
            if json.loads(response.text).get('factorResult') == 'REJECTED':
                self.okta_session.close()
                return "You didn't approve the connection, closing the session."
        self._session_token = json.loads(response.text).get('sessionToken')
        self._user_id = json.loads(response.text).get('_embedded').get('user').get('id')
        cookie_brewer_url = 'https://{0}.okta.com/login/sessionCookieRedirect?checkAccountSetupComplete=true&token={1}&redirectUrl=https%3A%2F%2F{0}.okta.com%2Fuser%2Fnotifications'.format(self.organization, self._session_token)
        self.okta_session.get(url=cookie_brewer_url)

    def app_list(self):
        appslist_url = "https://{}.okta.com/api/v1/users/{}/appLinks/".format(self.organization, self._user_id)
        appslist_headers = {
            "Host": "{}.okta.com".format(self.organization),
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,fr;q=0.8,nl;q=0.7",
        }

        return self.okta_session.get(url=appslist_url, headers=appslist_headers).json()

    def connect_to(self, url_app):
        response = self.okta_session.get(url=url_app)
        tree = html.fromstring(response.text)
        saml_response = tree.xpath('//input[@name="SAMLResponse"]')[0].attrib.get('value')
        url_saml = etree.XML(b64decode(saml_response)).get('Destination')
        payload_saml = {
            "SAMLResponse": saml_response,
            "RelayState": "",
        }
        headers_saml = {
            'origin': "https://{}.okta.com".format(self.organization),
            'upgrade-insecure-requests': "1",
            'content-type': "application/x-www-form-urlencoded",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9,fr;q=0.8,nl;q=0.7",
            'cache-control': "no-cache",
        }
        return self.okta_session.post(url=url_saml, data=payload_saml, headers=headers_saml)

    def connect_from_appslist(self):
        app_name = input('app name: ').lower()
        results = [{'name': i.get('label'), 'link': i.get('linkUrl')} for i in self.app_list() if app_name in i.get('label').lower()]
        for ind, app in enumerate(results):
            print("{} - {}".format(ind, app.get('name')))
        choice = int(input('Please select the app to connect to: '))
        app_link = results[choice].get('link')
        return self.connect_to(app_link)


if __name__ == '__main__':
    my_session = OktaSession(input('Please type your organization name (<organization>.okta.com): '))
    my_session.okta_auth(input('Type in your Okta username: '), getpass('Okta password: '))
    my_app = my_session.connect_from_appslist()
    print(my_app.content)
    my_session.okta_session.close()
