# Playwright Python UI Automation Framework

A comprehensive UI automation framework built with Playwright and Python, following the Page Object Model (POM) design pattern with a clear abstraction layer: Tests → Steps → Pages.

## Framework Architecture

```
playwright_test_fw/
├── pages/              # Page Object Models
│   ├── base_page.py   # Base page with common actions
│   ├── login_page.py  # Login page object
│   └── home_page.py   # Home page object
├── steps/              # Business logic layer
│   └── login_steps.py # Login workflow steps
├── tests/              # Test cases
│   ├── conftest.py    # Pytest fixtures and configuration
│   └── test_login.py  # Login test scenarios
├── utils/              # Utility modules
│   ├── logger.py      # Custom logging implementation
│   └── config.py      # Configuration management
├── logs/               # Test execution logs
├── reports/            # Test reports
├── screenshots/        # Failure screenshots
├── videos/             # Test execution videos
├── pytest.ini         # Pytest configuration
├── requirements.txt   # Python dependencies
└── .env               # Environment variables
```

## Design Patterns & Principles

### 1. Page Object Model (POM)
- Each page is represented as a class
- Page elements (locators) are defined as class attributes
- Page actions are defined as methods
- All pages inherit from `BasePage`

### 2. Three-Layer Abstraction
```
Tests (What to test)
  ↓
Steps (Business Logic)
  ↓
Pages (UI Interactions)
```

- **Tests**: High-level test scenarios focusing on WHAT to test
- **Steps**: Business logic and workflows (HOW to execute)
- **Pages**: UI interactions and element manipulations (WHERE to interact)

### 3. Key Features

#### Base Page
- Common actions: click, fill, select, check, hover, etc.
- Wait strategies: wait_for_selector, wait_for_url, wait_for_load_state
- Assertions: assert_element_visible, assert_text, assert_url
- Logging: All actions are logged automatically
- Screenshot capabilities

#### Configuration Management
- CLI arguments for dynamic configuration
- Environment-specific settings
- Credential management
- Singleton pattern for global config access

#### Logging
- Dual output: Console and file logging
- Structured log format with timestamps
- Step-level logging
- Assertion logging with pass/fail status
- Separate log files per day

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. Clone the repository
```bash
cd playwright_test_fw
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers
```bash
playwright install
```

5. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

### CLI Arguments

```bash
pytest --env=qa --browser=chromium --headed --slowmo=500
```

Available arguments:
- `--env`: Environment (dev, qa, staging, prod) - Default: qa
- `--browser`: Browser (chromium, firefox, webkit) - Default: chromium
- `--headed`: Run in headed mode - Default: headless
- `--slowmo`: Slow down execution (ms) - Default: 0
- `--base-url`: Base URL override
- `--timeout`: Default timeout (ms) - Default: 30000

### Environment Variables (.env)

```properties
ENV=qa
BROWSER=chromium
HEADED=false
SLOWMO=0
TIMEOUT=30000

QA_URL=https://qa.example.com
DEFAULT_USERNAME=test@example.com
DEFAULT_PASSWORD=Test@123
```

## Usage

### Running Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_login.py
```

Run specific test:
```bash
pytest tests/test_login.py::TestLogin::test_login_with_valid_credentials
```

Run tests with markers:
```bash
pytest -m smoke           # Run smoke tests
pytest -m login           # Run login tests
pytest -m "smoke and login"  # Run tests with both markers
```

Run tests in parallel:
```bash
pytest -n 4  # Run with 4 workers
```

Run with specific environment:
```bash
pytest --env=staging --browser=firefox --headed
```

### Test Reports

HTML Report:
```bash
pytest --html=reports/report.html --self-contained-html
```

Allure Report:
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Writing Tests

### Example Test Structure

```python
import pytest
from playwright.sync_api import Page
from steps.login_steps import LoginSteps

class TestLogin:
    @pytest.mark.smoke
    def test_login_success(self, page: Page, login_steps: LoginSteps):
        # Navigate and verify page
        login_steps.navigate_to_login_page()
        login_steps.login_page.verify_login_page_loaded()

        # Perform login
        login_steps.login_with_valid_credentials()

        # Verify success
        login_steps.verify_login_successful()
```

### Creating New Page Objects

```python
from pages.base_page import BasePage

class MyPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # Define locators
        self.submit_button = "button[type='submit']"
        self.input_field = "input#myfield"

    def submit_form(self):
        self.logger.info("Submitting form")
        self.click(self.submit_button)
```

### Creating Step Files

```python
from pages.my_page import MyPage
from utils.logger import Logger

class MySteps:
    def __init__(self, page):
        self.page = page
        self.my_page = MyPage(page)
        self.logger = Logger.get_logger(__name__)

    def complete_workflow(self):
        Logger.log_step(self.logger, "Complete workflow")
        self.my_page.fill(self.my_page.input_field, "test")
        self.my_page.submit_form()
```

## Best Practices

1. **Separation of Concerns**
   - Keep tests simple and readable
   - Business logic goes in steps
   - UI interactions go in pages

2. **Naming Conventions**
   - Tests: `test_<scenario_name>`
   - Pages: `<page_name>_page.py`
   - Steps: `<feature_name>_steps.py`

3. **Locator Strategy**
   - Prefer user-facing attributes (role, text, label)
   - Use data-testid for dynamic content
   - Avoid XPath unless necessary

4. **Assertions**
   - Use built-in assertion methods from BasePage
   - Add meaningful assertion messages
   - Verify one thing per assertion

5. **Logging**
   - Use Logger.log_step() for major steps
   - Log important actions and verifications
   - Include context in log messages

6. **Screenshots**
   - Automatic screenshots on failure
   - Manual screenshots for debugging
   - Stored in screenshots/ directory

## Troubleshooting

### Common Issues

**Issue: Tests failing with timeout**
```bash
pytest --timeout=60000  # Increase timeout to 60 seconds
```

**Issue: Browser not found**
```bash
playwright install chromium
```

**Issue: Logs not generated**
- Check `logs/` directory permissions
- Verify pytest.ini log configuration

**Issue: Screenshots not saved**
- Check `screenshots/` directory exists
- Verify conftest.py fixture configuration

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Playwright Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps
      - name: Run tests
        run: pytest --env=qa
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: |
            reports/
            screenshots/
            logs/
```

## Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Follow PEP 8 style guidelines
5. Add meaningful commit messages

## License

This framework is provided as-is for educational and testing purposes.

## Support

For issues and questions:
- Check the documentation
- Review example tests
- Check logs for detailed error messages
