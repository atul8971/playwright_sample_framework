import pytest
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    """
    Add custom CLI arguments
    """
    parser.addoption(
        "--url",
        action="store",
        default="https://rahulshettyacademy.com/client/#/auth/login",
        help="Base URL to navigate to"
    )
    parser.addoption(
        "--username",
        action="store",
        default="atulmysuru@gmail.com",
        help="Username for login"
    )
    parser.addoption(
        "--password",
        action="store",
        default="India123#",
        help="Password for login"
    )


@pytest.fixture(scope="session")
def username(request):
    """Fixture to get username from CLI"""
    return request.config.getoption("--username")


@pytest.fixture(scope="session")
def password(request):
    """Fixture to get password from CLI"""
    return request.config.getoption("--password")


@pytest.fixture(scope="function", autouse=True)
def setup_page(request):
    # Get URL from CLI argument
    base_url = request.config.getoption("--url")

    session = sync_playwright().start()
    browser = session.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to URL
    page.goto(base_url)

    # Attach page to test class if needed
    if request.cls:
        request.cls.page = page

    yield page

    # Teardown
    context.close()
    browser.close()
    session.stop()
