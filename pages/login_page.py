from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import Optional


class LoginPage(BasePage):
    """Page object for the login page"""

    def __init__(self, page: Page):
        """
        Initialize LoginPage

        Args:
            page: Playwright page instance
        """
        super().__init__(page)

        # Define locators using preferred strategies (role > test-id > CSS)
        # Using role-based locators discovered from browser exploration
        self.email_input = "role=textbox[name='email@example.com']"
        self.password_input = "role=textbox[name='enter your passsword']"
        self.login_button = "role=button[name='Login']"
        self.forgot_password_link = "role=link[name='Forgot password?']"
        self.register_link = "role=link[name='Register']"

        # Success message locator
        self.success_message = "role=generic[name='Login Successfully']"

    def enter_email(self, email: str) -> None:
        """
        Enter email address

        Args:
            email: Email address to enter
        """
        self.logger.info(f"Entering email: {email}")
        self.fill(self.email_input, email)

    def enter_password(self, password: str) -> None:
        """
        Enter password

        Args:
            password: Password to enter
        """
        self.logger.info("Entering password")
        self.fill(self.password_input, password)

    def click_login_button(self) -> None:
        """Click the login button"""
        self.logger.info("Clicking login button")
        self.click(self.login_button)
        # Wait for navigation to complete
        self.wait_for_load_state("networkidle")

    def login(self, email: str, password: str) -> None:
        """
        Perform complete login action

        Args:
            email: Email address
            password: Password
        """
        self.logger.info(f"Performing login with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def wait_for_login_success(self, timeout: Optional[int] = None) -> None:
        """
        Wait for successful login (URL change to dashboard)

        Args:
            timeout: Optional timeout in milliseconds
        """
        self.logger.info("Waiting for successful login")
        self.page.wait_for_url("**/dashboard/dash", timeout=timeout or self.timeout)
        self.logger.info("Successfully navigated to dashboard")

    def is_on_login_page(self) -> bool:
        """
        Check if currently on login page

        Returns:
            bool: True if on login page, False otherwise
        """
        return self.is_visible(self.login_button) and self.is_visible(self.email_input)
