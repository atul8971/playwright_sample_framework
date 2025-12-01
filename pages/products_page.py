from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import List, Optional
import pandas as pd

class ProductsPage(BasePage):
    """Page object for products/dashboard page with search functionality"""

    def __init__(self, page: Page):
        """
        Initialize ProductsPage

        Args:
            page: Playwright page instance
        """
        super().__init__(page)

        # Navigation locators
        self.home_button = "role=button[name=' HOME']"
        self.orders_button = "role=button[name=' ORDERS']"
        self.cart_button = "role=button[name=' Cart']"
        self.signout_button = "role=button[name='Sign Out']"

        # Search and filter locators
        self.search_input = "role=textbox[name='search']"
        self.min_price_input = "role=textbox[name='Min Price']"
        self.max_price_input = "role=textbox[name='Max Price']"

        # Product card locators
        self.product_cards = ".card-body"
        self.product_names = "h5.card-title"
        self.product_prices = ".card-body b"
        self.add_to_cart_buttons = "button:has-text('Add To Cart')"
        self.view_buttons = "button:has-text('View')"

        # Results info
        self.results_count = "div:has-text('Showing') >> nth=0"

    def click_search_box(self) -> None:
        """Click on the search input box"""
        self.logger.info("Clicking search box")
        self.click(self.search_input)

    def enter_search_text(self, search_text: str) -> None:
        """
        Enter text in search box

        Args:
            search_text: Text to search for
        """
        self.logger.info(f"Entering search text: {search_text}")
        self.fill(self.search_input, search_text)

    def press_enter_in_search(self) -> None:
        """Press Enter key to trigger search"""
        self.logger.info("Pressing Enter to trigger search")
        self.press_key("Enter")
        # Wait for search results to load
        self.wait_for_load_state('networkidle')

    def search_product(self, product_name: str) -> None:
        """
        Perform complete product search

        Args:
            product_name: Name of the product to search
        """
        self.logger.info(f"Searching for product: {product_name}")
        self.click_search_box()
        self.enter_search_text(product_name)
        self.press_enter_in_search()
        self.logger.info(f"Search completed for: {product_name}")

    def get_all_product_names(self) -> List[str]:
        """
        Get names of all visible products

        Returns:
            List[str]: List of product names
        """
        self.logger.info("Retrieving all product names")
        product_elements = self.get_elements(self.product_names)
        product_names = [element.text_content() for element in product_elements]
        self.logger.info(f"Found {len(product_names)} products: {product_names}")
        return product_names

    def get_product_count(self) -> int:
        """
        Get count of visible products

        Returns:
            int: Number of visible products
        """
        product_elements = self.get_elements(self.product_cards)
        count = len(product_elements)
        self.logger.info(f"Product count: {count}")
        return count

    def verify_all_products_contain(self, keyword: str) -> bool:
        """
        Verify that all product names contain the specified keyword

        Args:
            keyword: Keyword to check in product names

        Returns:
            bool: True if all products contain keyword, False otherwise
        """
        self.logger.info(f"Verifying all products contain keyword: {keyword}")
        product_names = self.get_all_product_names()

        if not product_names:
            self.logger.warning("No products found")
            return False

        # Check each product name (case-insensitive)
        keyword_lower = keyword.lower()
        products_without_keyword = []

        for product_name in product_names:
            if keyword_lower not in product_name.lower():
                products_without_keyword.append(product_name)

        if products_without_keyword:
            self.logger.error(
                f"Products not containing '{keyword}': {products_without_keyword}"
            )
            return False

        self.logger.info(f"All {len(product_names)} products contain '{keyword}'")
        return True

    def get_results_count_text(self) -> str:
        """
        Get the results count text

        Returns:
            str: Results count text (e.g., "Showing 1 results |")
        """
        text = self.get_text(self.results_count)
        self.logger.debug(f"Results count text: {text}")
        return text

    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """
        Add a product to cart by its name

        Args:
            product_name: Name of the product to add to cart
        """
        self.logger.info(f"Adding product '{product_name}' to cart")
        # Locate the product card containing the product name, then find Add to Cart button
        product_card_locator = f"h5:has-text('{product_name}') >> xpath=ancestor::div[contains(@class, 'card-body')]"
        add_to_cart_button = f"{product_card_locator} >> button:has-text('Add To Cart')"
        self.click(add_to_cart_button)
        self.logger.info(f"Product '{product_name}' added to cart")

    def is_on_products_page(self) -> bool:
        """
        Check if currently on products/dashboard page

        Returns:
            bool: True if on products page, False otherwise
        """
        return "/dashboard/dash" in self.get_current_url() and self.is_visible(self.search_input)

    def click_signout(self) -> None:
        """Click sign out button"""
        self.logger.info("Clicking sign out button")
        self.click(self.signout_button)
        self.wait_for_load_state('networkidle')
