import allure
from datetime import datetime
from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper
from core.main.sections.events.events_page import EventsPage


class EventFormStart(AppSectionsHelper):
    # Locators
    TITLE_ADD = (By.XPATH, "//h6[contains(text(), 'Добавить событие')]")
    AREAS_LIST = (By.XPATH, "//label[contains(text(), 'Сфера ЖКХ')]/..//select")
    DATE_TIME = (By.XPATH, "//label[contains(text(), 'Дата и время')]/..//input")
    DATE_TIME_CONFIRM = (By.XPATH, "//span[contains(text(), 'OK')]/parent::button")
    ADDRESS_INPUT = (By.XPATH, "//label[contains(text(), 'Адрес события')]/..//input")
    ADDRESS_BUTTON_OPEN = (By.XPATH, "//label[contains(text(), 'Адрес события')]/..//button")
    SOURCES_LIST = (By.XPATH, "//label[contains(text(), 'Источник первичной информации')]/..//select")
    DESCRIPTION = (By.XPATH, "//label[contains(text(), 'Краткое описание события')]/..//input")
    BUTTON_CANCEL = (By.XPATH, "//span[contains(text(), 'Отмена')]/parent::button")
    BUTTON_SAVE = (By.XPATH, "//span[contains(text(), 'Сохранить')]/parent::button")

    def _get_data(self):
        _area = self._get_element_attribute(locator=self.AREAS_LIST, attr_name="value")
        _date_time = self._get_element_attribute(locator=self.DATE_TIME, attr_name="value")
        _address = self._get_element_attribute(locator=self.ADDRESS_INPUT, attr_name="value")
        _source = self._get_element_attribute(locator=self.SOURCES_LIST, attr_name="value")
        _description = self._get_element_attribute(locator=self.DESCRIPTION, attr_name="value")
        data = {
            "Area": _area,
            "DateTime": _date_time,
            "Address": _address,
            "Source": _source,
            "Description": _description
        }
        return data

    def _fill_data(self, template: dict, save: bool):
        self._click_element(locator=EventsPage.BUTTON_ADD)
        self._check_element_visible(locator=self.TITLE_ADD)
        elements = self._click_element(locator=self.AREAS_LIST)
        self._select_option_by_text(selector=elements, text=template['Area'])
        # TODO: Fill date-time field with string in format "day-month-year hours:minutes:seconds"
        self._click_element(locator=self.DATE_TIME)
        date_time = self._get_element_attribute(locator=self.DATE_TIME, attr_name="value")
        date_time = f"{date_time}:{datetime.now().second:02d}"
        date_time_key = f"{date_time[6:10]}{date_time[3:5]}{date_time[0:2]}_" \
                        f"{date_time[11:13]}{date_time[14:16]}{date_time[17:19]}"
        self._click_element(locator=self.DATE_TIME_CONFIRM)
        # TODO: Check map opening by pressing button "Указать на карте"
        self._add_address(open_form_locator=self.ADDRESS_BUTTON_OPEN, address=template['Address'])
        elements = self._click_element(locator=self.SOURCES_LIST)
        self._select_option_by_text(selector=elements, text=template['Source'])
        description = f"{template['Description']}_{date_time_key}"
        self._fill_input(locator=self.DESCRIPTION, value=description)
        if save:
            self._click_element(locator=self.BUTTON_SAVE)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
        self._check_element_visible(locator=EventsPage.TITLE)
        return description
