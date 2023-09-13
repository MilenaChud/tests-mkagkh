import random
from selenium.webdriver.common.by import By
from core.main.sections.organizations.organization_tabs_common import OrganizationTabsCommon


class OrganizationTabInformation(OrganizationTabsCommon):
    # Locators
    NAME = (By.XPATH, "//label[contains(text(), 'Наименование организации')]/..//input")
    AREAS_INPUT = (By.XPATH, "//label[contains(text(), 'Сферы ЖКХ')]/..//input")
    AREAS_LIST = (By.XPATH, "//label[contains(text(), 'Сферы ЖКХ')]/..//div")
    ADDRESS_INPUT = (By.XPATH, "//label[contains(text(), 'Адрес организации')]/..//input")
    ADDRESS_BUTTON_OPEN = (By.XPATH, "//label[contains(text(), 'Адрес организации')]/..//button")
    TYPES_INPUT = (By.XPATH, "//label[contains(text(), 'Тип организации')]/..//input")
    TYPES_LIST = (By.XPATH, "//label[contains(text(), 'Тип организации')]/..//div")
    EMERGENCY_ROLES_LIST = (By.XPATH, "//label[contains(text(), 'Роль организации')]/..//select")
    COORDINATORS_LIST = (By.XPATH, "//label[contains(text(), 'Согласующая организация')]/..//select")
    DUTY_PHONE = (By.XPATH, "//label[contains(text(), 'Телефон дежурной службы')]/..//input")
    TIN = (By.XPATH, "//label[contains(text(), 'ИНН организации')]/..//input")
    DESCRIPTION = (By.XPATH, "//label[contains(text(), 'Описание')]/..//textarea[1]")
    MESSAGE_CREATE_SUCCESS = (By.XPATH, "//div[contains(text(), 'Организация:') and "
                                        "contains(text(), 'успешно добавлена')]")

    def _generate_tin(self):
        tin = ""
        for i in range(1, 13):
            tin += random.choice("0123456789")
        return tin

    def fill_data(self, template: dict, save: bool):
        tin = self._generate_tin()
        name = f"{template['Name']}_{tin}"
        self._fill_input(locator=self.NAME, value=name)
        self._click_element(locator=self.AREAS_LIST)
        for element in template['Areas']:
            checkbox_locator = (By.XPATH, f"//div/span[contains(text(), '{element}')]/../..//span")
            self._click_element(locator=checkbox_locator)
        self._press_keyboard_key(key="TAB")
        self._add_address(open_form_locator=self.ADDRESS_BUTTON_OPEN, address=template['Address'])
        self._click_element(locator=self.TYPES_LIST)
        for element in template['Types']:
            checkbox_locator = (By.XPATH, f"//div/span[contains(text(), '{element}')]/../..//span")
            self._click_element(locator=checkbox_locator)
        self._press_keyboard_key(key="TAB")
        elements = self._click_element(locator=self.EMERGENCY_ROLES_LIST)
        self._select_option_by_text(selector=elements, text=template['EmergencyRole'])
        elements = self._click_element(locator=self.COORDINATORS_LIST)
        self._select_option_by_text(selector=elements, text=template['Coordinator'])
        self._fill_input(locator=self.DUTY_PHONE, value=template['DutyPhone'])
        self._fill_input(locator=self.TIN, value=tin)
        self._fill_input(locator=self.DESCRIPTION, value=template['Description'])

        if save:
            self._click_element(locator=self.BUTTON_SAVE)
        else:
            self._click_element(locator=self.BUTTON_BACK)
            self._click_element(locator=self.BUTTON_LEAVE)
        self._check_element_visible(locator=self.MESSAGE_CREATE_SUCCESS, visibility=save)
        return name
