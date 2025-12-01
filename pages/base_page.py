from playwright.sync_api import Page, Locator, expect
from typing import Optional, List
from utils.logger import Logger


class BasePage:
    """Base page class with common actions for all page objects"""

    def __init__(self, page: Page):
        """
        Initialize base page

        Args:
            page: Playwright page instance
        """
        self.page = page
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.timeout = 30000

    def navigate(self, url: str) -> None:
        """
        Navigate to a URL

        Args:
            url: URL to navigate to
        """
        self.logger.info(f"Navigating to URL: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
        self.logger.info(f"Successfully navigated to: {url}")

    def click(self, locator: str | Locator, timeout: Optional[int] = None) -> None:
        """
        Click on an element

        Args:
            locator: Element locator (string or Locator object)
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        self.logger.info(f"Clicking on element: {locator}")
        element.click(timeout=timeout)
        self.logger.debug(f"Clicked on element: {locator}")

    def double_click(self, locator: str | Locator, timeout: Optional[int] = None) -> None:
        """
        Double click on an element

        Args:
            locator: Element locator
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        self.logger.info(f"Double clicking on element: {locator}")
        element.dblclick(timeout=timeout)

    def fill(self, locator: str | Locator, text: str, timeout: Optional[int] = None) -> None:
        """
        Fill text into an input field

        Args:
            locator: Element locator
            text: Text to fill
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        self.logger.info(f"Filling text '{text}' into element: {locator}")
        element.fill(text, timeout=timeout)
        self.logger.debug(f"Filled text into element: {locator}")

    def type_text(self, locator: str | Locator, text: str, delay: int = 100,
                  timeout: Optional[int] = None) -> None:
        """
        Type text with delay (simulates human typing)

        Args:
            locator: Element locator
            text: Text to type
            delay: Delay between keystrokes in milliseconds
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        self.logger.info(f"Typing text '{text}' into element: {locator}")
        element.type(text, delay=delay, timeout=timeout)

    def clear(self, locator: str | Locator, timeout: Optional[int] = None) -> None:
        """
        Clear an input field

        Args:
            locator: Element locator
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        self.logger.info(f"Clearing element: {locator}")
        element.clear(timeout=timeout)

    def select_option(self, locator: str | Locator, value: str,
                     timeout: Optional[int] = None) -> None:
        """
        Select option from dropdown

        Args:
            locator: Element locator
            value: Option value to select
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        self.logger.info(f"Selecting option '{value}' from dropdown: {locator}")
        element.select_option(value, timeout=timeout)

    def check(self, locator: str | Locator, timeout: Optional[int] = None) -> None:
        """
        Check a checkbox

        Args:
            locator: Element locator
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        self.logger.info(f"Checking checkbox: {locator}")
        element.check(timeout=timeout)

    def uncheck(self, locator: str | Locator, timeout: Optional[int] = None) -> None:
        """
        Uncheck a checkbox

        Args:
            locator: Element locator
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        self.logger.info(f"Unchecking checkbox: {locator}")
        element.uncheck(timeout=timeout)

    def hover(self, locator: str | Locator, timeout: Optional[int] = None) -> None:
        """
        Hover over an element

        Args:
            locator: Element locator
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        self.logger.info(f"Hovering over element: {locator}")
        element.hover(timeout=timeout)

    def press_key(self, key: str) -> None:
        """
        Press a keyboard key

        Args:
            key: Key to press (e.g., 'Enter', 'Escape', 'Tab')
        """
        self.logger.info(f"Pressing key: {key}")
        self.page.keyboard.press(key)

    def get_text(self, locator: str | Locator, timeout: Optional[int] = None) -> str:
        """
        Get text content of an element

        Args:
            locator: Element locator
            timeout: Optional timeout in milliseconds

        Returns:
            str: Text content of the element
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        text = element.text_content(timeout=timeout)
        self.logger.debug(f"Retrieved text '{text}' from element: {locator}")
        return text or ""

    def get_attribute(self, locator: str | Locator, attribute: str,
                     timeout: Optional[int] = None) -> Optional[str]:
        """
        Get attribute value of an element

        Args:
            locator: Element locator
            attribute: Attribute name
            timeout: Optional timeout in milliseconds

        Returns:
            str: Attribute value
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        value = element.get_attribute(attribute, timeout=timeout)
        self.logger.debug(f"Retrieved attribute '{attribute}' = '{value}' from element: {locator}")
        return value

    def is_visible(self, locator: str | Locator, timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible

        Args:
            locator: Element locator
            timeout: Optional timeout in milliseconds

        Returns:
            bool: True if visible, False otherwise
        """
        timeout = timeout or self.timeout
        try:
            element = self._get_element(locator)
            return element.is_visible(timeout=timeout)
        except Exception:
            return False

    def is_enabled(self, locator: str | Locator, timeout: Optional[int] = None) -> bool:
        """
        Check if element is enabled

        Args:
            locator: Element locator
            timeout: Optional timeout in milliseconds

        Returns:
            bool: True if enabled, False otherwise
        """
        timeout = timeout or self.timeout
        element = self._get_element(locator)
        return element.is_enabled(timeout=timeout)

    def is_checked(self, locator: str | Locator) -> bool:
        """
        Check if checkbox/radio is checked

        Args:
            locator: Element locator

        Returns:
            bool: True if checked, False otherwise
        """
        element = self._get_element(locator)
        return element.is_checked()

    def wait_for_selector(self, locator: str, state: str = "visible",
                         timeout: Optional[int] = None) -> None:
        """
        Wait for selector to be in a specific state

        Args:
            locator: Element locator string
            state: State to wait for (visible, hidden, attached, detached)
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        self.logger.info(f"Waiting for selector '{locator}' to be {state}")
        self.page.wait_for_selector(locator, state=state, timeout=timeout)

    def wait_for_url(self, url: str, timeout: Optional[int] = None) -> None:
        """
        Wait for URL to match

        Args:
            url: URL pattern to wait for
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        self.logger.info(f"Waiting for URL to match: {url}")
        self.page.wait_for_url(url, timeout=timeout)

    def wait_for_load_state(self, state: str = "load", timeout: Optional[int] = None) -> None:
        """
        Wait for page to reach a specific load state

        Args:
            state: Load state (load, domcontentloaded, networkidle)
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        self.logger.info(f"Waiting for load state: {state}")
        self.page.wait_for_load_state(state, timeout=timeout)

    def get_current_url(self) -> str:
        """
        Get current page URL

        Returns:
            str: Current URL
        """
        url = self.page.url
        self.logger.debug(f"Current URL: {url}")
        return url

    def get_title(self) -> str:
        """
        Get page title

        Returns:
            str: Page title
        """
        title = self.page.title()
        self.logger.debug(f"Page title: {title}")
        return title

    def screenshot(self, path: str, full_page: bool = False) -> None:
        """
        Take a screenshot

        Args:
            path: Path to save screenshot
            full_page: Whether to capture full page
        """
        self.logger.info(f"Taking screenshot: {path}")
        self.page.screenshot(path=path, full_page=full_page)

    def reload(self) -> None:
        """Reload the current page"""
        self.logger.info("Reloading page")
        self.page.reload()

    def go_back(self) -> None:
        """Navigate back in history"""
        self.logger.info("Navigating back")
        self.page.go_back()

    def go_forward(self) -> None:
        """Navigate forward in history"""
        self.logger.info("Navigating forward")
        self.page.go_forward()

    def get_elements(self, locator: str) -> List[Locator]:
        """
        Get all elements matching the locator

        Args:
            locator: Element locator string

        Returns:
            List of Locator objects
        """
        elements = self.page.locator(locator).all()
        self.logger.debug(f"Found {len(elements)} elements for locator: {locator}")
        return elements

    def scroll_to_element(self, locator: str | Locator) -> None:
        """
        Scroll to element

        Args:
            locator: Element locator
        """
        element = self._get_element(locator)
        self.logger.info(f"Scrolling to element: {locator}")
        element.scroll_into_view_if_needed()

    def _get_element(self, locator: str | Locator) -> Locator:
        """
        Get Locator object from string or Locator

        Args:
            locator: Element locator (string or Locator object)

        Returns:
            Locator: Playwright Locator object
        """
        if isinstance(locator, str):
            return self.page.locator(locator)
        return locator

    def assert_element_visible(self, locator: str | Locator,
                              message: Optional[str] = None) -> None:
        """
        Assert that element is visible

        Args:
            locator: Element locator
            message: Optional custom assertion message
        """
        element = self._get_element(locator)
        assertion_msg = message or f"Element {locator} should be visible"
        self.logger.info(f"Asserting: {assertion_msg}")
        try:
            expect(element).to_be_visible()
            Logger.log_assertion(self.logger, assertion_msg, True)
        except AssertionError as e:
            Logger.log_assertion(self.logger, assertion_msg, False)
            raise e

    def assert_element_hidden(self, locator: str | Locator,
                             message: Optional[str] = None) -> None:
        """
        Assert that element is hidden

        Args:
            locator: Element locator
            message: Optional custom assertion message
        """
        element = self._get_element(locator)
        assertion_msg = message or f"Element {locator} should be hidden"
        self.logger.info(f"Asserting: {assertion_msg}")
        try:
            expect(element).to_be_hidden()
            Logger.log_assertion(self.logger, assertion_msg, True)
        except AssertionError as e:
            Logger.log_assertion(self.logger, assertion_msg, False)
            raise e

    def assert_text(self, locator: str | Locator, expected_text: str,
                   message: Optional[str] = None) -> None:
        """
        Assert element contains expected text

        Args:
            locator: Element locator
            expected_text: Expected text
            message: Optional custom assertion message
        """
        element = self._get_element(locator)
        assertion_msg = message or f"Element {locator} should contain text '{expected_text}'"
        self.logger.info(f"Asserting: {assertion_msg}")
        try:
            expect(element).to_have_text(expected_text)
            Logger.log_assertion(self.logger, assertion_msg, True)
        except AssertionError as e:
            Logger.log_assertion(self.logger, assertion_msg, False)
            raise e

    def assert_url(self, expected_url: str, message: Optional[str] = None) -> None:
        """
        Assert current URL matches expected

        Args:
            expected_url: Expected URL pattern
            message: Optional custom assertion message
        """
        assertion_msg = message or f"URL should match '{expected_url}'"
        self.logger.info(f"Asserting: {assertion_msg}")
        try:
            expect(self.page).to_have_url(expected_url)
            Logger.log_assertion(self.logger, assertion_msg, True)
        except AssertionError as e:
            Logger.log_assertion(self.logger, assertion_msg, False)
            raise e

    def assert_title(self, expected_title: str, message: Optional[str] = None) -> None:
        """
        Assert page title matches expected

        Args:
            expected_title: Expected title
            message: Optional custom assertion message
        """
        assertion_msg = message or f"Page title should be '{expected_title}'"
        self.logger.info(f"Asserting: {assertion_msg}")
        try:
            expect(self.page).to_have_title(expected_title)
            Logger.log_assertion(self.logger, assertion_msg, True)
        except AssertionError as e:
            Logger.log_assertion(self.logger, assertion_msg, False)
            raise e


    def assert_attribute(self, locator: str | Locator, attribute: str, expected_value: str,
                         message: Optional[str] = None) -> None:
        """
        Assert element's attribute has the expected value

        Args:
            locator: Element locator
            attribute: Attribute name
            expected_value: Expected attribute value
            message: Optional custom assertion message
        """
        element = self._get_element(locator)
        assertion_msg = message or f"Element {locator}'s attribute '{attribute}' should be '{expected_value}'"
        self.logger.info(f"Asserting: {assertion_msg}")
        try:
            expect(element).to_have_attribute(attribute, expected_value)
            Logger.log_assertion(self.logger, assertion_msg, True)
        except AssertionError as e:
            Logger.log_assertion(self.logger, assertion_msg, False)
            raise e
