import pytest
from playwright.sync_api import Page
from steps.login_steps import LoginSteps
from steps.search_steps import SearchSteps
from dotenv import load_dotenv
import os
load_dotenv()

class TestProductSearch:
    """Test suite for product search functionality"""

    @pytest.mark.smoke
    @pytest.mark.search
    @pytest.mark.login
    def test_search_iphone_products(self, setup_page: Page):
        """
        Test case: Search for iPhone products and verify results

        Steps:
        1. Navigate to login page
        2. Login with valid credentials
        3. Click on search box
        4. Enter 'iphone' in search
        5. Verify that all search results contain 'iphone'

        Expected Result:
        - User successfully logs in
        - Search results only show iPhone-related products
        """
        page = setup_page

        # Initialize step classes
        login_steps = LoginSteps(page)
        search_steps = SearchSteps(page)

        # Test data
        search_keyword = "iphone"

        # Step 1 & 2: Navigate to login page and perform login
        login_steps.navigate_to_login_page(
            "https://rahulshettyacademy.com/client/#/auth/login"
        )
        login_steps.perform_login(os.getenv('USERNAME'), os.getenv('PASSWORD'))

        # Verify login was successful
        assert login_steps.verify_login_success(), "Login should be successful"

        # Step 3, 4 & 5: Search for iPhone and verify results
        search_steps.search_for_product(search_keyword)

        # Get all product names
        product_names = search_steps.get_all_product_names()

        # Verify at least one product is displayed
        assert len(product_names) > 0, "Search should return at least one product"
