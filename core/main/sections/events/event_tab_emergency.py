import time
from selenium.webdriver.common.by import By
from core.main.sections.events.event_tabs_common import EventTabsCommon


class EventTabEmergency(EventTabsCommon):
    # Locators
    MUNICIPALITY_INPUT = (By.XPATH, "//label[contains(text(), 'Муниципальное образование')]/..//input")
    MUNICIPALITY_TEXT = (By.XPATH, "//label[contains(text(), 'Муниципальное образование')]/.."
                                   "//div[@role='button']/span")
    SCALE_TEXTAREA = (By.XPATH, "//label[contains(text(), 'Характер ЧС')]/..//textarea[@rows='1']")
    SCALE_BUTTON_OPEN = (By.XPATH, "//label[contains(text(), 'Характер ЧС')]/..//button")
    SCALE_TITLE = (By.XPATH, "//h2[contains(text(), 'Выберите характер ЧС')]")
    SCALE_BUTTON_CANCEL = (By.XPATH, "//h2[contains(text(), 'Выберите характер ЧС')]/../.."
                                     "//span[contains(text(), 'Отмена')]/parent::button")
    SCALE_BUTTON_SAVE = (By.XPATH, "//h2[contains(text(), 'Выберите характер ЧС')]/../.."
                                   "//span[contains(text(), 'Сохранить')]/parent::button")
    SCALES_LIST = (By.XPATH, "//div[@role='radiogroup']//label[contains(text(), 'Наименование')]/parent::div")
    ZONE = (By.XPATH, "//label[contains(text(), 'Границы зоны ЧС')]/..//input")
    REASONS = (By.XPATH, "//label[contains(text(), 'Описание причин и оснований введения режима ЧС')]/..//input")
    DATE_TIME_ON = (By.XPATH, "//label[contains(text(), 'Дата, время введения режима ЧС')]/..//input")
    DATE_TIME_OFF = (By.XPATH, "//label[contains(text(), 'Дата, время снятия режима ЧС')]/..//input")
    DATE_TIME_CONFIRM = (By.XPATH, "//span[contains(text(), 'OK')]/parent::button")
    AUTHORITY_ON = (By.XPATH, "//label[contains(text(), 'Уполномоченный орган, принявший решение о введении ЧС')]/.."
                              "//select")
    AUTHORITY_OFF = (By.XPATH, "//label[contains(text(), 'Уполномоченный орган, принявший решение о снятии ЧС')]/.."
                               "//select")
    RESOLUTION_ON = (By.XPATH, "//label[contains(text(), 'Распоряжение/постановление о введении режима ЧС')]/..//input")
    RESOLUTION_BUTTON_ON = (By.XPATH, "//label[contains(text(), 'Распоряжение/постановление о введении режима ЧС')]/.."
                                      "//span[contains(text(), 'Выбрать')]/parent::button")
    RESOLUTIONS_ON_TITLE = (By.XPATH, "//h2//div[contains(text(), 'Распоряжение/постановление о введении режима ЧС')]")
    RESOLUTION_OFF = (By.XPATH, "//label[contains(text(), 'Распоряжение/постановление о снятии режима ЧС')]/..//input")
    RESOLUTION_BUTTON_OFF = (By.XPATH, "//label[contains(text(), 'Распоряжение/постановление о снятии режима ЧС')]/.."
                                       "//span[contains(text(), 'Выбрать')]/parent::button")
    RESOLUTIONS_OFF_TITLE = (By.XPATH, "//h2//div[contains(text(), 'Распоряжение/постановление о снятии режима ЧС')]")
    RESOLUTIONS_NAMES = (By.XPATH, "//div[@class='solo_Card_wrapper__description__info_text']")
    PLANS = (By.XPATH, "//label[contains(text(), 'Планы мероприятий')]/..//input")
    PLAN_BUTTON_ADD = (By.XPATH, "//label[contains(text(), 'Планы мероприятий')]/../.."  # TODO: Проверить поведение данной кнопки 
                                 "//span[contains(text(), 'Добавить')]/parent::button")
    EVENT_STATUS = (By.XPATH, "//label[contains(text(), 'Статус карточки ЧС')]/..//input")

    def _check_elements_editable(self, disabled: bool):
        self._check_element_editable(locator=self.MUNICIPALITY_INPUT, disabled=disabled)
        self._check_element_editable(locator=self.SCALE_TEXTAREA, disabled=True)
        self._check_element_editable(locator=self.SCALE_BUTTON_OPEN, disabled=disabled)
        self._check_element_editable(locator=self.ZONE, disabled=disabled)
        self._check_element_editable(locator=self.REASONS, disabled=disabled)
        self._check_element_editable(locator=self.DATE_TIME_ON, disabled=disabled)
        # self._check_element_editable(locator=self.DATE_TIME_OFF, disabled=disabled)
        self._check_element_editable(locator=self.AUTHORITY_ON, disabled=disabled)
        # self._check_element_editable(locator=self.AUTHORITY_OFF, disabled=disabled)
        self._check_element_editable(locator=self.RESOLUTION_ON, disabled=True)
        # self._check_element_editable(locator=self.RESOLUTION_OFF, disabled=True)
        self._check_element_editable(locator=self.RESOLUTION_BUTTON_ON, disabled=disabled)
        # self._check_element_editable(locator=self.RESOLUTION_BUTTON_OFF, disabled=disabled)
        self._check_element_editable(locator=self.PLANS, disabled=True)
        self._check_element_editable(locator=self.EVENT_STATUS, disabled=True)

    def _get_data(self):
        if self._is_element_visible(locator=self.MUNICIPALITY_TEXT, timeout=3):
            _municipality = self._find_element(locator=self.MUNICIPALITY_TEXT).text
        else:
            _municipality = ""
        _scale = self._find_element(locator=self.SCALE_TEXTAREA).text
        _zone = self._get_element_attribute(locator=self.ZONE, attr_name="value")
        _reasons = self._get_element_attribute(locator=self.REASONS, attr_name="value")
        _date_time_on = self._get_element_attribute(locator=self.DATE_TIME_ON, attr_name="value")
        _date_time_off = self._get_element_attribute(locator=self.DATE_TIME_OFF, attr_name="value")
        _authority_on = self._get_selected_option(select_locator=self.AUTHORITY_ON)['Text']
        _authority_off = self._get_selected_option(select_locator=self.AUTHORITY_OFF)['Text']
        _resolution_on = self._get_element_attribute(locator=self.RESOLUTION_ON, attr_name="value")
        _resolution_off = self._get_element_attribute(locator=self.RESOLUTION_OFF, attr_name="value")
        _plans = self._get_element_attribute(locator=self.PLANS, attr_name="value")
        _status = self._get_element_attribute(locator=self.EVENT_STATUS, attr_name="value")
        data = {
            "Municipality": _municipality,
            "Scale": _scale,
            "Zone": _zone,
            "Reasons": _reasons,
            "EmergencyOn":
            {
                 "DateTime": _date_time_on,
                 "Authority": _authority_on,
                 "Resolution": _resolution_on
            },
            "EmergencyOff":
            {
                "DateTime": _date_time_off,
                "Authority": _authority_off,
                "Resolution": _resolution_off
            },
            "Plans": _plans,
            "Status": _status
        }
        return data

    def _fill_data(self, template: dict, save: bool):
        self._check_buttons(edit=False)
        self._check_elements_editable(disabled=True)
        self._press_keyboard_key(key="PAGE UP")
        self._click_element(locator=self.BUTTON_EDIT)
        self._check_buttons(edit=True)
        self._check_elements_editable(disabled=False)
        result = self._get_data()
        self._fill_input_by_symbols(locator=self.MUNICIPALITY_INPUT, value=template['Municipality'])
        self._press_keyboard_key(key="DOWN, ENTER")
        self._click_element(locator=self.SCALE_BUTTON_OPEN)
        self._check_element_visible(locator=self.SCALE_TITLE)
        elements = self._find_elements_visible(locator=self.SCALES_LIST)
        element = self._get_element_by_text(elements=elements, text=template['Scale'])
        self._click_webelement(element=element)
        self._click_element(locator=self.SCALE_BUTTON_SAVE)
        self._check_element_visible(locator=self.SCALE_TITLE, visibility=False)
        self._fill_input(locator=self.ZONE, value=template['Zone'])
        self._fill_input(locator=self.REASONS, value=template['Reasons'])
        self._click_element(locator=self.DATE_TIME_ON)
        self._click_element(locator=self.DATE_TIME_CONFIRM)
        elements = self._click_element(locator=self.AUTHORITY_ON)
        self._select_option_by_text(selector=elements, text=template['EmergencyOn']['Authority'])
        self._click_element(locator=self.RESOLUTION_BUTTON_ON)
        self._check_element_visible(locator=self.RESOLUTIONS_ON_TITLE)
        elements = self._find_elements_visible(locator=self.RESOLUTIONS_NAMES)
        element = self._get_element_by_text(elements=elements, text=template['EmergencyOn']['Resolution'])
        self._click_webelement(element=element)
        if save:
            result = self._get_data()
            element = self._check_element_visible(locator=self.BUTTON_SAVE)
        else:
            element = self._check_element_visible(locator=self.BUTTON_CANCEL)
        self._press_keyboard_key(key="PAGE DOWN")
        self._click_webelement(element=element)
        # TODO: Похоже сообщения об успешности сохранения данных нет в интерфейсе - разобраться
        # self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=save)
        self._check_buttons(edit=False)
        self._check_elements_editable(disabled=True)

        time.sleep(1)  # Для гарантированного сохранения данных TODO: Возможно надо будет поискать другое решение
        return result
