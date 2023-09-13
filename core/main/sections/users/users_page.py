from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper
import allure


class UsersPage(AppSectionsHelper):
    # Locators
    TITLE = (By.XPATH, "//h1[contains(text(), 'Пользователи')]")
    USERS_TABLE_EMPTY = (By.XPATH, "//tbody/tr/td[contains(text(), 'Данных не найдено')]")
    BUTTON_ADD_USER = (By.XPATH, "//span[contains(text(), 'Добавить')]/parent::button")
    BUTTON_ADD_SUPERUSER = (By.XPATH, "//span[contains(text(), 'Добавить суперпользователя')]/parent::button")

    def _goto(self):
        with allure.step("Check users page title"):
            if self._is_element_visible(locator=self.TITLE, visibility=False, timeout=3):
                self._open(added_path="users")
                self._check_element_visible(locator=self.TITLE)

        with allure.step("Check users page data"):
            self._check_element_visible(locator=self.USERS_TABLE_EMPTY, visibility=False, timeout=15)

        return self

    def _smart_open(self, credentials: dict, execute: bool = True):
        if execute:
            self._auth.smart_login(credentials=credentials)
            self._goto()
