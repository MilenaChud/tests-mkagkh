import allure
from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper


class DocumentsNPAPage(AppSectionsHelper):
    TITLE = (By.XPATH, "//h1[contains(text(), 'Реестр справочных документов и НПА')]")
    BUTTON_ADD = (By.XPATH, "//span[contains(text(), 'Добавить')]/parent::button")

    def _goto(self):
        if self._is_element_visible(locator=self.TITLE, visibility=False, timeout=3):
            self._open(added_path="ReferenceDocuments")
            with allure.step("Check plans page title"):
                self._check_element_visible(locator=self.TITLE)
        return self

    def _smart_open(self, credentials: dict):
        self._auth.smart_login(credentials=credentials)
        self._goto()
