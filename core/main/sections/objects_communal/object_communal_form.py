import time
from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper


class ObjectCommunalForm(AppSectionsHelper):
    # Locators
    TITLE = (By.XPATH, "//h1[contains(text(), 'Карточка объекта ЖКХ')]")
    AREAS_LIST = (By.XPATH, "//label[contains(text(), 'Сфера ЖКХ')]/..//select")
    STAGE = (By.XPATH, "//label[contains(text(), 'Этап')]/..//input")
    KIND = (By.XPATH, "//label[contains(text(), 'Объект')]/..//input")
    TYPE = (By.XPATH, "//label[contains(text(), 'Тип объекта')]/..//input")
    NAME = (By.XPATH, "//label[contains(text(), 'Наименование объекта')]/..//input")
    ADDRESS = (By.XPATH, "//label[contains(text(), 'Адрес местоположения объекта')]/..//input")
    OWNER = (By.XPATH, "//label[contains(text(), 'Выбрать собственника')]/..//input")
    OPERATOR = (By.XPATH, "//label[contains(text(), 'Выбрать эксплуатирующую организацию')]/..//input")
    ENERGY = (By.XPATH, "//label[contains(text(), 'Энергорайон')]/..//input")
    BUTTON_ADD = (By.XPATH, "//span[contains(text(), 'Добавить')]/parent::button")
    ADDRESS_BUTTON_OPEN = (By.XPATH, "//label[contains(text(), 'Адрес местоположения объекта')]/..//button")
    TYPE_BUTTON_OPEN = (By.XPATH, "//label[contains(text(), 'Этап')]/..//span[@class='MuiTouchRipple-root']")
    TYPE_FOR = (By.XPATH, "//div[contains(@role, 'radiogroup')]/label//span[contains(@class, 'MuiTypography-root')]")
    BUTTON_SAVE_STAGE = (By.XPATH,
                         "//h6[contains(text(), 'Этап')]/../..//span[contains(text(), 'Сохранить')]")
    CHOOSE_OWNER = (
    By.XPATH, "//label[contains(text(), 'Выбрать собственника')]/..//span[@class='MuiTouchRipple-root']")
    LIST_ORGANIZATION = (By.XPATH,
                         "//div[@class='solo_Card_wrapper__description class_block_registry_icon']/div[contains(text(), 'Наименование организации')]")
    BUTTON_USING_ORGANIZATION = (
    By.XPATH, "//label[contains(text(), 'Выбрать эксплуатирующую организацию')]/..//span[@class='MuiTouchRipple-root']")
    BUTTON_OBJECT_OPEN = (By.XPATH, "//label[contains(text(), 'Объект')]/..//span[@class='MuiTouchRipple-root']")
    BUTTON_SAVE_OBJECT = (By.XPATH, "//h6[contains(text(), 'Объект')]/../..//span[contains(text(), 'Сохранить')]")
    BUTTON_SAVE_TYPE_OBJECT = (
    By.XPATH, "//h6[contains(text(), 'Тип объекта')]/../..//span[contains(text(), 'Сохранить')]")
    NAME_OBJECT = (By.XPATH, "//label[contains(text(), 'Наименование объекта ')]/..//input")
    ENERGY_DISTRICT = (
    By.XPATH, "//label[contains(text(), 'Энергорайон')]/..//span[contains(@class, 'MuiTouchRipple-root')]")
    ENERGY_BUTTON_SAVE = (
    By.XPATH, "//h6[contains(text(), 'Энергорайон')]/../../..//span[contains(text(), 'Сохранить')]")
    SAVE_CARD = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Сохранить')]")
    SAVE_MESSAGE = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), 'Объект ЖКХ успешно создан')]")
    BUTTON_NEXT = (By.XPATH, "//button[@type='button']/span[contains(text(), 'Далее')]")
    EDITE = (By.XPATH, "//span[contains(text(), 'Редактировать')]")
    CURRENT_STATUS = (By.XPATH, "//label[contains(text(), 'Действующий статус')]/..//select")
    FUEL = (By.XPATH, "//label[contains(text(), 'Вид основного топлива')]/..//select")
    YEAR_OPERATING = (By.XPATH, "//label[contains(text(), 'Год ввода в эксплуатацию')]/..//input")
    TYPE_POWER_PLANT = (
    By.XPATH, "//label[contains(text(), 'Тип электростанции по типу первичных двигателей')]/..//select")
    FACTORY = (By.XPATH, "//label[contains(text(), 'Завод изготовитель')]/..//input")
    SETTING_POWER = (By.XPATH, "//label[contains(text(), 'Установленная мощность, МВт')]/..//input")
    SAVE_UPDATE = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), 'Объект успешно обновлен')]")
    BUTTON_CANCEL = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Отмена')]")
    MAIN_TITLE = (By.XPATH, "//h1[contains(text(), 'Реестр объектов ЖКХ')]")
    BUTTON_CONFIRM = (By.XPATH, "//span[contains(text(), 'Уйти со страницы')]")

    CURRENT_STATES = {
        "RESERV": "Резерв",
        "EXPLOITATION": "Эксплуатация",
        "NEW_CONSTRUCTION": "Новое строительство",
        "UNDER_MODERNIZATION": "В стадии модернизации",
        "TO_BE_DECOMMISSIONED": "Подлежит выводу из эксплуатации",
        "PROJECTED": "Проектируемый"
    }

    FUEL_LIST = {
        "GAS": "Газ",
        "COAL": "Уголь",
        "FUEL_OIL": "Мазут",
        "DIESEL": "Дизель",
        "OTHER_PETROLEUM": "Иные нефтепродукты",
        "FIREWOOD": "Дрова",
        "PEAT": "Торф",
        "OTHER": "Иное"
    }

    POWER_PLANTS = {
        "THERMAL_STEAM_TURBINE": "Тепловая турбина",
        "DIESEL": "Дизельная",
        "GAS_GENERATOR_AND_OTHER": "С газогенераторным двигателем и другими двигателями",
        "ATOMIC": "Атомная",
        "HYDROELECTRIC": "Гидроэлектростанция",
        "WIND": "Ветровая",
        "GEOTHERMAL": "Геотермальная",
        "SUNNY": "Солнечная",
        "BIOELECTRIC": "Биоэлектростанция"
    }

    def _get_data(self):
        time.sleep(1)
        _area = self._get_element_attribute(locator=self.AREAS_LIST, attr_name="value")
        _stage = self._get_element_attribute(locator=self.STAGE, attr_name="value")
        _kind = self._get_element_attribute(locator=self.KIND, attr_name="value")
        _type = self._get_element_attribute(locator=self.TYPE, attr_name="value")
        _name = self._get_element_attribute(locator=self.NAME, attr_name="value")
        _address = self._get_element_attribute(locator=self.ADDRESS, attr_name="value")
        _owner = self._get_element_attribute(locator=self.OWNER, attr_name="value")
        _operator = self._get_element_attribute(locator=self.OPERATOR, attr_name="value")
        data = {
            "Area": _area,
            "Stage": _stage,
            "Kind": _kind,
            "Type": _type,
            "Name": _name,
            "Address": _address,
            "Owner": _owner,
            "Operator": _operator
        }
        return data

    def _get_data_object_main_properties(self):
        time.sleep(1)
        _current_status = self._get_element_attribute(locator=self.CURRENT_STATUS, attr_name="value")
        _fuel = self._get_element_attribute(locator=self.FUEL, attr_name="value")
        _year_operating = self._get_element_attribute(locator=self.YEAR_OPERATING, attr_name="value")
        _type_of_power_plant = self._get_element_attribute(locator=self.TYPE_POWER_PLANT, attr_name="value")
        _factory = self._get_element_attribute(locator=self.FACTORY, attr_name="value")
        _power = self._get_element_attribute(locator=self.SETTING_POWER, attr_name="value")

        data = {
            "CurrentStatus": _current_status,
            "Fuel": _fuel,
            "YearOperating": _year_operating,
            "TypeOfPowerPlant": _type_of_power_plant,
            "Factory": _factory,
            "Power": _power,
        }
        return data

    def _fill_new_card_object(self, template: dict, save: bool):
        self._click_element(locator=self.BUTTON_ADD)
        self._check_element_visible(locator=self.TITLE)
        elements = self._find_element(self.AREAS_LIST)
        self._select_option_by_text(selector=elements, text=template["TypeGKH"])
        self._click_element(locator=self.TYPE_BUTTON_OPEN)
        elements = self._find_elements_visible(locator=self.TYPE_FOR)
        stage = self._get_element_by_text(elements=elements, text=template['Stage'])
        self._click_webelement(element=stage)
        self._click_element(locator=self.BUTTON_SAVE_STAGE)
        self._click_element(locator=self.CHOOSE_OWNER)
        elements = self._find_elements_visible(locator=self.LIST_ORGANIZATION)
        card = self._get_element_by_text(elements=elements, text=template['Owner'])
        self._click_webelement(element=card)
        self._click_element(locator=self.BUTTON_USING_ORGANIZATION)
        elements = self._find_elements_visible(locator=self.LIST_ORGANIZATION)
        card = self._get_element_by_text(elements=elements, text=template['Owner'])
        self._click_webelement(element=card)
        self._add_address(open_form_locator=self.ADDRESS_BUTTON_OPEN, address=template['Address'])
        button_obj_open = self._find_element(locator=self.BUTTON_OBJECT_OPEN)
        self._click_webelement(element=button_obj_open)
        elements = self._find_elements_visible(locator=self.TYPE_FOR)
        object_web = self._get_element_by_text(elements=elements, text=template['Object'])
        self._click_webelement(element=object_web)
        self._click_element(locator=self.BUTTON_SAVE_OBJECT)
        button_type_object_open = self._find_element_by_relative_tag(base=button_obj_open, tag="span", location="below")
        self._click_webelement(element=button_type_object_open)
        elements = self._find_elements_visible(locator=self.TYPE_FOR)
        type_of = self._get_element_by_text(elements=elements, text=template['TypeObject'])
        self._click_webelement(element=type_of)
        self._click_element(locator=self.BUTTON_SAVE_TYPE_OBJECT)
        self._fill_input_by_symbols(locator=self.NAME_OBJECT, value=template['NameObject'])
        self._click_element(locator=self.ENERGY_DISTRICT)
        elements = self._find_elements_visible(locator=self.TYPE_FOR)
        energy = self._get_element_by_text(elements=elements, text=template['EnergyDistrict'])
        self._click_webelement(element=energy)
        self._click_element(locator=self.ENERGY_BUTTON_SAVE)
        if save:
            self._click_element(locator=self.SAVE_CARD)
            self._check_element_visible(locator=self.SAVE_MESSAGE, visibility=True)
            return template['NameObject']
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
            self._click_element(locator=self.BUTTON_CONFIRM)
            self._check_element_visible(locator=self.MAIN_TITLE, visibility=True)

    def _check_data_object_gkh(self, template: dict):
        area = self._get_element_attribute(locator=self.AREAS_LIST, attr_name="value")
        assert self.Areas[area] == template['TypeGKH']
        self._check_element_value(locator=self.STAGE, value=template['Stage'])
        self._check_element_value(locator=self.OWNER, value=template['FullName'])
        self._check_element_value(locator=self.OPERATOR, value=template['FullName'])
        self._check_element_value(locator=self.ADDRESS, value=template['FullAddress'])
        self._check_element_value(locator=self.KIND, value=template['Object'])
        self._check_element_value(locator=self.TYPE, value=template['TypeObject'])
        self._check_element_value(locator=self.NAME, value=template['NameObject'])
        self._check_element_value(locator=self.ENERGY, value=template['EnergyDistrict'])

    def _fill_main_properties(self, template: dict, area_key: str):
        self._check_element_visible(locator=self.BUTTON_NEXT)
        self._click_element(locator=self.BUTTON_NEXT)
        self._check_element_visible(locator=self.EDITE)
        self._click_element(locator=self.EDITE)
        element = self._find_element(self.CURRENT_STATUS)
        self._select_option_by_text(selector=element, text=template["CurrentStatus"])
        self._fill_input_by_symbols(locator=self.YEAR_OPERATING, value=template['YearOperating'])
        match area_key:
            case "electro":
                element1 = self._find_element(self.FUEL)
                self._select_option_by_text(selector=element1, text=template["Fuel"])
                element2 = self._find_element(self.TYPE_POWER_PLANT)
                self._select_option_by_text(selector=element2, text=template["TypeOfPowerPlant"])
                self._fill_input_by_symbols(locator=self.FACTORY, value=template['Factory'])
                self._fill_input_by_symbols(locator=self.SETTING_POWER, value=template['Power'])
        self._click_element(locator=self.SAVE_CARD)
        self._check_element_visible(locator=self.SAVE_UPDATE)
        button_back = self._find_element_by_relative_tag(base=element, tag="span", location="below")
        self._click_webelement(button_back)
        self._check_element_visible(locator=self.BUTTON_NEXT)
        self._click_element(locator=self.BUTTON_NEXT)

    def _check_data_main_properties(self, template: dict):
        status = self._get_element_attribute(locator=self.CURRENT_STATUS, attr_name="value")
        assert self.CURRENT_STATES[status] == template['CurrentStatus']
        fuel = self._get_element_attribute(locator=self.FUEL, attr_name="value")
        assert self.FUEL_LIST[fuel] == template['Fuel']
        self._check_element_value(locator=self.YEAR_OPERATING, value=template['YearOperating'])
        power_plant = self._get_element_attribute(locator=self.TYPE_POWER_PLANT, attr_name="value")
        assert self.POWER_PLANTS[power_plant] == template['TypeOfPowerPlant']
        self._check_element_value(locator=self.FACTORY, value=template['Factory'])
        self._check_element_value(locator=self.SETTING_POWER, value=template['Power'])

    def _edit_card(self, template: dict):
        initial_date = self._get_data_object_main_properties()
        self._check_element_visible(locator=self.EDITE)
        self._click_element(locator=self.EDITE)
        self._fill_input_by_symbols(locator=self.YEAR_OPERATING, value=template['OtherYear'])
        element2 = self._find_element(self.CURRENT_STATUS)
        self._select_option_by_text(selector=element2, text=template['OtherStatus'])
        up_to_date_data = self._get_data_object_main_properties()
        assert initial_date is not up_to_date_data
