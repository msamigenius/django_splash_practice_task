

import datetime

import logging

def convert_cookies_to_splash_format(splash_cookies=None, cookies=None):
    """
    Converts cookies to the format required by Splash.

    Parameters:
    - splash_cookies (list): The list to which formatted cookies will be appended.
    - cookies (dict): The dictionary of cookies to be converted, with cookie names as keys and cookie values as values.

    Returns:
    - list: The updated list of Splash-formatted cookies if both parameters are provided.
    - bool: False if the necessary parameters are not provided.

    This function takes a dictionary of cookies and appends them to a list in a format that can be used by Splash,
    including setting attributes such as name, value, expiration time, path, httpOnly, secure, and domain.
    If either parameter is missing or None, the function returns False.
    """
    if (not splash_cookies == None) and (cookies):
        now = datetime.datetime.now()
        expires = now + datetime.timedelta(hours=1)
        for name, value in cookies.items():
            cookie = {
                'name': name,
                'value': value,
                'expires': expires.isoformat(),
                'path': '/',
                'httpOnly': True,
                'secure': True,
                'domain': 'www.corrlinks.com'
            }
            splash_cookies.append(cookie)
        return splash_cookies
    else:
        return False
 