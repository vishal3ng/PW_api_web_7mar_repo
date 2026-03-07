# PW_Automation — Corporate Test Automation Framework

**Playwright (Web) + Appium (iOS/Android) + REST API | Python | Allure | GitHub Actions**

---

## Framework Architecture

```
PW_automation/
├── config/
│   ├── config.yaml           Master config: URLs, browser, mobile, email, users
│   └── config_loader.py      CFG singleton — resolves ${ENV_VAR} placeholders
├── users/
│   └── users.json            User pool: buyer, seller, admin, api_user, mobile_user
├── pages/
│   ├── web/
│   │   ├── web_common.py     Base class: ALL Playwright generic methods
│   │   ├── login_page.py
│   │   └── home_page.py
│   ├── mobile/
│   │   ├── mobile_common.py  Base class: ALL Appium generic methods (iOS+Android)
│   │   └── mobile_login_page.py
│   └── api/
│       ├── api_common.py     Base class: ALL REST API generic methods
│       └── objects_service.py
├── tests/
│   ├── test_web/             Playwright browser tests
│   ├── test_api/             REST API tests
│   └── test_mobile/          Android and iOS Appium tests
├── util/
│   ├── user_manager.py       Thread-safe parallel user pool
│   ├── logger_util.py        Per-test file + console logger
│   └── email_util.py         Gmail SMTP notifications
├── .github/workflows/
│   └── playwright_tests.yml  CI: push + daily 8AM + manual trigger
├── conftest.py               All fixtures, hooks, video, user pool
├── pytest.ini                Test discovery, markers, logging
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

## How The Framework Runs — Deep Explanation

### 1. Config Loading (on first import)

When any test file is imported, config_loader.py creates a singleton CFG object:
- Reads config/config.yaml
- Checks ENVIRONMENT env var (default: staging)
- Loads the correct URL block, credentials, and settings for that environment
- Resolves every ${VAR} placeholder from os.environ
- If a required env var is missing, raises a clear EnvironmentError

Every module that does `from config.config_loader import CFG` gets the same resolved config.

---

### 2. Session Setup (conftest.py)

Runs ONCE at the very start of a test session:
- Clears the logs/ directory (unless retain_logs: true)
- Creates allure-results/ and logs/ directories
- Calls reset_all_users() — unlocks any users stuck in-use from a crashed run

---

### 3. User Pool — Parallel-Safe Credential Management

Each test that needs a user declares the fixture:

    def test_checkout(self, page, buyer_user, logger):
        # buyer_user = {"username": "buyer1@example.com", "password": "...", "role": "buyer"}

How it works:
  1. acquire_user("buyer") opens users.json with a threading lock
  2. Finds first user where role == "buyer" AND in_use == False
  3. Sets in_use = True, locked_by = worker_id, writes JSON
  4. Returns user dict to the test
  5. After test, release_user() sets in_use = False

4 parallel workers can each hold a different buyer account simultaneously.
If no user is free, worker waits up to lock_timeout_seconds before raising TimeoutError.

User roles:
  admin       - Admin panel, user management
  buyer       - Shopping, checkout, orders
  seller      - Product listing, inventory
  viewer      - Read-only access
  api_user    - API tests — has api_token field
  mobile_user - Mobile app login tests

---

### 4. Web Test Execution (Playwright)

Fixture chain: playwright_instance -> browser -> page -> logger

page fixture flow:
  1. Creates browser context with record_video_dir = allure-results/videos/
  2. Sets viewport and default timeout from config
  3. Opens a new page, yields to test
  4. AFTER TEST:
     - Closes the page
     - Gets raw video path from page.video.path()
     - RENAMES video to <test_name>_<timestamp>.webm (named after test)
     - Closes context (finalizes video)
     - Stores named video path on request.node._video_path

---

### 5. Mobile Test Execution (Appium)

android_driver fixture:
  - Reads caps from CFG.android_caps
  - Connects to Appium server at CFG.appium_server
  - Auto-quits after test
  - Auto-skips if appium-python-client not installed

ios_driver fixture:
  - Same but XCUITest caps, UDID from ${IOS_UDID} env var

Both fixtures skip gracefully so web/API tests still run on machines without Appium.

---

### 6. API Test Execution

Tests use a service class (e.g. ObjectsService) extending APICommon.

Every HTTP call:
  1. Builds full URL from CFG.api_base_url + endpoint
  2. Sends via requests.Session (keeps auth headers)
  3. Retries on 500/502/503/504 up to CFG.api_max_retries times
  4. Attaches request body, response body, headers to Allure automatically
  5. Returns Response object for assertions

---

### 7. After Each Test — pytest_runtest_makereport Hook

Always: log file attached to Allure as TEXT

On failure:
  - Screenshot from item.cls.driver (works for Playwright page AND Appium driver)
  - Video file read from _video_path (set by page fixture) attached as WEBM
  - Failure appended to _failed_tests list
  - Per-test failure email sent (if configured)

---

### 8. Allure Report Contents

  Test log file       Every test (pass + fail)
  Screenshot          On failure (web + mobile)
  Video (.webm)       On failure — named after test
  API Request body    Every API call
  API Response body   Every API call
  Response headers    Every API call

---

### 9. CI/CD — GitHub Actions

Triggers:
  - Push/merge to main         Every commit
  - Pull Request to main       Every PR
  - schedule: 30 2 * * 1-5    Mon-Fri at 08:00 IST (02:30 UTC)
  - workflow_dispatch          Manual — choose env + suite + workers

CI Steps:
  1. Checkout code
  2. Python 3.11 setup
  3. pip install -r requirements.txt
  4. playwright install --with-deps chromium
  5. pytest -v -n $WORKERS -m $SUITE --alluredir=allure-results
  6. Upload allure-results artifact (14 days)
  7. Generate Allure HTML report
  8. Deploy to GitHub Pages (gh-pages branch)
  9. Upload logs/ on failure

All credentials come from GitHub Secrets — never hardcoded.

---

## Quick Start

    # 1. Clone and enter
    git clone <your-repo>
    cd PW_automation

    # 2. Create virtual environment
    python -m venv venv
    source venv/bin/activate       # Windows: venv\Scripts\activate

    # 3. Install dependencies
    pip install -r requirements.txt
    playwright install chromium

    # 4. Set up local secrets
    cp .env.example .env
    # Edit .env with real values

    # 5. Run all tests
    pytest

    # 6. Run specific suites
    pytest -m smoke
    pytest -m api
    pytest -m "web and not performance"

    # 7. Run in parallel (4 workers)
    pytest -n 4

    # 8. View Allure report
    allure serve allure-results

---

## Mobile Setup

    pip install appium-python-client==3.1.0
    npm install -g appium
    appium driver install uiautomator2    # Android
    appium driver install xcuitest        # iOS (macOS only)
    appium --port 4723
    pytest -m android
    pytest -m ios

---

## GitHub Secrets Required

  EMAIL_SENDER     Gmail address for reports
  EMAIL_PASSWORD   Gmail App Password
  PROD_USERNAME    Production test user
  PROD_PASSWORD    Production test password
  IOS_UDID         iOS device UDID
  GITHUB_TOKEN     Auto-provided for Pages deploy
