# from curl_cffi import requests
# from selectolax.lexbor import LexborHTMLParser
# from requests_toolbelt import MultipartEncoder
# from Login_system.settings import LOGIN_URL
# from Login_system.settings import username,password, login_button
# # from celery import shared_task


# # @shared_task

# def fetch_login_page():
#     session = requests.Session()  # Initialize session
#     session.headers.update({
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
#     })

#     # Attempt to fetch the login page

#     while True:
#         response = session.get(LOGIN_URL,timeout=5)
#         if response.status_code == 200:
#             print("Login page fetched successfully:", response.status_code)
#             break
#         print('retrying failed request...')
#         session.headers.clear()
#         session.cookies.clear()
    
#             # Step 2: Parse hidden fields and update data
#     soup = LexborHTMLParser(response.content)
#     data = {
#         'ctl00$mainContentPlaceHolder$loginUserNameTextBox': username,
#         'ctl00$mainContentPlaceHolder$loginPasswordTextBox': password,
#         'ctl00$mainContentPlaceHolder$loginButton': login_button
#          }
#     data.update({x.attrs['name']: x.attrs['value'] for x in soup.css('input[type="hidden"]')})

#     form = MultipartEncoder(fields=data)
#     print(form)
#     session.headers.update({'Content-Type': form.content_type})
#     r = session.post(LOGIN_URL, data=form.to_string())
#     print("Login attempt response:", r.status_code)
  

        # Process the page if needed
        # e.g., parser = LexborHTMLParser(response.text)
    # else:
    #     print("Failed to fetch the login page. Retrying...")
    #     # Clear headers and cookies before retrying
    #     session.headers.clear()
    #     session.cookies.clear()
    #     response = session.get(LOGIN_URL)
    #     if response.status_code == 200:
    #         print("Login page fetched successfully on retry:", response.status_code)
        
    #     else:
    #         print("Retry failed. Status code:", response.status_code)






# # # Call the function
# # # login_to_site()





## login.py ##

from curl_cffi import requests
from selectolax.lexbor import LexborHTMLParser
from requests_toolbelt import MultipartEncoder
import os
import logging
import ctypes
# from variables import *
from Login_system.settings import *

def login_to_corrlinks():
    """
    Logs into the Corrlinks website and returns a session object.
    Returns:
    - requests.Session or None: A session object if login is successful, None otherwise

    This function sets up a requests session, configures it with necessary headers
    and proxy settings, and attempts to log in to the Corrlinks website. It handles
    retries for failed requests and verifies IP masking. The function returns the
    session object for use in subsequent requests.
    """
    try:
        req = requests.Session()  # Initialize session here
        req.headers.update({
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        })

        if USE_PROXY and PROXY_URL:
            req.proxies = {'http': PROXY_URL, 'https': PROXY_URL}

        req.impersonate = 'chrome'
        req.base_url = BASE_URL


        # Attempt to log in
        while True:
            r = req.get(LOGIN_PAGE)
            if r.status_code == 200:
                print("Login page fetched successfully:", r.status_code)
                break
            print('retrying failed request...')
            req.headers.clear()
            req.cookies.clear()
    
        # Parse hidden fields and update data
        soup = LexborHTMLParser(r.content)
        data = {
            'ctl00$mainContentPlaceHolder$loginUserNameTextBox': username,
            'ctl00$mainContentPlaceHolder$loginPasswordTextBox': password,
            'ctl00$mainContentPlaceHolder$loginButton': login_button,
        }
        data.update({x.attrs['name']: x.attrs['value'] for x in soup.css('input[type="hidden"]')})
        form = MultipartEncoder(fields=data)
        req.headers.update({'Content-Type': form.content_type})
        r = req.post(LOGIN_PAGE, data=form.to_string())
        print("Login attempt response:", r.status_code)

        return req  # Return the session object for further use
    except Exception as e:
        logging.error(f"An error occurred during login: {e}")
        return None  # It might be safer to return None or handle this more gracefully













# # from accounts.utils import get_username_password

# from django.conf import settings

# from curl_cffi import requests
# from selectolax.lexbor import LexborHTMLParser
# from requests_toolbelt import MultipartEncoder

# import logging

# logger = logging.getLogger('login')

# class SessionManager:
#     _session = None

#     @classmethod
#     def get_session(cls):
#         if cls._session is None:
#             cls._session = cls._login_to_corrlinks()
#         return cls._session

#     @classmethod
#     def _login_to_corrlinks(cls):
#         try:
#             user_name =user_name
#             password = password
#             req = requests.Session()
#             req.headers.update({
#                 'User-Agent': settings.LOGIN_REQUEST_HEADER
#             })

#             if settings.USE_PROXY and settings.PROXY_URL:
#                 logger.info(f'Using proxies {settings.PROXY_URL}')
#                 req.proxies = {'http': settings.PROXY_URL, 'https': settings.PROXY_URL}
#             else:
#                 logger.info('Continue Without Proxies.')

#             req.impersonate = 'chrome'
#             req.base_url = settings.BASE_URL

#             # Verify IP masking by checking the external IP
#             http_ip_response = req.get(settings.HTTPBIN_IP_URL_HTTP)
#             logger.info(f'http {http_ip_response.json()["origin"]}')
#             https_ip_response = req.get(settings.HTTPBIN_IP_URL_HTTPS)
#             logger.info(f'https {https_ip_response.json()["origin"]}')

#             # Attempt to log in
#             while True:
#                 r = req.get(settings.LOGIN_PAGE)
#                 if r.status_code == 200:
#                     logger.info(f"Login page fetched successfully: STATUS CODE = {r.status_code}")
#                     break
#                 logger.error("Login Page not fetched. Retrying ........")
#                 req.headers.clear()
#                 req.cookies.clear()

#             # Parse hidden fields and update data
#             soup = LexborHTMLParser(r.content)
#             data = {
#                 settings.LOGIN_EMAIL_FIELD_ID: user_name,
#                 settings.LOGIN_PASSWORD_FIELD_ID: password,
#                 settings.LOGIN_BUTTON_ID: settings.LOGIN_BUTTON_TEXT
#             }
#             data.update({x.attrs['name']: x.attrs['value'] for x in soup.css('input[type="hidden"]')})
#             form = MultipartEncoder(fields=data)
#             req.headers.update({'Content-Type': form.content_type})

#             r = req.post(settings.LOGIN_PAGE, data=form.to_string())

#             logger.info(f"Login attempt response: STATUS CODE = {r.status_code}")
#             if r.status_code == 200:
#                 logger.info('Session initialized successfully.')
#                 return req
#             else:
#                 logger.error("Login attempt failed.")
#                 return None

#         except Exception as e:
#             logger.error(f"An error occurred during login: {e}")
#             return None