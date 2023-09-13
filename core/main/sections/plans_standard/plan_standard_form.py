import time
from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper


class PlanStandardEventsForm(AppSectionsHelper):
    BUTTON_ADD = (By.XPATH, "//span[contains(text(), 'Добавить')]/parent::button")
    TITLE_CARD = (By.XPATH, "//h1[contains(text(), 'Карточка учета информации о типовом плане мероприятий')]")
    TYPE_EVENT = (By.XPATH, "//select[@id='typeSelect']")
    SPHERE_GKH = (By.XPATH, "//select[@id='sphereServiceSelect']")
    ACCOUNTING_SIGNS_BUTTON = (
        By.XPATH, "//label[contains(text(), 'Учетные признаки события')]/..//span[@class='MuiTouchRipple-root']")
    ACCOUNTING_SIGNS = (By.XPATH, "//label[contains(text(), 'Учетные признаки события')]/..//textarea")
    WINDOW_ACCOUNTING_SIGNS = (By.XPATH, "//h6[contains(text(), 'Учётные признаки события')]")
    RADIO_BUTTON = (
        By.XPATH, "//label[@class='MuiFormControlLabel-root']//span[contains(@class, 'MuiTypography-root')]")
    BUTTON_SAVE = (By.XPATH, "//div[@id='form-dialog-title']/..//span[contains(text(), 'Сохранить')]")
    NAME_EVENT = (By.XPATH, "//label[contains(text(), 'Наименование мероприятия')]/..//input")
    TYPE_PLAN_EVENT = (By.XPATH, "//div[@id='mui-component-select-type']")
    TYPE_PLAN_EVENT_INPUT = (By.XPATH, "//label[contains(text(), 'Тип плана мероприятия')]/..//input")
    TYPE_PLAN_EVENT_1 = (By.XPATH, "//ul[@role='listbox']//li")
    THINGS_FOR_EVENTS = (
        By.XPATH, "//label[contains(text(), 'Силы и средства, задействованные для проведения работ')]/..//input")
    SOURCES_FINANCE = (By.XPATH, "//label[contains(text(), 'Источники финансирования')]/..//input")
    PRICE_TASKS = (By.XPATH, "//label[contains(text(), 'Стоимость работ, тыс.руб')]/..//input")
    PERIOD_TIME = (By.XPATH, "//label[contains(text(), 'Плановый срок проведения мероприятия (в часах)')]/..//input")
    TITLE_EXTRA_STEP = (By.XPATH, "//h2[contains(text(), 'Добавить ')]")
    NAME_ITEM_EVENT = (By.XPATH, "//label[contains(text(), 'Наименование пункта мероприятия')]/..//input")
    MAIN_TITLE = (
        By.XPATH, "//h1[contains(text(), 'Типовые планы мероприятий по устранению последствий аварий и инцидентов')]")
    BUTTON_BACK = (By.XPATH, "//span[contains(text(), 'Назад')]")
    SAVE_CARD = (By.XPATH, "//span[contains(text(), 'Сохранить')]")
    NAME_EVENT_TITLE = (By.XPATH, "//div[contains(text(), 'Наименование мероприятия')]//div")
    BUTTON_EDITE = (By.XPATH, "//span[contains(text(), 'Редактировать')]")

    def _fill_plans(self, template: dict, save: bool = False):
        self._check_element_visible(locator=self.BUTTON_ADD)
        self._click_element(locator=self.BUTTON_ADD)
        self._check_element_visible(locator=self.TITLE_CARD)
        elements = self._find_element(self.TYPE_EVENT)
        self._select_option_by_text(selector=elements, text=template["TypeEvents"])
        elements = self._find_element(self.SPHERE_GKH)
        self._select_option_by_text(selector=elements, text=template["SphereGKH"])
        self._click_element(locator=self.ACCOUNTING_SIGNS_BUTTON)
        self._check_element_visible(locator=self.WINDOW_ACCOUNTING_SIGNS)
        self._check_element_visible(locator=self.RADIO_BUTTON)
        elements = self._find_elements_visible(locator=self.RADIO_BUTTON)
        element = self._get_element_by_text(elements=elements, text=template['AccountingSignsButton'])
        self._click_webelement(element=element)
        self._click_element(locator=self.BUTTON_SAVE)
        name_event = self._find_element(locator=self.NAME_EVENT)
        name_event.send_keys(template['NameEvent'])
        self._click_element(locator=self.TYPE_PLAN_EVENT)
        elements = self._find_elements_visible(locator=self.TYPE_PLAN_EVENT_1)
        element = self._get_element_by_text(elements=elements, text=template['TypePlanEvent'])
        self._click_webelement(element=element)
        things_for_events = self._find_element(locator=self.THINGS_FOR_EVENTS)
        things_for_events.send_keys(template['ThingsForEvent'])
        source_finance = self._find_element(locator=self.SOURCES_FINANCE)
        source_finance.send_keys(template['SourceFinance'])
        price_tasks = self._find_element(locator=self.PRICE_TASKS)
        price_tasks.send_keys(template['PriceTasks'])
        period_time = self._find_element(locator=self.PERIOD_TIME)
        period_time.send_keys(template['PeriodTime'])
        self._click_element(locator=self.BUTTON_ADD)
        self._check_element_visible(locator=self.TITLE_EXTRA_STEP)
        name_item_event = self._find_element(locator=self.NAME_ITEM_EVENT)
        name_item_event.send_keys(template['NameItemEvent'])
        self._click_element(locator=self.BUTTON_SAVE)
        self._press_keyboard_key(key="PAGE DOWN")
        if save:
            self._click_element(locator=self.SAVE_CARD)
            self._check_element_visible(locator=self.MAIN_TITLE)
        else:
            self._click_element(locator=self.BUTTON_BACK)
            self._check_element_visible(locator=self.MAIN_TITLE)

    def _check_tab(self, template):
        self._filter_by_feature(filter_type='sphere_gkh', template=template)
        elements = self._find_elements_visible(locator=self.NAME_EVENT_TITLE)
        element = self._get_element_by_text(elements=elements, text=template['NameEvent'])
        self._click_element(locator=element)
        self._check_element_value(locator=self.TYPE_EVENT, value=template['TypeEventsSelect'])
        sphere_gkh = self._get_element_attribute(locator=self.SPHERE_GKH, attr_name="value")
        assert self.Areas[sphere_gkh] == template['SphereGKH']
        element = self._find_element(locator=self.ACCOUNTING_SIGNS)
        assert element.text == template['AccountingSignsButton']
        self._check_element_value(locator=self.NAME_EVENT, value=template['NameEvent'])
        self._check_element_value(locator=self.TYPE_PLAN_EVENT_INPUT, value=template['TypePlanEventInput'])
        self._check_element_value(locator=self.THINGS_FOR_EVENTS, value=template['ThingsForEvent'])
        self._check_element_value(locator=self.PRICE_TASKS, value=template['PriceTasks'])
        self._check_element_value(locator=self.SOURCES_FINANCE, value=template['SourceFinance'])
        self._check_element_value(locator=self.PERIOD_TIME, value=template['PeriodTime'])

    def _edite_card(self, template: dict):
        self._click_element(locator=self.BUTTON_EDITE)
        source_finance = self._find_element(locator=self.SOURCES_FINANCE)
        self._click_webelement(element=source_finance)
        self._press_keyboard_key(key="CTRL + A, DEL")
        source_finance.send_keys(template['SourceFinanceChange'])
        things_for_events = self._find_element(locator=self.THINGS_FOR_EVENTS)
        self._click_webelement(element=things_for_events)
        self._press_keyboard_key(key="CTRL + A, DEL")
        things_for_events.send_keys(template['ThingsForEventChange'])
        self._click_element(self.SAVE_CARD)
        self._check_element_value(locator=self.SOURCES_FINANCE, value=template['SourceFinanceChange'])
        self._check_element_value(locator=self.THINGS_FOR_EVENTS, value=template['ThingsForEventChange'])
