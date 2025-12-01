from playwright.sync_api import Page
from pages.products_page import ProductsPage
from utils.logger import Logger
from typing import List


class SearchSteps:
    """Step file containing search-related business logic"""

    def __init__(self, page: Page):
        """
        Initialize SearchSteps

        Args:
            page: Playwright page instance
        """
        self.page = page
        self.products_page = ProductsPage(page)
        self.logger = Logger.get_logger(__name__)

    def search_for_product(self, product_name: str) -> None:
        """
        Perform product search workflow

        Args:
            product_name: Name of the product to search
        """
        Logger.log_step(self.logger, f"Searching for product: {product_name}")

        # Perform search using ProductsPage
        self.products_page.search_product(product_name)

        self.logger.info(f"Search workflow completed for: {product_name}")

    def get_all_product_names(self) -> List[str]:
        """
        Get all visible product names from search results

        Returns:
            List[str]: List of product names
        """
        Logger.log_step(self.logger, "Retrieving all product names from search results")

        product_names = self.products_page.get_all_product_names()

        self.logger.info(f"Retrieved {len(product_names)} product names: {product_names}")
        return product_names

    def verify_all_products_contain_keyword(self, keyword: str) -> bool:
        """
        Verify that all search results contain the specified keyword

        Args:
            keyword: Keyword to verify in product names

        Returns:
            bool: True if all products contain keyword, False otherwise
        """
        Logger.log_step(
            self.logger,
            f"Verifying all search results contain keyword: '{keyword}'"
        )

        result = self.products_page.verify_all_products_contain(keyword)

        if result:
            Logger.log_assertion(
                self.logger,
                f"All products contain the keyword '{keyword}'",
                True
            )
        else:
            Logger.log_assertion(
                self.logger,
                f"Not all products contain the keyword '{keyword}'",
                False
            )

        return result

    def verify_product_count(self, expected_count: int) -> bool:
        """
        Verify the number of products displayed

        Args:
            expected_count: Expected number of products

        Returns:
            bool: True if count matches, False otherwise
        """
        Logger.log_step(self.logger, f"Verifying product count equals {expected_count}")

        actual_count = self.products_page.get_product_count()

        if actual_count == expected_count:
            Logger.log_assertion(
                self.logger,
                f"Product count matches expected: {expected_count}",
                True
            )
            return True
        else:
            Logger.log_assertion(
                self.logger,
                f"Product count mismatch. Expected: {expected_count}, Actual: {actual_count}",
                False
            )
            return False

    def search_and_verify_results(self, product_name: str) -> bool:
        """
        Complete workflow: search for product and verify results contain keyword

        Args:
            product_name: Product name to search for

        Returns:
            bool: True if verification passed, False otherwise
        """
        Logger.log_step(
            self.logger,
            f"Starting search and verify workflow for: {product_name}"
        )

        # Perform search
        self.search_for_product(product_name)

        # Verify results
        verification_result = self.verify_all_products_contain_keyword(product_name)

        return verification_result

    def get_product_count(self) -> int:
        """
        Get the count of visible products

        Returns:
            int: Number of products displayed
        """
        count = self.products_page.get_product_count()
        self.logger.info(f"Current product count: {count}")
        return count
