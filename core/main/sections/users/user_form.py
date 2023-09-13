import allure
from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper
from core.main.sections.users.users_page import UsersPage


class UserForm(AppSectionsHelper):
    # Locators
    TITLE_ADD_USER = (By.XPATH, "//h6[contains(text(), 'Добавление пользователя')]")
    TITLE_ADD_SUPERUSER = (By.XPATH, "//h6[contains(text(), 'Добавление суперпользователя')]")
    TITLE_UPDATE_USER = (By.XPATH, "//h6[contains(text(), 'Редактирование пользователя')]")
    LOGIN = (By.XPATH, "//label[contains(text(), 'Логин пользователя')]/..//input")
    ROLES_TITLE = (By.XPATH, "//label[contains(text(), 'Роли пользователя')]/../div/div/div")
    ROLES_LIST = (By.XPATH, "//div[@id='menu-']/div[3]/ul/li")
    EMAIL = (By.XPATH, "//label[contains(text(), 'Email')]/..//input")
    EMAIL_CONFIRM = (By.XPATH, "//span[contains(text(), 'Email подтвержден')]")
    LAST_NAME = (By.XPATH, "//label[contains(text(), 'Фамилия')]/..//input")
    FIRST_NAME = (By.XPATH, "//label[contains(text(), 'Имя')]/..//input")
    MIDDLE_NAME = (By.XPATH, "//label[contains(text(), 'Отчество')]/..//input")
    ORGANIZATION = (By.XPATH, "//label[contains(text(), 'Организация')]/..//span")
    ORGANIZATIONS_TITLE = (By.XPATH, "//h1[contains(text(), 'Реестр организаций')]")
    ORGANIZATIONS_LIST = (By.XPATH, "//div[contains(text(), 'Наименование организации')]/div")
    POSITION = (By.XPATH, "//label[contains(text(), 'Должность')]/..//input")
    PHONE = (By.XPATH, "//label[contains(text(), 'Телефон')]/..//input")
    MOBILE_PHONE = (By.XPATH, "//label[contains(text(), 'Моб. телефон')]/..//input")
    PASSWORD = (By.XPATH, "//label[contains(text(), 'Пароль')]/..//input")
    PASSWORD_CONFIRM = (By.XPATH, "//label[contains(text(), 'Подтверждение пароля')]/..//input")
    BUTTON_CLOSE = (By.XPATH, "//button[@aria-label='close']")
    BUTTON_CANCEL = (By.XPATH, "//span[contains(text(), 'Отмена')]/parent::button")
    BUTTON_SAVE = (By.XPATH, "//span[contains(text(), 'Сохранить')]/parent::button")
    MESSAGE_CREATE_SUCCESS = (By.XPATH, "//div[contains(text(), 'Пользователь успешно создан')]")
    MESSAGE_UPDATE_SUCCESS = (By.XPATH, "//div[contains(text(), 'Данные о пользователе успешно обновлены')]")

    def _modify_template_data(self, template: dict, superuser: bool = False):
        date_time_key = self._get_date_time_key()
        result = dict(template)
        result['Username'] += f"_{date_time_key}"
        result['LastName'] += f"_{date_time_key}"
        email = result['Email'].split("@")
        result['Email'] = f"{email[0]}_{date_time_key}@{email[1]}"
        if not superuser:
            result['FullName'] = f"{result['LastName']} {result['FirstName']} {result['MiddleName']}"
            result['UserExists'] = True
        return result

    def _close(self):
        if self._is_element_visible(locator=self.BUTTON_CLOSE, visibility=True, timeout=3):
            self._click_element(locator=self.BUTTON_CLOSE)

    def _fill_data(self, template: dict, save: bool, superuser: bool = False):
        if not superuser:
            self._click_element(locator=UsersPage.BUTTON_ADD_USER)
            self._check_element_visible(locator=self.TITLE_ADD_USER)
            self._fill_input(locator=self.LOGIN, value=template['Username'])
            self._click_element(locator=self.ROLES_TITLE)
            elements = self._find_elements_visible(locator=self.ROLES_LIST)
            element = self._get_element_by_text(elements=elements, text=template['Role'])
            self._click_webelement(element=element)
            self._press_keyboard_key(key="TAB")
        else:
            self._click_element(locator=UsersPage.BUTTON_ADD_SUPERUSER)
            self._check_element_visible(locator=self.TITLE_ADD_SUPERUSER)
            self._fill_input(locator=self.LOGIN, value=template['Username'])
        self._fill_input(locator=self.EMAIL, value=template['Email'])
        self._click_element(locator=self.EMAIL_CONFIRM)
        self._fill_input(locator=self.LAST_NAME, value=template['LastName'])
        self._fill_input(locator=self.FIRST_NAME, value=template['FirstName'])
        self._fill_input(locator=self.MIDDLE_NAME, value=template['MiddleName'])
        if not superuser:
            self._click_element(locator=self.ORGANIZATION)
            self._check_element_visible(locator=self.ORGANIZATIONS_TITLE)
            elements = self._find_elements_visible(locator=self.ORGANIZATIONS_LIST)
            element = self._get_element_by_text(elements=elements, text=template['Organization'])
            self._click_webelement(element=element)
            self._check_element_visible(locator=self.TITLE_ADD_USER)
            self._fill_input(locator=self.POSITION, value=template['Position'])
        self._fill_input(locator=self.PHONE, value=template['Phone'])
        self._fill_input(locator=self.MOBILE_PHONE, value=template['MobilePhone'])
        self._fill_input(locator=self.PASSWORD, value=template['Password'])
        self._fill_input(locator=self.PASSWORD_CONFIRM, value=template['Password'])
        if save:
            self._click_element(locator=self.BUTTON_SAVE)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
        self._check_element_visible(locator=self.MESSAGE_CREATE_SUCCESS, visibility=save)
        self._check_element_visible(locator=UsersPage.TITLE)

    def _set_organization(self, name: str):
        self._check_element_visible(locator=self.TITLE_UPDATE_USER)
        self._click_element(locator=self.ORGANIZATION)
        self._check_element_visible(locator=self.ORGANIZATIONS_TITLE)
        elements = self._find_elements_visible(locator=self.ORGANIZATIONS_LIST)
        element = self._get_element_by_text(elements=elements, text=name)
        self._click_webelement(element=element)
        self._check_element_visible(locator=self.TITLE_UPDATE_USER)
        self._click_element(locator=self.BUTTON_SAVE)
        self._check_element_visible(locator=self.MESSAGE_UPDATE_SUCCESS)
        self._check_element_visible(locator=UsersPage.TITLE)
