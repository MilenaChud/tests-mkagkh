import time

import allure
from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper


class ObjectHousingForm(AppSectionsHelper):
    # Locators
    TITLE = (By.XPATH, "//h1[contains(text(), 'Карточка объекта жилищного фонда')]")
    BUTTON_ADD = (By.XPATH, "//span[contains(text(), 'Добавить')]/parent::button")
    ADDRESS_BUTTON_OPEN = (By.XPATH, "//label[contains(text(), 'Адрес местоположения объекта')]/..//button")
    ADDRESS = (By.XPATH, "//label[contains(text(), 'Адрес местоположения объекта')]/..//input")
    TYPE = (By.XPATH, "//label[contains(text(), 'Тип объекта')]/..//select")
    BUTTON_GET_DATA = (By.XPATH, "//span[contains(text(), 'Получить данные из ГИС')]/parent::button")
    STAGE_LIVING_CYCLE = (By.XPATH, "//label[contains(text(), 'Стадия жизненного цикла')]/..//select")
    YEAR_OF_CONSTRUCTION = (By.XPATH, "//label[contains(text(), 'Год постройки')]/..//input")
    FLOORS = (By.XPATH, "//label[contains(text(), 'Количество этажей ')]/..//input")
    SAVE_CARD = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Сохранить')]")
    BUTTON_BACK = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Назад')]")
    MAIN_TITLE = (By.XPATH, "//h1[contains(text(), 'Реестр объектов жилищного фонда')]")
    CARD = (By.XPATH, "//./../..//div[@data-testid='card-click']")
    BUTTON_NEXT = (By.XPATH, "//button[@type='button']/span[contains(text(), 'Далее')]")
    EDITE = (By.XPATH, "//span[contains(text(), 'Редактировать')]")
    BUTTON_CHECK_FROM_LIST = (By.XPATH,
                              "//label[contains(text(), 'Эксплуатирующие организации')]/../../../..//span[contains(text(), 'Выбрать из списка')]")
    BUTTON_CHECK_FROM_LIST_2 = (By.XPATH, "//label[contains(text(), 'Связанные объекты ЖКХ')]/../../../..//span[contains(text(), 'Выбрать из списка')]")
    BUTTON_OPEN_MANAGE_COMPANY = (By.XPATH, "//label[contains(text(), 'Выбрать управляющую организацию')]/..//span[@class='MuiTouchRipple-root']")
    TABLE_EXPLOATE_ORGANISATION = (By.XPATH,
                                   "//label[contains(text(), 'Эксплуатирующие организации')]/../../../..//td[contains(text(), 'Данных не найдено')]")
    BUTTON_CANCEL = (By.XPATH, "//button[@type='button']/span[contains(text(), 'Отмена')]")
    SWITCH_TAB_INF = (By.XPATH, "//span[contains(text(), 'Сведения об обслуживании')]")
    LIVING_OBJECT = (By.XPATH, "//span[contains(text(), 'Объект жилищного фонда')]")
    TYPE_GAS_SUPPLY = (By.XPATH, "//label[contains(text(), 'Тип газоснабжения')]/..//select")
    TYPE_MANAGE = (By.XPATH, "//label[contains(text(), 'Способ управления многоквартирным домом')]/..//select")
    TYPE_NUMBER = (By.XPATH, "//label[contains(text(), 'Серия, тип постройки здания')]/..//input")
    COUNT_HALLS = (By.XPATH, "//label[contains(text(), 'Количество подъездов')]/..//input")
    COUNT_ELEVATOR = (By.XPATH, "//label[contains(text(), 'Количество лифтов')]/..//input")
    COUNT_APARTMENTS = (By.XPATH, "//label[contains(text(), 'Количество квартир')]/..//input")
    COUNT_PEOPLE = (By.XPATH, "//label[contains(text(), 'Число жителей')]/..//input")
    CHANGE_TABLE = (By.XPATH, "//h2[contains(text(), 'Введенные вами данные не совпадают с данными о доме в Реформе ЖКХ. Настройте синхронизацию данных.')]")
    TABLE_ROWS = (By.XPATH, "//p[contains(text(), 'Несовпадающие поля')]/..//tbody/tr")
    RADIO_BUTTON = (By.XPATH, "//p[contains(text(), 'Несовпадающие поля')]/..//td[4]//span[contains(@class, 'MuiTouchRipple-root')]")
    TABLE = (By.XPATH, "//div[@class='ant-table-content']")

    LivingCycle = {
        "11": "Строящийся",
        "12": "Эксплуатируемый",
        "13": "Выведенный из эксплуатации",
        "14": "Снесенный"
    }

    TypesObjects = {
        "15": "Многоквартирный дом",
        "16": "Жилой дом блокированной застройки",
        "17": "Специализированный объект жилищного фонда",
        "18": "Не заполнено",
        "19": "Жилой дом (индивидуально-определенное здание)"
    }

    def _get_data(self):
        _address = self._get_element_attribute(locator=self.ADDRESS, attr_name="value")
        _type = self._get_element_attribute(locator=self.TYPE, attr_name="value")
        _amount_of_floors = self._get_element_attribute(locator=self.FLOORS, attr_name="value")
        _stage_living_cycle = self._get_element_attribute(locator=self.STAGE_LIVING_CYCLE, attr_name="value")
        _year_of_construction = self._get_element_attribute(locator=self.YEAR_OF_CONSTRUCTION, attr_name="value")
        data = {
            "Address": _address,
            "Type": _type,
            "Amount_of_floors": _amount_of_floors,
            "Stage_living_cycle": _stage_living_cycle,
            "Year_of_construction": _year_of_construction
        }
        return data

    def _fill_new_card_object(self, template: dict, save: bool, double: bool):
        self._click_element(locator=self.BUTTON_ADD)
        self._check_element_visible(locator=self.TITLE)
        self._add_address(open_form_locator=self.ADDRESS_BUTTON_OPEN, address=template['Address'])
        self._check_element_clickable(locator=self.BUTTON_GET_DATA)
        self._click_element(locator=self.BUTTON_GET_DATA)
        self._check_element_visible(locator=self.STAGE_LIVING_CYCLE)
        elements = self._find_element(self.STAGE_LIVING_CYCLE)
        self._select_option_by_text(selector=elements, text=template["Stage"])
        self._check_element_visible(locator=self.TYPE)
        elements = self._find_element(self.TYPE)
        self._select_option_by_text(selector=elements, text=template['TypeHouse'])
        self._fill_input_by_symbols(locator=self.FLOORS, value=template['CountOfFloors'])
        self._fill_input_by_symbols(locator=self.YEAR_OF_CONSTRUCTION, value=template['YearOfConstruction'])
        if save:
            self._click_element(locator=self.SAVE_CARD)
            if double:
                self._check_element_visible(locator=self.CHANGE_TABLE, visibility=True)
                elements = len(self._find_elements_visible(locator=self.TABLE_ROWS))
                el = self._find_elements_visible(locator=self.RADIO_BUTTON)
                for i in range(elements):
                    self._click_webelement(element=el[i])
                table = self._find_element(locator=self.TABLE)
                butt = self._find_element_by_relative_tag(base=table, tag="span", location="below")
                buttt = self._find_element_by_relative_tag(base=butt, tag="span", location="right")
                self._click_webelement(element=buttt)
                self._check_element_visible(locator=self.MAIN_TITLE, visibility=True)
            self._check_element_visible(locator=self.MAIN_TITLE, visibility=True)
        else:
            self._click_element(locator=self.BUTTON_BACK)
            self._check_element_visible(locator=self.MAIN_TITLE, visibility=True)

    def _check_data_object_living_house(self, template: dict):
        time.sleep(3)
        self._filter_by_feature(template=template, filter_type='address')
        element = self._find_element(locator=self.CARD)
        self._click_webelement(element=element)
        self._check_element_visible(locator=self.TITLE)
        area = self._get_element_attribute(locator=self.TYPE, attr_name="value")
        assert self.TypesObjects[area] == template['TypeHouse']
        stage = self._get_element_attribute(locator=self.STAGE_LIVING_CYCLE, attr_name="value")
        assert self.LivingCycle[stage] == template['Stage']
        self._check_element_value(locator=self.FLOORS, value=template['CountOfFloors'])
        self._get_element_attribute(locator=self.ADDRESS, attr_name="value")
        self._check_element_value(locator=self.ADDRESS, value=template['TemporaryAdd'])
        self._check_element_value(locator=self.YEAR_OF_CONSTRUCTION, value=template['YearOfConstruction'])

    def switch_tab(self):
        self._click_element(locator=self.SWITCH_TAB_INF)
        self._click_element(locator=self.LIVING_OBJECT)
        self._click_element(locator=self.SWITCH_TAB_INF)

    def _fill_new_service_inf(self, template: dict, save: bool, switch: bool):
        if switch:
            self.switch_tab()
        else:
            self._check_element_visible(locator=self.BUTTON_NEXT)
            self._click_element(locator=self.BUTTON_NEXT)
        self._check_element_visible(locator=self.EDITE)
        self._click_element(locator=self.EDITE)
        self._check_element_visible(locator=self.TABLE_EXPLOATE_ORGANISATION)
        self._click_element(locator=self.BUTTON_CHECK_FROM_LIST)
        self._click_element(locator=self.BUTTON_OPEN_MANAGE_COMPANY)
        self._open_card_by_key(key=template['ExploitationOrganisation'], into='object_housing_card')
        self._press_keyboard_key(key="PAGE DOWN")
        el = self._find_element(locator=self.BUTTON_CHECK_FROM_LIST_2)
        but = self._find_element_by_relative_tag(base=el, tag="span", location="below")
        self._click_webelement(element=but)
        self._check_element_visible(locator=self.TYPE)
        self._click_element(locator=self.BUTTON_NEXT)
        self._press_keyboard_key(key="PAGE DOWN")
        if save:
            self._click_element(locator=self.SAVE_CARD)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
            self._check_element_visible(locator=self.BUTTON_BACK, visibility=True)
            self._click_element(locator=self.BUTTON_BACK)
            self._check_element_visible(locator=self.MAIN_TITLE, visibility=True)

    def _check_service_inf(self, template: dict):
        self._filter_by_feature(template=template, filter_type='address')
        element = self._find_element(locator=self.CARD)
        self._click_webelement(element=element)
        self._check_element_visible(locator=self.TITLE)
        elements = self._find_elements_visible(locator=self.TABLE_EXPLOATE_ORGANISATION)
        self._get_element_by_text(elements=elements, text=template['ExploitationOrganisation'])
