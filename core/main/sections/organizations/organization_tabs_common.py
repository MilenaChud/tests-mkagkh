from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper


class OrganizationTabsCommon(AppSectionsHelper):
    # Locators
    BUTTON_EDIT = (By.XPATH, "//div[@class='action-buttons']//span[contains(text(), 'Редактировать')]/parent::button")
    BUTTON_BACK = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Назад')]/parent::button")
    BUTTON_CANCEL = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Отмена')]/parent::button")
    BUTTON_SAVE = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Сохранить')]/parent::button")
    BUTTON_LEAVE = (By.XPATH, "//span[contains(text(), 'Уйти со страницы')]/parent::button")
    BUTTON_RETURN = (By.XPATH, "//span[contains(text(), 'Вернуться')]/parent::button")

    # TODO: Проверка состояния кнопок
