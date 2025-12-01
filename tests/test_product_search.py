import pytest
from playwright.sync_api import Page
from steps.login_steps import LoginSteps
from steps.search_steps import SearchSteps


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
        email = "atulmysuru@gmail.com"
        password = "India123#"
        search_keyword = "iphone"

        # Step 1 & 2: Navigate to login page and perform login
        login_steps.navigate_to_login_page(
            "https://rahulshettyacademy.com/client/#/auth/login"
        )
        login_steps.perform_login(email, password)

        # Verify login was successful
        assert login_steps.verify_login_success(), "Login should be successful"

        # Step 3, 4 & 5: Search for iPhone and verify results
        search_steps.search_for_product(search_keyword)

        # Get all product names
        product_names = search_steps.get_all_product_names()

        # Verify at least one product is displayed
        assert len(product_names) > 0, "Search should return at least one product"

        # Verify all products contain 'iphone' keyword
        assert search_steps.verify_all_products_contain_keyword(
            search_keyword
        ), f"All products should contain '{search_keyword}'"

        # Additional verification: Check each product name individually
        for product_name in product_names:
            assert search_keyword.lower() in product_name.lower(), (
                f"Product '{product_name}' should contain '{search_keyword}'"
            )

    @pytest.mark.smoke
    @pytest.mark.search
    def test_search_iphone_with_url_navigation(self, setup_page: Page):
        """
        Test case: Alternative approach - Direct navigation to login URL then search

        This test demonstrates using the conftest fixture that already navigates
        to the URL provided via CLI args.

        Steps:
        1. Login with valid credentials (page already at login URL via conftest)
        2. Search for 'iphone'
        3. Verify search results

        Expected Result:
        - User successfully logs in
        - Search returns only iPhone products
        """
        page = setup_page

        # Initialize step classes
        login_steps = LoginSteps(page)
        search_steps = SearchSteps(page)

        # Test data
        email = "atulmysuru@gmail.com"
        password = "India123#"

        # Perform login (page is already at login URL via conftest)
        login_steps.perform_login(email, password)

        # Verify login success
        login_success = login_steps.verify_login_success()
        assert login_success, "User should be logged in and on dashboard"

        # Search for iPhone products
        search_steps.search_for_product("iphone")

        # Verify search results contain iPhone
        verification_result = search_steps.verify_all_products_contain_keyword("iphone")
        assert verification_result, "All search results should contain 'iphone'"

        # Verify product count is at least 1
        product_count = search_steps.get_product_count()
        assert product_count >= 1, f"Expected at least 1 product, found {product_count}"

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_empty_results(self, setup_page: Page):
        """
        Test case: Search for a product that doesn't exist

        Steps:
        1. Navigate and login
        2. Search for non-existent product
        3. Verify appropriate results

        Expected Result:
        - Search should return 0 results or show appropriate message
        """
        page = setup_page

        # Initialize step classes
        login_steps = LoginSteps(page)
        search_steps = SearchSteps(page)

        # Test data
        email = "atulmysuru@gmail.com"
        password = "India123#"
        non_existent_product = "xyz123nonexistent"

        # Login
        login_steps.navigate_to_login_page(
            "https://rahulshettyacademy.com/client/#/auth/login"
        )
        login_steps.perform_login(email, password)

        # Search for non-existent product
        search_steps.search_for_product(non_existent_product)

        # Verify no products are found
        product_count = search_steps.get_product_count()
        assert product_count == 0, (
            f"Expected 0 products for non-existent search, found {product_count}"
        )
