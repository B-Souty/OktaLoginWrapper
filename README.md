# Okta Login Wrapper

Provide an easy way for your scripts to access ressources behind an Okta SSO solution, without the need for an API token.

## Prerequisite

* Python 3
* An Okta account 

### Installing

oktaloginwrapper is now available on Pypi. Simply install it with:

```pip install oktaloginwrapper```

## Getting Started

**\~WARNING\~ Currently the script only works if you have "push", "secret question" or "software token" enabled as MFA.**

The main goal of this script is to help you login to an application using SSO with Okta, without requiring any API token.

As part of another scripts, it allows you to have an okta_session object from where you can connect to all application assigned to you in Okta.

Start by importing the module and instantiate an OktaSession object with your Okta instance/organization name.
```Python
from oktaloginwrapper import OktaLoginWrapper as OLW

my_session = OLW.OktaSession(okta_instance) #Where okta_instance is https://<okta_instance>.okta.com
```

Then, depending on the type of multi-factor you want to use, you can do as follow

* **Most Basic use with push notification (default). You have 60 seconds to approve the connection on your phone.**
  ```Python
  >>>  my_session.okta_auth(
  ...    username='<your_username>',
  ...    password='<your_password>',
  ...  )
  
  59 seconds remaining before timeout.
  57 seconds remaining before timeout.
  55 seconds remaining before timeout.
  'You are now logged in.'
  ```
* **Connect using the secret question.**
  * You can provide the answer directly during authentication. this will log you straight in.
    ```Python
    >>>  my_session.okta_auth(
    ...    username='<your_username>',
    ...    password='<your_password>',
    ...    answer='<your_answer>'
    ...  )
    
    'You are now logged in.'
    ```
  * Or using the interactive way by providing the factor_type. You will be prompted to enter the answer.
    ```Python
    >>>  my_session.okta_auth(
    ...    username='<your_username>',
    ...    password='<your_password>',
    ...    factor_type='question'
    ...  )
    
    What was your dream job as a child >? <your_answer>
    'You are now logged in.'
    ```
* **Connect using a software token. (Currently not tested with hardware token)**
  * You can provide the passCode directly during authentication. this will log you straight in.
    ```Python
    >>>  my_session.okta_auth(
    ...    username='<your_username>',
    ...    password='<your_password>',
    ...    passCode='<your_passCode>'
    ...  )
    
    'You are now logged in.'
    ```
  * Or using the interactive way by providing the factor_type. You will be prompted to enter the passCode.
    ```Python
    >>>  my_session.okta_auth(
    ...    username='<your_username>',
    ...    password='<your_password>',
    ...    factor_type='token'
    ...  )
    
    Please type in your OTP: >? <your_passCode>
    'You are now logged in.'
    ```
* **Connect to an app assigned to you.**
  * You need to know the "embedded" link of the app you want to log into and pass it as an argument of connect_to(). 
    ```Python
    my_app = my_session.connect_to(<your_app_url>)
    ```
  Alternatively, you can use the provided method app_list() to retrieve the list of apps assigned to you along with their url and connect from there. 
    ```Python
    >>> my_apps = my_session.app_list()

    >>> my_app = None
    >>> app_name = <your_app_name>
    >>> for app in my_apps:
    ...     if app.get('label') == app_name:
    ...         my_app = my_session.connect_to(app.get('linkUrl'))

    >>> if not my_app:
    ...     print("You do not have {} assigned in Okta.".format(app_name))
    ```
  * You can also use the method connect_from_appslist() to get an interactive way to select you app and connect to it.
  ```Python
  >>> my_app = my_session.connect_from_appslist()
  
  app name: >? Slack
  0 - Slack
  1 - Slack-dev
  Please select the app to connect to: >? 0
  ```

* Then simply close the session when you're done.
  ```Python
  my_session.okta_session.close()
  ```

It can also be executed but this is mainly a proof of concept as it just print the raw content. 
I will probably remove that part at some point in the future.


## Built With

* [Requests](http://docs.python-requests.org/en/master/) - Python HTTP Requests for Humans
* [lxml](http://lxml.de/) - The lxml XML toolkit for Python

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
