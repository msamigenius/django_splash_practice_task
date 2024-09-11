# push_email.py
import requests
from PIL import Image
from io import BytesIO
import base64
import logging
import json
import requests
from Login.login import login_to_corrlinks
# from variables import MAX_EMAIL_REPLY_RETRIES, HEADERS_FOR_PUSH_EMAIL_REQUEST, SPLASH_URL, \
#     ENVIRONMENT
from utils.helper_functions import convert_cookies_to_splash_format
from Login_system.settings import MAX_EMAIL_REPLY_RETRIES, HEADERS_FOR_PUSH_EMAIL_REQUEST,SPLASH_URL

# Set up logging
logging.basicConfig(filename='push_email_interaction.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
SPLASH_URL = 'http://localhost:8050/execute'

# Static cookies (these don't change between sessions)
STATIC_COOKIES = {
    '__cflb': '02DiuJS4Qt1fYJgjizGYDpBdpvG3kZuePiK6aACa2VVk8',
    'cf_clearance': 'NVzVrHA955EqW3BWDz88iyjl3C9DgxYunr5aA39Ime0-1720556066-1.0.1.1-iRuayH1JZaLN0s7CorH6YLiiL6473CYJDarLnx57PclIoO3rJL1j_WVDVTzRamuBzuDeGSzZA8Hf4rj2BVzjZg'
}

def capture_session_state(session):
    """
    Captures the current state of the session, including headers and dynamic cookies.
    """
    state = {
        'headers': dict(session.headers),
        'cookies': {k: v for k, v in session.cookies.items() if k not in STATIC_COOKIES}
    }
    logging.info("Captured session state:")
    logging.info(json.dumps(state, indent=2))
    return state

def log_response_info(response, is_splash_response=False, retry_number=0):
    """
    Logs detailed information about an HTTP response.
    Parameters:
    - response (requests.Response): The response object to log

    This function logs various details of the HTTP response including URL,
    status code, headers, cookies, and a portion of the response body.
    It also saves the full HTML content to a file for inspection.
    """
    logging.info(f"=== RESPONSE INFO ===")
    logging.info(f"URL: {response.url}")
    logging.info(f"Status Code: {response.status_code}")
    logging.info(f"Headers: {json.dumps(dict(response.headers), indent=2)}")
    logging.info(f"Cookies: {json.dumps(dict(response.cookies), indent=2)}")
    
    # Save the full HTML content to a file for inspection
    if is_splash_response:
        json_response = response.json()
        html_content = json_response.get('html')
        logging.info(f"Response Body: {response.text[:1000]}")
        if not html_content == None:
            with open(f"response_content_{response.status_code}_try{retry_number}.html", "w", encoding="utf-8") as f:
                f.write(html_content)
        else:
            logging.error(f"Empty HTML page returned. {response.url} {response.status_code}")
    else:
        logging.info(f"Response Body: {response.text[:1000]}")
        with open(f"response_content_{response.status_code}_try{retry_number}.html", "w", encoding="utf-8") as f:
            f.write(response.text)
    logging.info(f"=====================")


def send_email_reply(session,subject ,message_content, session_state):


    reply_url = f"https://www.corrlinks.com/NewMessage.aspx"

    with open('utils/lua_scripts/send_email_reply.lua', 'r') as file:
        lua_script = file.read()
        print("splash script read successfully")
    headers = HEADERS_FOR_PUSH_EMAIL_REQUEST
    cookies = session_state['cookies']
    


    """
    Here converting the cookies to a format that is accpeted by the splash browser
  .
    """
    splash_cookies = []
    splash_cookies = convert_cookies_to_splash_format(splash_cookies=splash_cookies, cookies=cookies)
    if splash_cookies == False:
        logging.error(f'Error occured while converting cookies to splash browser format. \
        This is what was returned by the |convert_cookies_to_splash_format| function. {splash_cookies}')
        return False

    """
    This function converts cookies into a string format for use in request headers.
    """
    cookie_header = "; ".join([f"{key}={value}" for key, value in cookies.items()])

    # Setting up all the required parameters for the request to the splash service.
    params = {
        'lua_source': lua_script,
        'reply_url': reply_url,
        'subject_content' : subject,
        'message_content': message_content,
        'headers' : headers,
        'cookies' : cookie_header,
        'splash_cookies' : splash_cookies
    }

    """
    This is a simple retry mechanism for the email reply request.
    """
    result = None
    request_success = False
    print("good")
    for retry_number in range(MAX_EMAIL_REPLY_RETRIES):
        response = session.post(SPLASH_URL, json=params)
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
    
    # Extract the HTML content and screenshot from the result
            html_content = result['html']
            screenshot_data = result['png']
            output = result['result']
            # har = result['har']
            print(output)
            # print(har)


    # Print the HTML content
            # print(html_content)

    # Decode the screenshot from base64 and display it using PIL
            screenshot = Image.open(BytesIO(base64.b64decode(screenshot_data)))
            screenshot.show()
        else:
              print(f"Error: {response.status_code}")
              print(response.text)
    #     result = response.json()

        log_response_info(response=response, is_splash_response=True, retry_number=retry_number + 1)
        print(response.status_code)
        if response.status_code == 200 and output:
            logging.info('Message sent successfully.')
            logging.info('----------------------------------')
            return True



def run_push_email():
    """
    Runs the push email process
    """

    
    session = login_to_corrlinks()
    if not session:
        logging.error("Failed to login to Corrlinks")
        return "Failed to login to Corrlinks"

    # Capture the session state right after login
    session_state = capture_session_state(session)
    print("hello")
    message_subject="Testing Purpose message"
    message_content='This message is for texting purpose. sorry for inconvience.'

    success = send_email_reply(session=session,subject=message_subject, message_content=message_content,  session_state=session_state)
    print(success)
    if success:
           
        logging.info(f"Email message sent successfully ")
    else:
        logging.error("Failed to send email ")
    return "Push email operation completed."


