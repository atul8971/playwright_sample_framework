import pytest
from playwright.sync_api import Page, BrowserContext


def pytest_addoption(parser):
    """
    Add custom CLI arguments

    Args:
        parser: Pytest argument parser
    """
    parser.addoption(
        "--url",
        action="store",
        default="https://www.google.com",
        help="Base URL to navigate to"
    )


@pytest.fixture(scope="function", autouse=True)
def setup_page(request, context: BrowserContext) -> Page:
    """
    Initialize page and navigate to URL from CLI args

    Args:
        request: Pytest request object
        context: Browser context

    Returns:
        Page: Playwright page instance
    """
    # Get URL from CLI args
    url = request.config.getoption("--url")

    # Create new page
    page = context.new_page()

    # Navigate to URL
    page.goto(url)

    yield page

    # Cleanup
    page.close()
