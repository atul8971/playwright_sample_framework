from playwright.sync_api import Page
from pages.login_page import LoginPage
from utils.logger import Logger

class LoginSteps:
    """Step file containing login-related business logic"""

    def __init__(self, page: Page):
        """
        Initialize LoginSteps

        Args:
            page: Playwright page instance
        """
        self.page = page
        self.login_page = LoginPage(page)
        self.logger = Logger.get_logger(__name__)

    def navigate_to_login_page(self, url: str) -> None:
        """
        Navigate to the login page

        Args:
            url: Login page URL
        """
        Logger.log_step(self.logger, f"Navigating to login page: {url}")
        self.login_page.navigate(url)
        self.logger.info("Successfully navigated to login page")

    def perform_login(self, email: str, password: str) -> None:
        """
        Perform complete login workflow

        Args:
            email: User email address
            password: User password
        """
        Logger.log_step(self.logger, f"Performing login with email: {email}")

        # Use the login method from LoginPage
        self.login_page.login(email, password)

        # Wait for successful login (navigation to dashboard)
        self.login_page.wait_for_login_success()

        self.logger.info("Login workflow completed successfully")

    def verify_login_success(self) -> bool:
        """
        Verify that login was successful by checking URL

        Returns:
            bool: True if login successful, False otherwise
        """
        Logger.log_step(self.logger, "Verifying login success")

        current_url = self.page.url
        is_successful = "/dashboard/dash" in current_url

        if is_successful:
            Logger.log_assertion(
                self.logger,
                "User successfully logged in and redirected to dashboard",
                True
            )
        else:
            Logger.log_assertion(
                self.logger,
                f"User login failed or not redirected to dashboard. Current URL: {current_url}",
                False
            )

        return is_successful

    def login_with_credentials(self, email: str, password: str) -> None:
        """
        Complete login flow with credentials

        Args:
            email: User email address
            password: User password
        """
        Logger.log_step(self.logger, f"Starting login flow for user: {email}")
        self.perform_login(email, password)
        self.verify_login_success()
