import time
from selenium.webdriver.common.by import By
from core.main.sections.events.event_tabs_common import EventTabsCommon


class EventTabObject(EventTabsCommon):
    # Locators
    BUTTON_CHOOSE = (By.XPATH, "//span[contains(text(), 'Выбрать из списка')]/parent::button")
    STAGE = (By.XPATH, "//label[contains(text(), 'Этап')]/..//input")
    KIND = (By.XPATH, "//label[contains(text(), 'Объект')]/..//input")
    TYPE = (By.XPATH, "//label[contains(text(), 'Тип объекта')]/..//input")
    NAME = (By.XPATH, "//label[contains(text(), 'Наименование объекта')]/..//input")
    ADDRESS = (By.XPATH, "//label[contains(text(), 'Адрес объекта')]/..//input")
    OWNER = (By.XPATH, "//label[contains(text(), 'Информация о собственнике объекта')]/..//input")
    OPERATOR = (By.XPATH, "//label[contains(text(), 'Информация об эксплуатирующей организации')]/..//input")

    def _check_buttons(self, edit: bool):
        super()._check_buttons(edit=edit)
        if edit:
            self._check_element_visible(locator=self.BUTTON_CHOOSE, visibility=True)
            self._check_element_editable(locator=self.BUTTON_CHOOSE, disabled=False)
        else:
            self._check_element_visible(locator=self.BUTTON_CHOOSE, visibility=True)
            self._check_element_editable(locator=self.BUTTON_CHOOSE, disabled=True)

    def _check_elements_editable(self, disabled: bool):
        self._check_element_editable(locator=self.STAGE, disabled=disabled)
        self._check_element_editable(locator=self.KIND, disabled=disabled)
        self._check_element_editable(locator=self.TYPE, disabled=disabled)
        self._check_element_editable(locator=self.NAME, disabled=disabled)
        self._check_element_editable(locator=self.ADDRESS, disabled=disabled)
        self._check_element_editable(locator=self.OWNER, disabled=disabled)
        self._check_element_editable(locator=self.OPERATOR, disabled=disabled)

    def _get_data(self):
        _stage = self._get_element_attribute(locator=self.STAGE, attr_name="value")
        _kind = self._get_element_attribute(locator=self.KIND, attr_name="value")
        _type = self._get_element_attribute(locator=self.TYPE, attr_name="value")
        _name = self._get_element_attribute(locator=self.NAME, attr_name="value")
        _address = self._get_element_attribute(locator=self.ADDRESS, attr_name="value")
        _owner = self._get_element_attribute(locator=self.OWNER, attr_name="value")
        _operator = self._get_element_attribute(locator=self.OPERATOR, attr_name="value")
        data = {
            "Stage": _stage,
            "Kind": _kind,
            "Type": _type,
            "Name": _name,
            "Address": _address,
            "Owner": _owner,
            "Operator": _operator
        }
        return data

    def _check_data(self, template: dict):
        self._check_element_value(locator=self.STAGE, value=template['Stage'])
        self._check_element_value(locator=self.KIND, value=template['Kind'])
        self._check_element_value(locator=self.TYPE, value=template['Type'])
        self._check_element_value(locator=self.NAME, value=template['Name'])
        self._check_element_value(locator=self.ADDRESS, value=template['Address'])
        self._check_element_value(locator=self.OWNER, value=template['Owner'])
        self._check_element_value(locator=self.OPERATOR, value=template['Operator'])

    def _fill_data(self, template: dict, save: bool):
        self._check_buttons(edit=False)
        self._check_elements_editable(disabled=True)
        self._press_keyboard_key(key="PAGE UP")
        self._click_element(locator=self.BUTTON_EDIT)
        self._check_buttons(edit=True)
        self._check_elements_editable(disabled=True)
        self._click_element(locator=self.BUTTON_CHOOSE)
        self._open_card_by_key(key=template['Name'], into="event_card")
        if save:
            element = self._check_element_visible(locator=self.BUTTON_SAVE)
        else:
            element = self._check_element_visible(locator=self.BUTTON_CANCEL)
        self._press_keyboard_key(key="PAGE DOWN")
        self._click_webelement(element=element)
        self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=save)
        self._check_buttons(edit=False)
        self._check_elements_editable(disabled=True)
        time.sleep(1)  # Для гарантированного сохранения данных TODO: Возможно надо будет поискать другое решение
