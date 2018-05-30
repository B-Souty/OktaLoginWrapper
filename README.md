# Okta Login Wrapper

Helps you connect to resources behind Okta SSO

## Prerequisite

* Python 3
* Python modules
    * Requests
    * lxml
* An Okta account 

## Getting Started

**\~WARNING\~ Currently the script only works if you have "push" enabled as MFA.**

The main goal of this script is to help you login to an application using SSO with Okta, without requiring any API token.

As part of another scripts, it allows you to have an okta_session object from where you can connect to all application assigned to you in Okta.


```
#  Create a session with your okta instance name as well as your credentials.
#  If the credentials are correct, you'll be asked for MFA. (Currently only work with push notification)
my_session = OktaSession(okta_instance)
my_session.okta_auth(okta_username, okta_password)
```

As a non-interactive script:
```
#  get a list of available app along with their url
app_list = my_session.app_list()
#  Find the url of the app you want to login to from app_list then run
my_app = my_session.connect_to(app_url)
```

As an interactive script:
```
#  You can prompt the user to type the name of an app he wants to log into.
#  A list is returned with with corresponding apps and the user has to select which one to login to.
#  If connection is successful, it returns a requests.models.response of the homepage of the app.
#  From there, you can navigate the app using your object my_session.

my_app = my_session.connect_from_appslist()
```
Close the session once you're done.
```
my_session.okta_session.close()
```


It can also be executed but this is mainly a proof of concept as it just print the raw content.

### Installing

Simply make sure you you have the required python modules installed. 

```
pip install -r requirements.txt
```

## Built With

* [Requests](http://docs.python-requests.org/en/master/) - Python HTTP Requests for Humans
* [lxml](http://lxml.de/) - The lxml XML toolkit for Python

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
