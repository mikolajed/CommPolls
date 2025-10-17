from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

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
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_signup_login_logout_flow(self):
        driver = self.driver
        driver.get(f"{self.live_server_url}/signup/")

        # Fill signup form
        driver.find_element(By.NAME, "username").send_keys("e2euser")
        driver.find_element(By.NAME, "email").send_keys("e2e@example.com")
        driver.find_element(By.NAME, "password1").send_keys("E2ePass123")
        driver.find_element(By.NAME, "password2").send_keys("E2ePass123")
        driver.find_element(By.TAG_NAME, "button").click()

        # Check if redirected to home and logged in
        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Hello, e2euser!", body_text)

        # Logout
        driver.find_element(By.LINK_TEXT, "Logout").click()
        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Sign up", body_text)

    def element_exists(self, by, value):
        """Helper to check if element exists"""
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False
