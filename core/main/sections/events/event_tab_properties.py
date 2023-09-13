import time
from selenium.webdriver.common.by import By
from core.main.sections.events.event_tabs_common import EventTabsCommon


class EventTabProperties(EventTabsCommon):
    # Locators
    TYPES_LIST = (By.XPATH, "//label[contains(text(), 'Тип события')]/..//select")
    SOLUTION_DATE_TIME = (By.XPATH, "//label[contains(text(), 'Дата и время устранения')]/..//input")
    SIGNS_TEXTAREA = (By.XPATH, "//label[contains(text(), 'Учетные признаки события')]/..//textarea[1]")
    SIGNS_BUTTON_OPEN = (By.XPATH, "//label[contains(text(), 'Учетные признаки события')]/..//button")
    SIGNS_TITLE = (By.XPATH, "//h6[contains(text(), 'Учётные признаки события')]")
    SIGNS_BUTTON_CANCEL = (By.XPATH, "//h6[contains(text(), 'Учётные признаки события')]/../.."
                                     "//span[contains(text(), 'Отмена')]/parent::button")
    SIGNS_BUTTON_SAVE = (By.XPATH, "//h6[contains(text(), 'Учётные признаки события')]/../.."
                                   "//span[contains(text(), 'Сохранить')]/parent::button")
    SIGNS_LIST = (By.XPATH, "//div[@role='radiogroup']/label/span[2]")

    PARENT_EVENT = (By.XPATH, "//label[contains(text(), 'Родительское событие')]/..//input")
    PARENT_EVENT_BUTTON_OPEN = (By.XPATH, "//label[contains(text(), 'Родительское событие')]/..//button")

    WEATHER_TEXTAREA = (By.XPATH, "//label[contains(text(), 'Погодные условия в месте события')]/..//textarea")
    WEATHER_BUTTON_OPEN = (By.XPATH, "//label[contains(text(), 'Погодные условия в месте события')]/..//button")
    WEATHER_TITLE = (By.XPATH, "//h6[contains(text(), 'Погодные условия в месте события')]")
    WEATHER_BUTTON_CANCEL = (By.XPATH, "//h6[contains(text(), 'Погодные условия в месте события')]/../.."
                                       "//span[contains(text(), 'Отмена')]/parent::button")
    WEATHER_BUTTON_SAVE = (By.XPATH, "//h6[contains(text(), 'Погодные условия в месте события')]/../.."
                                     "//span[contains(text(), 'Сохранить')]/parent::button")
    WEATHER_DESCRIPTION = (By.XPATH, "//label[contains(text(), 'Описание')]/..//input")
    WEATHER_WIND_SPEED = (By.XPATH, "//label[contains(text(), 'Скорость ветра')]/..//input")
    WEATHER_WIND_DIRECTION = (By.XPATH, "//label[contains(text(), 'Направление ветра')]/..//input")
    WEATHER_WIND_DIRECTION_DROPDOWN = (By.XPATH, "//label[contains(text(), 'Направление ветра')]/.."
                                                 "//div[@id='windDirectionSelect']")
    WEATHER_WIND_DIRECTIONS_LIST = (By.XPATH, "//div[@id='menu-']//ul/li[@role='option']")
    WEATHER_TEMPERATURE = (By.XPATH, "//label[contains(text(), 'Температура воздуха')]/..//input")
    WEATHER_SOURCE = (By.XPATH, "//label[contains(text(), 'Источник информации')]/..//input")

    INJURED = (By.XPATH, "//label[contains(text(), 'Количество пострадавших')]/..//input")
    LOST = (By.XPATH, "//label[contains(text(), 'Количество погибших')]/..//input")
    STATUSES_LIST = (By.XPATH, "//label[contains(text(), 'Статус решения')]/..//select")
    DUPLICATE_TITLE = (By.XPATH, "//h2[contains(text(), 'В системе найдена похожая запись')]")
    DUPLICATE_CARD_CHECKBOX = (By.XPATH, "./../../td[1]/label/span")
    DUPLICATE_CARDS_KEYS = (By.XPATH, "//tr/td[6]/a")
    DUPLICATE_BUTTON_SAVE = (By.XPATH, "//span[contains(text(), 'Все равно сохранить текущую карточку')]"
                                       "/parent::button")
    DUPLICATE_BUTTON_DELETE = (By.XPATH, "//span[contains(text(), 'Удалить текущую карточку')]"
                                         "/parent::button")

    Types = {
          "ACCIDENT": "Авария",
          "INCIDENT": "Инцидент",
          "PLANNED": "Плановое"
    }

    Statuses = {
        "IN_PROGRESS": "В работе",
        "ELIMINATED": "Устранено",
        "COMPLETED": "Завершенное"
    }

    def _check_elements_editable(self, disabled: bool):
        self._check_element_editable(locator=self.TYPES_LIST, disabled=disabled)
        self._check_element_editable(locator=self.SOLUTION_DATE_TIME, disabled=disabled)
        self._check_element_editable(locator=self.SIGNS_TEXTAREA, disabled=True)
        self._check_element_editable(locator=self.SIGNS_BUTTON_OPEN, disabled=disabled)
        self._check_element_editable(locator=self.WEATHER_BUTTON_OPEN, disabled=disabled)
        self._check_element_editable(locator=self.INJURED, disabled=disabled)
        self._check_element_editable(locator=self.LOST, disabled=disabled)
        self._check_element_editable(locator=self.STATUSES_LIST, disabled=disabled)

    def _get_data(self):
        # TODO: Добаваить обработку поля "Срок планового отключения" для Тип события = "Плановое"

        time.sleep(0.5)

        # _type = self._get_selected_option(select_locator=self.TYPES_LIST)['Text']
        _type = self._get_element_attribute(locator=self.TYPES_LIST, attr_name="value")

        _solution_date_time = self._get_element_attribute(locator=self.SOLUTION_DATE_TIME, attr_name="value")
        _sign = self._find_element(locator=self.SIGNS_TEXTAREA).text
        _parent_event = self._get_element_attribute(locator=self.PARENT_EVENT, attr_name="value")
        _weather = self._find_element(locator=self.WEATHER_TEXTAREA).text
        _injured = self._get_element_attribute(locator=self.INJURED, attr_name="value")
        _lost = self._get_element_attribute(locator=self.LOST, attr_name="value")

        # _status = self._get_selected_option(select_locator=self.STATUSES_LIST)['Text']
        _status = self._get_element_attribute(locator=self.STATUSES_LIST, attr_name="value")

        data = {
            "Type": self.Types[_type],
            "SolutionDateTime": _solution_date_time,
            "Sign": _sign,
            "ParentEvent": _parent_event,
            "WeatherText": _weather,
            "EmergencyData":
            {
                "Injured": _injured,
                "Lost": _lost
            },
            "Status": self.Statuses[_status]
        }
        return data

    def _check_data(self, template: dict):
        # TODO: Добавить обработку поля "Срок планового отключения" для Тип события = "Плановое"
        # assert self._get_selected_option(select_locator=self.TYPES_LIST)['Text'] == template['Type']
        _type = self._get_element_attribute(locator=self.TYPES_LIST, attr_name="value")
        assert self.Types[_type] == template['Type']

        self._check_element_value(locator=self.SOLUTION_DATE_TIME, value=template['SolutionDateTime'])
        self._check_element_text(locator=self.SIGNS_TEXTAREA, text=template['Sign'])
        self._check_element_value(locator=self.PARENT_EVENT, value=template['ParentEvent'])
        if "Weather" in template.keys():
            weather = f"описание: {template['Weather']['Description']}, "
            weather += f"температура воздуха {template['Weather']['Temperature']}°С, "
            weather += f"скорость ветра {template['Weather']['WindSpeed']} м/с, "
            weather += f"направление ветра: {template['Weather']['WindDirection']}, "
            weather += f"источник информации - {template['Weather']['Source']}"
            template['WeatherText'] = weather
        self._check_element_text(locator=self.WEATHER_TEXTAREA, text=template['WeatherText'])
        self._check_element_value(locator=self.INJURED, value=str(template['EmergencyData']['Injured']))
        self._check_element_value(locator=self.LOST, value=str(template['EmergencyData']['Lost']))

        _status = self._get_element_attribute(locator=self.STATUSES_LIST, attr_name="value")
        assert self.Statuses[_status] == template['Status']

    def _fill_data(self, template: dict, save: bool, duplicate_save: bool = True):
        # TODO: Добавить обработку поля "Срок планового отключения" для Тип события = "Плановое"
        # time.sleep(1)
        self._check_buttons(edit=False)
        self._check_elements_editable(disabled=True)
        self._click_element(locator=self.BUTTON_EDIT)
        self._check_buttons(edit=True)
        self._check_elements_editable(disabled=False)
        elements = self._click_element(locator=self.TYPES_LIST)
        self._select_option_by_text(selector=elements, text=template['Type'])
        self._click_element(locator=self.SIGNS_BUTTON_OPEN)
        self._check_element_visible(locator=self.SIGNS_TITLE)
        elements = self._find_elements_visible(locator=self.SIGNS_LIST)
        element = self._get_element_by_text(elements=elements, text=template['Sign'])
        self._click_webelement(element=element)
        self._click_element(locator=self.SIGNS_BUTTON_SAVE)

        # TODO: Реализовать заполнение поля "Родительское событие"

        self._click_element(locator=self.WEATHER_BUTTON_OPEN)
        self._check_element_visible(locator=self.WEATHER_TITLE)
        time.sleep(5)  # Ожидание автоматического заполнения погодных данных
        self._fill_input(locator=self.WEATHER_DESCRIPTION, value=template['Weather']['Description'])
        self._fill_input(locator=self.WEATHER_WIND_SPEED, value=template['Weather']['WindSpeed'])
        self._click_element(locator=self.WEATHER_WIND_DIRECTION_DROPDOWN)
        elements = self._find_elements_visible(locator=self.WEATHER_WIND_DIRECTIONS_LIST)
        element = self._get_element_by_text(elements=elements, text=template['Weather']['WindDirection'])
        self._click_webelement(element=element)
        self._fill_input(locator=self.WEATHER_TEMPERATURE, value=template['Weather']['Temperature'])
        self._fill_input(locator=self.WEATHER_SOURCE, value=template['Weather']['Source'])
        self._click_element(locator=self.WEATHER_BUTTON_SAVE)

        value = str(template['EmergencyData']['Injured'])
        if value.isdigit():
            self._fill_input(locator=self.INJURED, value=value)
        value = str(template['EmergencyData']['Lost'])
        if value.isdigit():
            self._fill_input(locator=self.LOST, value=value)
        if save:
            self._click_element(locator=self.BUTTON_SAVE)
            if self._is_element_visible(locator=self.DUPLICATE_TITLE, timeout=3):
                if duplicate_save:
                    self._click_element(locator=self.DUPLICATE_BUTTON_SAVE)
                    self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=True)
                    self._check_element_visible(locator=self.DUPLICATE_TITLE, visibility=False)
                    self._check_buttons(edit=False)
                    self._check_elements_editable(disabled=True)
                else:
                    elements = self._find_elements_visible(locator=self.DUPLICATE_CARDS_KEYS)
                    element = self._get_element_by_text(elements=elements, text=template['DuplicateKey'])
                    element_checkbox = self._find_element_from_base(base=element, locator=self.DUPLICATE_CARD_CHECKBOX)
                    self._click_webelement(element=element_checkbox)
                    self._click_element(locator=self.DUPLICATE_BUTTON_DELETE)
                    self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=False)
                    self._check_element_visible(locator=self.DUPLICATE_TITLE, visibility=False)
            else:
                self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=True)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
            self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=False)
            self._check_buttons(edit=False)
            self._check_elements_editable(disabled=True)
        time.sleep(1)  # Для гарантированного сохранения данных TODO: Возможно надо будет поискать другое решение

    # TODO: Probably this method should be moved to another class
    @staticmethod
    # def _get_emergency_type(injured: int, lost: int):
    def _get_emergency_type(emergency_data: dict):
        # TODO: Ask for proper calculation formula of emergency type depending on values into "Injured" and "Lost" keys
        injured, lost = str(emergency_data['Injured']), str(emergency_data['Lost'])
        if lost.isdigit() and int(lost) > 0:
            result = "Угроза: ЧС"
        else:
            result = "Нет угрозы ЧС"
        return result

    # def _edit_emergency_data(self, injured: int, lost: int, save: bool = True):
    def _edit_emergency_data(self, emergency_data: dict, save: bool = True):
        self._check_buttons(edit=False)
        self._check_elements_editable(disabled=True)
        self._click_element(locator=self.BUTTON_EDIT)
        self._check_buttons(edit=True)
        self._check_elements_editable(disabled=False)
        value = str(emergency_data['Injured'])
        if value.isdigit():
            self._fill_input(locator=self.INJURED, value=value)
        value = str(emergency_data['Lost'])
        if value.isdigit():
            self._fill_input(locator=self.LOST, value=value)
        if save:
            self._click_element(locator=self.BUTTON_SAVE)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
        self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=save)
        self._check_buttons(edit=False)
        self._check_elements_editable(disabled=True)
        # time.sleep(1)
