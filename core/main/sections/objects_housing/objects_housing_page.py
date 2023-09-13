import allure
from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper


class ObjectsHousingPage(AppSectionsHelper):
    # Locators
    TITLE = (By.XPATH, "//h1[contains(text(), 'Реестр объектов жилищного фонда')]")
    BUTTON_ADD = (By.XPATH, "//span[contains(text(), 'Добавить')]/parent::button")
    OBJECTS_NAMES = (By.XPATH, "//span[contains(text(), 'Наименование объекта')]/parent::div")
    OBJECT_TITLE = (By.XPATH, "//h1[contains(text(), 'Карточка объекта жилищного фонда')]")

    def _goto(self):
        if self._is_element_visible(locator=self.TITLE, visibility=False, timeout=3):
            self._open(added_path="LifeObjects")
            with allure.step("Check objects page title"):
                self._check_element_visible(locator=self.TITLE)
        return self

    def _smart_open(self, credentials: dict):
        self._auth.smart_login(credentials=credentials)
        self._goto()
