# your_app/management/commands/fetch_login.py

from django.core.management.base import BaseCommand
# from Login.login import login_to_site # Import the function from your utility module
# from Login.login import fetch_login_page # Import the function from your utility module
# from Login.login import login_to_corrlinks
from Login.message import run_push_email
# from Login.message import check_navigation
class Command(BaseCommand):
    help = 'Fetches the login page from the specified URL'

    def handle(self, *args, **kwargs):
        # Call the fetch_login_page function
        # login_to_site()
        # fetch_login_page()
        # login_to_corrlinks()
        run_push_email()
        # check_navigation()
        self.stdout.write(self.style.SUCCESS('Successfully fetched the login page.'))
