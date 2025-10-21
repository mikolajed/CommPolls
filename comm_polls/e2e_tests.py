from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from django.utils import timezone
from django.test import override_settings
from datetime import timedelta

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class UserE2ETests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        """Ensure each test starts from the home page."""
        self.driver.get(self.live_server_url)

    def test_signup_login_logout_flow(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign up"))).click()

        # Fill signup form
        wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("e2euser")
        driver.find_element(By.NAME, "email").send_keys("e2e@example.com")
        driver.find_element(By.NAME, "password1").send_keys("E2ePass123")
        driver.find_element(By.NAME, "password2").send_keys("E2ePass123")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Check if redirected to home and logged in
        welcome_message = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "strong"))).text
        self.assertIn("Hello, e2euser!", welcome_message)

        # Logout
        driver.find_element(By.LINK_TEXT, "Logout").click()
        signup_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Sign up"))).text
        self.assertEqual("Sign up", signup_link)

    def test_create_and_vote_on_poll(self):
        """Test creating a poll, and another user voting on it."""
        # Create users directly for setup
        creator = User.objects.create_user('creator', 'creator@test.com', 'password123')
        voter = User.objects.create_user('voter', 'voter@test.com', 'password123')

        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # --- Creator logs in and creates a poll ---
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
        wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("creator")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Navigate to create poll page
        wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Create Poll"))).click()

        # Fill out poll form
        wait.until(EC.visibility_of_element_located((By.NAME, "name"))).send_keys("E2E Test Poll")
        now = timezone.now()
        start_date = now - timedelta(minutes=1)
        end_date = now + timedelta(hours=1)
        driver.find_element(By.NAME, "start_date").send_keys(start_date.strftime("%Y-%m-%dT%H:%M"))
        driver.find_element(By.NAME, "end_date").send_keys(end_date.strftime("%Y-%m-%dT%H:%M"))

        # Fill out choices
        driver.find_element(By.NAME, "form-0-name").send_keys("Choice A")
        driver.find_element(By.NAME, "form-1-name").send_keys("Choice B")

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Verify poll was created and logout
        my_polls_header = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        self.assertEqual("My Created Polls", my_polls_header)
        self.assertIn("E2E Test Poll", driver.page_source)
        driver.find_element(By.LINK_TEXT, "Logout").click()

        # --- Voter logs in and votes ---
        wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Login"))).click()
        wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("voter")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Find the poll and vote
        wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Vote Now"))).click()

        # Select a choice and vote
        wait.until(EC.visibility_of_element_located((By.ID, "choice1"))).click()
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Verify results page
        results_header = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        self.assertIn("Results for: E2E Test Poll", results_header)
        self.assertIn("Choice A", driver.page_source)
        self.assertIn("1", driver.page_source) # Check for 1 vote

    def element_exists(self, by, value):
        """Helper to check if element exists"""
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False
