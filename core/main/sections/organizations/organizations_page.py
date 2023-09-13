import allure
import time
from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper
from core.main.sections.organizations.organization_form import OrganizationForm


class OrganizationsPage(OrganizationForm):
    # Locators
    TITLE = (By.XPATH, "//h1[contains(text(), 'Реестр организаций')]")
    BUTTON_ADD = (By.XPATH, "//span[contains(text(), 'Добавить')]/parent::button")

    def _goto(self):
        if self._is_element_visible(locator=self.TITLE, visibility=False, timeout=3):
            self._open(added_path="DataProviders")
            with allure.step("Check organizations page title"):
                self._check_element_visible(locator=self.TITLE)
        return self

    def _smart_open(self, credentials: dict):
        self._auth.smart_login(credentials=credentials)
        self._goto()

    def _add_card(self, template: dict, save: bool):
        self._click_element(locator=self.BUTTON_ADD)
        name = self._tab_information.fill_data(template=template, save=save)
        return name
