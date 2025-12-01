import pytest
from playwright.sync_api import Page
from steps.login_steps import LoginSteps


class TestLogin:
    """Test class for login functionality"""

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.critical
    def test_login_with_valid_credentials_and_verify_results(self, setup_page: Page, test_credentials: dict):
        """
        Test successful login and verify 3 results are displayed

        This test:
        1. Navigates to the login page (handled by setup_page fixture)
        2. Enters valid credentials
        3. Clicks login button
        4. Verifies login success
        5. Verifies that 3 results are displayed
        """
        # Get the page instance from fixture
        page = setup_page

        # Create steps instance
        login_steps = LoginSteps(page)

        # Test data
        expected_results = 3

        # Step 1-4: Perform login
        login_steps.perform_login(test_credentials["email"], test_credentials["password"])

        # Step 5: Verify login success
        assert login_steps.verify_login_success(), "Login should be successful"

        # Step 6: Verify 3 results are displayed
        actual_count = login_steps.get_displayed_results_count()
        assert actual_count == expected_results, \
            f"Expected {expected_results} results but found {actual_count}"

        # Verify URL contains dashboard
        assert "/dashboard/dash" in page.url, \
            "URL should contain '/dashboard/dash' after login"

    @pytest.mark.login
    @pytest.mark.regression
    def test_login_displays_correct_product_count(self, setup_page: Page, test_credentials: dict):
        """
        Test that product cards match the displayed count

        This test verifies that the number shown in "Showing X results"
        matches the actual number of product cards displayed
        """
        page = setup_page
        login_steps = LoginSteps(page)

        # Perform login
        login_steps.perform_login(test_credentials["email"], test_credentials["password"])

        # Get displayed count from text
        displayed_count = login_steps.get_displayed_results_count()

        # Get actual product card count
        actual_product_cards = login_steps.products_page.get_product_count()

        # Verify they match
        assert displayed_count == actual_product_cards, \
            f"Displayed count ({displayed_count}) should match actual product cards ({actual_product_cards})"
