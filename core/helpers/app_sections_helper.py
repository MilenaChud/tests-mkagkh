import allure
from datetime import date, datetime
import os
import time
from selenium.webdriver.common.by import By
from core.helpers.app_auth_helper import AppAuthHelper
from core.helpers.app_notif_helper import AppNotifHelper
from core.helpers.base_helper import BaseHelper


class AppSectionsHelper(BaseHelper):
    # Locators
    SORT_LIST = (By.XPATH, "//div[@class='Filter_data_block Select']/div")
    SORT_OPTIONS_LABEL = (By.XPATH, "//div[@aria-labelledby='SortType']")
    SORT_OPTIONS = (By.XPATH, "//ul[@aria-labelledby='SortType']/li")

    RESPONSIBLES_FORM_TITLE = (By.XPATH, "//h6[contains(text(), 'Ответственные лица')]")
    RESPONSIBLES_FORM_CLOSE = (By.XPATH, "//h6[contains(text(), 'Ответственные лица')]/..//button")
    RESPONSIBLES_FORM_ORGANIZATIONS_LABEL = (By.XPATH, "//h6[contains(text(), 'Ответственные лица')]/../.."
                                                       "//label[contains(text(), 'Выберите организацию')]")
    RESPONSIBLES_FORM_ORGANIZATIONS = (By.XPATH, "//h6[contains(text(), 'Ответственные лица')]/../..//input")
    RESPONSIBLES_FORM_PERSONS_LABEL = (By.XPATH, "//div[contains(text(), 'Выберите сотрудника')]")
    RESPONSIBLES_FORM_PERSONS = (By.XPATH, f"//div[contains(text(), 'Выберите сотрудника')]/../../..//tbody/tr")

    ADDRESS_FORM_PLACE = (By.XPATH, "//label[contains(text(), 'Населенный пункт')]/..//input")
    ADDRESS_FORM_STREET = (By.XPATH, "//label[contains(text(), 'Улица')]/..//input")
    ADDRESS_FORM_HOUSE = (By.XPATH, "//label[contains(text(), 'Дом')]/..//input")
    ADDRESS_FORM_BUTTON_SAVE = (By.XPATH, "//label[text()='Населенный пункт']/"
                                          "following::span[contains(text(), 'Сохранить')]/parent::button")

    CALENDAR_BUTTON_NEXT_LEFT = (By.XPATH, "//div[@class='MuiPickersCalendarHeader-switchHeader']//button[1]")
    CALENDAR_BUTTON_NEXT_RIGHT = (By.XPATH, "//div[@class='MuiPickersCalendarHeader-switchHeader']//button[2]")
    CALENDAR_BUTTON_OK = (By.XPATH, "//span[contains(text(), 'OK')]")

    SEARCH_FORM_OPEN = (By.XPATH, "//span[contains(text(), 'Поиск')]/parent::button")
    SEARCH_FORM_CLOSE = (By.XPATH, "//span[contains(text(), 'Закрыть')]/parent::button")
    SEARCH_FORM_BUTTON_FIND = (By.XPATH, "(//span[contains(text(), 'Поиск')]/parent::button)[last()]")

    FILTERS = (By.XPATH, "//div[contains(text(), 'Фильтры')]")
    FILTERS_TITLE = (By.XPATH, "//div[@class='filters_block']/h2[contains(text(), 'Фильтрация')]")
    FILTERS_BUTTON_CLEAR = (By.XPATH, "//div[@class='filters_block']/.."
                                      "//span[contains(text(), 'Сбросить')]/parent::button")
    FILTER_SPHERE_GKH = (By.XPATH, "//div[contains(text(), 'Сфера ЖКХ')]/..//label/span[2]")
    FILTER_PRICE = (By.XPATH, "//div[contains(text(), 'По стоимости')]/..//input[@name='До']")

    Areas = {
        "1": "Электроснабжение",
        "2": "Теплоснабжение и горячее водоснабжение",
        "3": "Холодное водоснабжение",
        "4": "Водоотведение",
        "5": "Газоснабжение",
        "6": "Эксплуатация жилищного фонда"
    }

    def __init__(self, driver):
        super().__init__(driver=driver)
        self._auth = AppAuthHelper(driver=driver)
        self._notif = AppNotifHelper(driver=driver)

    def _prepare_data_from_template(self, filename: str, area_key: str):
        data = self._read_data_from_file(filename=filename)
        if (list(data.keys()) == ['AreaKey', 'Template']) and (data['AreaKey'] == area_key):
            with allure.step(f"Successfully prepare data for area key \'{area_key}\' from file \'{filename}\'"):
                self._logger.info(f"Successfully prepare data for area key \'{area_key}\' from file \'{filename}\'")
                return data['Template']
        else:
            with allure.step(f"Failed to prepare data - can't find template for area key \'{area_key}\'"
                             f" in file \'{filename}\'"):
                self._logger.error(f"Assertion Error: Failed to prepare data - can't find template for"
                                   f" area key \'{area_key}\' in file \'{filename}\'")
                raise AssertionError(f"Failed to prepare data - can't find template for area key"
                                     f" \'{area_key}\' in file \'{filename}\'")

    def _get_file_info(self, filename: str, full: bool = False):
        file_type = filename.split(".")[-1].lower()
        file_image_flag = True if file_type in ("jpg", "jpeg", "png") else False
        file_basename = self._get_file_basename(filename=filename)
        file_info = {
            "Image": file_image_flag,
            "Name": file_basename
        }
        if full:
            file_size = self._get_file_size(filename=filename)
            file_hash = self._get_file_hash(filename=filename)
            file_info["Size"] = file_size
            file_info["Hash"] = file_hash
        return file_info

    def _prepare_download(self, filename: str):
        downloads = self._driver.data_paths["downloads"]
        target_file = f"{downloads}/{self._get_file_basename(filename=filename)}"
        if os.path.isfile(path=target_file):
            os.remove(path=target_file)
        for file in os.listdir(path=downloads):
            if os.path.isfile(path=file) and file.endswith((".crdownload", ".part")):
                os.remove(path=file)
        return self

    def _get_download_info(self, filename: str, timeout: int = 5):
        downloads = self._driver.data_paths["downloads"]
        target_file = f"{downloads}/{self._get_file_basename(filename=filename)}"
        target_file_info = {}
        size = 0
        timer = 0
        temp_target_file = None
        while timer < timeout:
            time.sleep(1)
            timer += 1
            if temp_target_file is None:
                files = os.listdir(path=downloads)
                temp_files = list(filter(lambda item: item.endswith((".crdownload", ".part")), files))
                if len(temp_files) > 0:
                    temp_target_file = f"{downloads}/{temp_files[0]}"
            else:
                try:
                    temp_size = self._get_file_size(filename=temp_target_file)
                except FileNotFoundError:
                    time.sleep(0.5)
                    timer = timeout
                else:
                    if temp_size > size:
                        timer = 0
                        size = temp_size

        if os.path.isfile(path=target_file):
            target_file_info = self._get_file_info(filename=target_file, full=True)
        return target_file_info

    def _switch_sort(self, sort_type: str):
        self._check_element_visible(locator=self.SORT_OPTIONS_LABEL)
        self._click_element(locator=self.SORT_LIST)
        time.sleep(1)
        elements = self._find_elements_visible(locator=self.SORT_OPTIONS)
        element = self._get_element_by_text(elements=elements, text=sort_type)
        self._click_webelement(element=element)
        return self

    def _add_responsible(self, open_form_locator: tuple, responsible: dict):
        expected = (responsible['Organization'], responsible['Position'], responsible['FullName'])
        self._click_element(locator=open_form_locator)
        self._check_element_visible(locator=self.RESPONSIBLES_FORM_TITLE)
        self._check_element_visible(locator=self.RESPONSIBLES_FORM_ORGANIZATIONS_LABEL)
        self._fill_input(locator=self.RESPONSIBLES_FORM_ORGANIZATIONS, value=expected[0])
        self._press_keyboard_key(key="DOWN, ENTER")

        time.sleep(0.5)
        self._check_element_visible(locator=self.RESPONSIBLES_FORM_PERSONS_LABEL)
        elements = self._find_elements_visible(locator=self.RESPONSIBLES_FORM_PERSONS)
        found = False
        row = 0
        while (not found) and (row < len(elements)):
            row += 1
            col = 1
            flag = True
            while flag and (col < len(expected)):
                td_locator = (By.XPATH, f"//div[contains(text(), 'Выберите сотрудника')]/../../.."
                                        f"//tbody//tr[{row}]/td[{col}]")
                td_text = self._check_element_visible(locator=td_locator).text.strip()
                flag = (td_text == expected[col])
                col += 1
            found = flag
        if found:
            self._click_webelement(element=elements[row - 1])
        else:
            self._click_element(locator=self.RESPONSIBLES_FORM_CLOSE)
        self._check_element_visible(locator=self.RESPONSIBLES_FORM_TITLE, visibility=False)

    def _add_address(self, open_form_locator: tuple, address: dict, save: bool = True):
        self._click_element(locator=open_form_locator)
        self._check_element_visible(locator=self.ADDRESS_FORM_PLACE)
        self._fill_input_by_symbols(locator=self.ADDRESS_FORM_PLACE, value=address['Place'])
        self._press_keyboard_key(key="DOWN, ENTER")
        self._fill_input_by_symbols(locator=self.ADDRESS_FORM_STREET, value=address['Street'])
        self._press_keyboard_key(key="DOWN, ENTER")
        self._fill_input_by_symbols(locator=self.ADDRESS_FORM_HOUSE, value=address['House'])
        self._press_keyboard_key(key="DOWN, ENTER")
        if save:
            self._click_element(locator=self.ADDRESS_FORM_BUTTON_SAVE)
            self._check_element_visible(locator=self.ADDRESS_FORM_PLACE, visibility=False)

    def _set_calendar(self, input_locator: tuple, target_date_time: str):
        # Parameter target_date_time should be in format: DD-MM-YYYY hh:mm
        current_date_time = self._get_element_attribute(locator=input_locator, attr_name="value")
        if len(current_date_time) > 0:
            current_date = datetime.strptime(current_date_time, "%d-%m-%Y %H:%M").date()
        else:
            current_date = date.today()
        target = datetime.strptime(target_date_time, "%d-%m-%Y %H:%M")
        target_date, target_time = target.date(), target.time()
        delta = (target_date.year - current_date.year) * 12 + (target_date.month - current_date.month)
        self._click_element(locator=input_locator)
        button_next = self.CALENDAR_BUTTON_NEXT_RIGHT if delta >= 0 else self.CALENDAR_BUTTON_NEXT_LEFT
        for i in range(abs(delta)):
            self._click_element(locator=button_next)
        time.sleep(0.5)
        target_day = target_date.day
        position = "1" if 1 <= target_day <= 24 else "last()"
        target_day = str(target_day)
        target_day_locator = (By.XPATH, f"(//div[contains(@class, 'Calendar-transitionContainer')]//"
                                        f"p[text()='{target_day}'])[{position}]")
        self._click_element(locator=target_day_locator)
        target_hours = target_time.hour
        target_hours = str(target_hours) if target_hours > 0 else "00"
        target_hours_locator = (By.XPATH, f"//div[@class='MuiPickersClock-clock']/span[text()='{target_hours}']")
        self._click_element(locator=target_hours_locator)
        target_minutes = target_time.minute
        target_minutes = str(target_minutes) if target_minutes > 5 else "0" + str(target_minutes)
        target_minutes_locator = (By.XPATH, f"//div[@class='MuiPickersClock-clock']/span[text()='{target_minutes}']")
        self._click_element(locator=target_minutes_locator)
        self._click_element(locator=self.CALENDAR_BUTTON_OK)

    def _find_card_by_key(self, key: str, presence: bool, close_search: bool, into: str):
        search_label = None
        search_input = None
        search_results = None
        search_result_element = None
        timeout = 1
        match into:
            case "event_card":
                search_label = (By.XPATH, "//label[@id='ZKHObjects_add_objectSphereServiceSelect' "
                                          "and contains(text(), 'Наименование объекта')]")
                search_input = (By.XPATH, "//label[@id='ZKHObjects_add_objectSphereServiceSelect' "
                                          "and contains(text(), 'Наименование объекта')]/..//input")
                search_results = (By.XPATH, f"//div[@class='solo_Card_wrapper__header__info_header' "
                                            f"and text()='{key}']")
                search_result_element = (By.XPATH, "./ancestor::div[@data-testid='card-click']")

            case "objects_communal":
                search_label = (By.XPATH, "//h3[contains(text(), 'Поиск объектов ЖКХ')]")
                search_input = (By.XPATH, "//label[contains(text(), 'Наименование объекта')]/..//input")
                search_results = (By.XPATH, f"//div[@class='solo_Card_wrapper__header__info_header' "
                                            f"and text()='{key}']")
                search_result_element = (By.XPATH, "./ancestor::div[@data-testid='card-click']")

            case "users":
                search_label = (By.XPATH, "//h3[contains(text(), 'Поиск пользователей')]")
                search_input = (By.XPATH, "//label[contains(text(), 'Логин пользователя')]/..//input")
                search_results = (By.XPATH, f"(//tbody/tr/td/div[text()='{key}'])[1]")
                search_result_element = (By.XPATH, "./../../td[1]")
                timeout = 5

            case "object_housing_card":
                search_label = (By.XPATH, "//h3[contains(text(), 'Поиск в реестре организаций')]")
                search_input = (By.XPATH, "//label[contains(text(), 'Наименование организации')]/..//input")
                search_results = (By.XPATH, f"//div[@class='solo_Card_wrapper__description__info_text' "
                                            f"and text()='{key}']")
                search_result_element = (By.XPATH, "./ancestor::div[@data-testid='card-click']")

            case "organizations":
                search_label = (By.XPATH, "//h3[contains(text(), 'Поиск в реестре организаций')]")
                search_input = (By.XPATH, "//label[contains(text(), 'Наименование организации')]/..//input")
                search_results = (By.XPATH, f"//div[@class='solo_Card_wrapper__description__info_text' "
                                            f"and text()='{key}']")
                search_result_element = (By.XPATH, "./ancestor::div[@data-testid='card-click']")

        self._click_element(locator=self.SEARCH_FORM_OPEN)
        self._check_element_visible(locator=search_label)
        self._fill_input(locator=search_input, value=key)
        self._check_element_editable(locator=self.SEARCH_FORM_BUTTON_FIND, disabled=False)
        self._click_element(locator=self.SEARCH_FORM_BUTTON_FIND)
        time.sleep(timeout)
        result_key = self._check_element_visible(locator=search_results, visibility=presence)
        if presence:
            result = self._find_element_from_base(base=result_key, locator=search_result_element)
        else:
            result = result_key
        if close_search:
            self._click_element(locator=self.SEARCH_FORM_CLOSE)
        return result

    def _open_card_by_key(self, key: str, into: str):
        title_locator = None
        input_locator = None
        input_check_type = "value"
        match into:
            case "event_card":
                title_locator = (By.XPATH, "//h1[contains(text()[1], 'Карточка события')"
                                           " and contains(text()[2], 'на объекте ЖКХ')]")
                input_locator = (By.XPATH, "//label[contains(text(), 'Наименование объекта')]/..//input")

            case "objects_communal":
                title_locator = (By.XPATH, "//h1[contains(text(), 'Карточка объекта ЖКХ')]")
                input_locator = (By.XPATH, "//label[contains(text(), 'Наименование объекта')]/..//input")

            case "users":
                title_locator = (By.XPATH, "//h6[contains(text(), 'Редактирование пользователя')]")
                input_locator = (By.XPATH, "//label[contains(text(), 'Логин пользователя')]/..//input")

            case "object_housing_card":
                title_locator = (By.XPATH, "//h1[contains(text(), 'Карточка объекта жилищного фонда')]")
                input_locator = (By.XPATH, "//th[contains(text(), 'Наименование организации')]/../../../.."
                                           "//tbody//td[1]")
                input_check_type = "text"

            case "organizations":
                title_locator = (By.XPATH, "//h1[contains(text(), 'Карточка организации')]")
                input_locator = (By.XPATH, "//label[contains(text(), 'Наименование организации')]/..//input")

        element = self._find_card_by_key(key=key, presence=True, close_search=False, into=into)
        self._click_webelement(element=element)
        self._check_element_visible(locator=title_locator)
        match input_check_type:
            case "value":
                self._check_element_value(locator=input_locator, value=key)

            case "text":
                self._check_element_text(locator=input_locator, text=key)

    def _delete_card(self, key: str, confirm: bool, into: str, template: dict = None):
        if key is None:
            return

        cards = None
        button_delete = None
        confirm_window = None
        button_confirm_delete = None
        button_cancel_delete = None
        message_delete_success = None
        timeout = 1
        use_filters = False
        match into:
            case "events":
                cards = (By.XPATH, "//div[@class='solo_event_data_block__Header description']")
                button_delete = (By.XPATH, "./../../..//button[@class='RemoveImage']")
                confirm_window = (By.XPATH, "//h2[contains(text(), 'Вы действительно хотите удалить карточку "
                                            "события?')]")
                button_confirm_delete = (By.XPATH, "//span[contains(text(), 'Подтвердить')]/parent::button")
                button_cancel_delete = (By.XPATH, "//span[contains(text(), 'Отменить')]/parent::button")
                message_delete_success = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), "
                                                    "'Карточка удалена успешно')]")
            case "objects_communal":
                cards = (By.XPATH, "//div[@class='solo_Card_wrapper__header__info_header']")
                button_delete = (By.XPATH, "./../..//img[@data-testid='card-remove']")
                confirm_window = (By.XPATH, "//h2[contains(text(), 'Вы действительно хотите удалить объект ЖКХ?')]")
                button_confirm_delete = (By.XPATH, "//span[contains(text(), 'Удалить')]/parent::button")
                button_cancel_delete = (By.XPATH, "//span[contains(text(), 'Отмена')]/parent::button")
                message_delete_success = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), "
                                                    "'Объект ЖКХ удален успешно')]")

            case "users":
                cards = (By.XPATH, "//tbody/tr/td[1]/div")
                button_delete = (By.XPATH, "./../..//div[@class='row-action-buttons']")
                confirm_window = (By.XPATH, "//h6[contains(text(), 'Подтвердите удаление пользователя')]")
                button_confirm_delete = (By.XPATH, "//span[contains(text(), 'Подтвердить')]/parent::button")
                button_cancel_delete = (By.XPATH, "//span[contains(text(), 'Отмена')]/parent::button")
                message_delete_success = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), "
                                                    "'Пользователь удален успешно')]")
                timeout = 5

            case "objects_housing":
                cards = (By.XPATH, "//div[contains(@class, '_icon_small')]//div[contains(@class, '__info_text')]")
                button_delete = (By.XPATH, "./../../../../img[@data-testid='card-remove']")
                confirm_window = (By.XPATH, "//h2[contains(text(), 'Вы действительно хотите удалить объект ЖФ?')]")
                button_confirm_delete = (By.XPATH, "//span[contains(text(), 'Удалить')]/parent::button")
                button_cancel_delete = (By.XPATH, "//span[contains(text(), 'отмена')]/parent::button")
                message_delete_success = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), "
                                                    "'Объект жил. фонда удален успешно')]")
                use_filters = True
                self._filter_by_feature(filter_type='address', template=template)

            case "organizations":
                cards = (By.XPATH, "//div[contains(text(), 'Наименование организации')]/div")
                button_delete = (By.XPATH, "./../../../..//img[@data-testid='card-remove']")
                confirm_window = (By.XPATH, "//h2[contains(text(), 'Вы действительно хотите удалить "
                                            "выбранной организации?')]")
                button_confirm_delete = (By.XPATH, "//span[contains(text(), 'Удалить')]/parent::button")
                button_cancel_delete = (By.XPATH, "//span[contains(text(), 'Отмена')]/parent::button")
                message_delete_success = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), "
                                                    "'Организация удалена успешно')]")

            case "plans_events":
                cards = (By.XPATH, "//div[contains(text(), 'Наименование плана')]/div")
                button_delete = (By.XPATH, "./../../../..//img[@data-testid='card-remove']")
                confirm_window = (By.XPATH, "//h2[contains(text(), 'Вы действительно хотите удалить "
                                            "выбранный план мероприятий?')]")
                button_confirm_delete = (By.XPATH, "//span[contains(text(), 'Удалить')]/parent::button")
                button_cancel_delete = (By.XPATH, "//span[contains(text(), 'Отмена')]/parent::button")
                message_delete_success = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), "
                                                    "'План мероприятий удален успешно')]")
                use_filters = True
                self._filter_by_feature(filter_type='cost_high', template=template)

            case "plans_standard":
                cards = (By.XPATH, "//div[contains(text(), 'Наименование мероприятия')]/div")
                button_delete = (By.XPATH, "./../../../..//img[@data-testid='card-remove']")
                confirm_window = (By.XPATH, "//h2[contains(text(), 'Вы действительно хотите удалить "
                                            "выбранный план мероприятий?')]")
                button_confirm_delete = (By.XPATH, "//span[contains(text(), 'Удалить')]/parent::button")
                button_cancel_delete = (By.XPATH, "//span[contains(text(), 'Отмена')]/parent::button")
                message_delete_success = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), "
                                                    "'План мероприятий удален успешно')]")
                use_filters = True
                self._filter_by_feature(filter_type='sphere_gkh', template=template)

            case "heating_seasons":
                cards = (By.XPATH, "//div[contains(text(), 'Муниципальное образование')]/div")
                button_delete = (By.XPATH, "./../../../..//img[@data-testid='card-remove']")
                button_confirm_delete = (By.XPATH, "//span[contains(text(), 'Удалить')]/parent::button")
                confirm_window = (By.XPATH, "//h2[contains(text(), 'Вы действительно хотите удалить "
                                            "выбранный отопительный сезон?')]")
                button_cancel_delete = (By.XPATH, "//span[contains(text(), 'Отмена')]/parent::button")
                # message_delete_success = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), "
                #                                     "'План мероприятий удален успешно')]")

            case "documents_npa":
                cards = (By.XPATH, "//div[contains(text(), 'Наименование документа')]/div")
                button_delete = (By.XPATH, "./../../../..//img[@data-testid='card-remove']")
                confirm_window = (By.XPATH, "//h2[contains(text(), 'Вы действительно хотите удалить справочный документ?')]")
                button_confirm_delete = (By.XPATH, "//span[contains(text(), 'Удалить')]/parent::button")
                button_cancel_delete = (By.XPATH, "//span[contains(text(), 'Отмена')]/parent::button")
                # message_delete_success = (By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), "
                #                                     "'План мероприятий удален успешно')]")
                use_filters = True
                self._filter_by_feature(filter_type='type_document', template=template)

        self._check_element_visible(locator=cards)
        elements = self._find_elements_visible(locator=cards)
        base = self._get_element_by_text(elements=elements, text=key, strict_mode=True)
        element = self._find_element_from_base(base=base, locator=button_delete)
        self._check_webelement_visible(element=element)
        self._click_webelement(element=element)
        self._check_element_visible(locator=confirm_window)
        if confirm:
            element = self._check_element_visible(locator=button_confirm_delete)
            check_func = self._check_no_elements_by_text
        else:
            element = self._check_element_visible(locator=button_cancel_delete)
            check_func = self._get_element_by_text
        self._click_webelement(element=element)

        if message_delete_success is not None:  # TODO: Удалить когда подтверждение будеть реализовано в интерфейсе (Реестр учета ОС)
            self._check_element_visible(locator=message_delete_success, visibility=confirm)

        self._check_element_visible(locator=confirm_window, visibility=False)

        if use_filters:
            self._filters_clear(close_panel=True)

        time.sleep(timeout)
        elements = self._find_elements_visible(locator=cards)
        check_func(elements=elements, text=key)

    def _filters_clear(self, close_panel: bool):
        if self._is_element_visible(locator=self.FILTERS_TITLE, visibility=False, timeout=3):
            self._check_element_visible(locator=self.FILTERS)
            self._click_element(locator=self.FILTERS)

        self._press_keyboard_key(key="PAGE DOWN")
        self._click_element(locator=self.FILTERS_BUTTON_CLEAR)

        if close_panel:
            self._click_element(locator=self.FILTERS)

    def _filter_by_feature(self, filter_type: str, template: dict):
        match filter_type:
            case "address":
                self._check_element_visible(locator=self.FILTERS, visibility=True)
                self._add_address(open_form_locator=self.FILTERS, address=template['address'], save=False)
                self._click_element(locator=self.FILTERS)

            case "sphere_gkh":
                self._check_element_visible(locator=self.FILTERS, visibility=True)
                self._click_element(locator=self.FILTERS)
                elements = self._find_elements_visible(locator=self.FILTER_SPHERE_GKH)
                element = self._get_element_by_text(elements=elements, text=template['SphereGKH'])
                self._click_element(locator=element)

            case "cost_high":
                self._check_element_visible(locator=self.FILTERS, visibility=True)
                self._click_element(locator=self.FILTERS)
                self._fill_input(locator=self.FILTER_PRICE, value=template['PriceProject'])
                self._switch_sort(sort_type="Наименование плана (А-Я)")

            case "type_document":
                self._check_element_visible(locator=self.FILTERS, visibility=True)
                self._click_element(locator=self.FILTERS)
                TYPE_DOCUMENT = (By.XPATH, f"//div[contains(text(), 'Тип документа')]/..//span[contains(text(), '{template['TypeDocument']}')]")
                self._click_element(locator=TYPE_DOCUMENT)
                KIND_DOCUMENT = (By.XPATH, f"//div[contains(text(), 'Вид документа')]/..//span[contains(text(), '{template['KindDocument']}')]")
                self._click_element(locator=KIND_DOCUMENT)

    def _find_by_key(self, key: str, template: dict, presence: bool):
        CARDS = (By.XPATH, f"//div[contains(text(), '{template['AreaSearch']}')]/div")
        elements = self._find_elements_visible(locator=CARDS)
        if presence:
            return self._get_element_by_text(elements=elements, text=key)
        else:
            self._check_no_elements_by_text(elements=elements, text=key)

    def _open_by_key(self, key: str, template: dict):
        element = self._find_by_key(key=key, presence=True, template=template)
        self._click_webelement(element=element)