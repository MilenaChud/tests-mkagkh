from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper


class EventTabsCommon(AppSectionsHelper):
    # Locators
    BUTTON_EDIT = (By.XPATH, "//div[@class='action-buttons']//span[contains(text(), 'Редактировать')]/parent::button")
    BUTTON_BACK = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Назад')]/parent::button")
    BUTTON_CANCEL = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Отмена')]/parent::button")
    BUTTON_SAVE = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Сохранить')]/parent::button")
    MESSAGE_SAVE_SUCCESS = (By.XPATH, "//div[contains(text(), 'Сохранено успешно')]")

    def _check_buttons(self, edit: bool):
        if edit:
            self._check_element_visible(locator=self.BUTTON_EDIT, visibility=True)
            self._check_element_editable(locator=self.BUTTON_EDIT, disabled=True)
            self._check_element_visible(locator=self.BUTTON_BACK, visibility=False)
            self._check_element_visible(locator=self.BUTTON_CANCEL, visibility=True)
            self._check_element_editable(locator=self.BUTTON_CANCEL, disabled=False)
            self._check_element_visible(locator=self.BUTTON_SAVE, visibility=True)
            self._check_element_editable(locator=self.BUTTON_SAVE, disabled=False)
        else:
            self._check_element_visible(locator=self.BUTTON_EDIT, visibility=True)
            self._check_element_editable(locator=self.BUTTON_EDIT, disabled=False)
            self._check_element_visible(locator=self.BUTTON_BACK, visibility=True)
            self._check_element_editable(locator=self.BUTTON_BACK, disabled=False)
            self._check_element_visible(locator=self.BUTTON_CANCEL, visibility=False)
            self._check_element_visible(locator=self.BUTTON_SAVE, visibility=True)
            self._check_element_editable(locator=self.BUTTON_SAVE, disabled=True)
