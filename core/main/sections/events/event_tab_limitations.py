import time
from selenium.webdriver.common.by import By
from core.main.sections.events.event_tabs_common import EventTabsCommon


class EventTabLimitations(EventTabsCommon):
    # Locators
    BUTTON_ADD_LIMITATIONS = (By.XPATH, "//span[contains(text(), 'Добавить ограничение')]/parent::button")
    LIMITATION_TITLE_ADD = (By.XPATH, "//h6[contains(text(), 'Добавить ограничение для ЖКХ')]")
    LIMITATION_TITLE_EDIT = (By.XPATH, "//h6[contains(text(), 'Редактировать ограничение для ЖКХ')]")
    LIMITATION_TYPE = (By.XPATH, "//label[contains(text(), 'Тип ограничения')]/.."
                                 "//div[@id='mui-component-select-limitTypeList']")
    LIMITATION_TYPE_OPTIONS = (By.XPATH, "//ul[@aria-labelledby='limitType']/li")
    LIMITATION_AREA = (By.XPATH, "//label[contains(text(), 'Сфера ЖКХ')]/..//div[@id='sphereService']")
    LIMITATION_AREA_OPTIONS = (By.XPATH, "//ul[@aria-labelledby='sphereServiceLabel']/li/div/span")
    LIMITATION_DATE_TIME_ON = (By.XPATH, "//label[contains(text(), 'Дата установки ограничения')]/..//input")
    LIMITATION_DATE_TIME_OFF = (By.XPATH, "//label[contains(text(), 'Дата снятия ограничения')]/..//input")
    LIMITATION_DATE_TIME_CONFIRM = (By.XPATH, "//span[contains(text(), 'OK')]/parent::button")
    LIMITATION_ADDRESS_ROWS = (By.XPATH, "//label[contains(text(), 'Населенные пункты')]/../../../ul/li/div/div/span")
    LIMITATION_ADDRESS_BUTTON_ADD = (By.XPATH, "//span[contains(text(), 'Добавить адрес')]/../../..//button")
    LIMITATION_ADDRESS_TITLE = (By.XPATH, "//h2[contains(text(), 'Введите адрес')]")
    LIMITATION_ADDRESS_PLACE = (By.XPATH, "//label[contains(text(), 'Населенный пункт')]/..//input")
    LIMITATION_ADDRESS_STREET = (By.XPATH, "//label[contains(text(), 'Улица')]/..//input")
    LIMITATION_ADDRESS_HOUSE = (By.XPATH, "//label[contains(text(), 'Дом')]/..//input")
    LIMITATION_ADDRESS_BUTTON_SAVE = (By.XPATH, "//h2[contains(text(), 'Введите адрес')]/../.."
                                                "//span[contains(text(), 'Сохранить')]/parent::button")
    LIMITATION_MAJOR_OBJECTS = (By.XPATH, "//label[contains(text(), 'Перечень значимых обьектов')]/..//input")
    LIMITATION_MULTI_HOUSES = (By.XPATH, "//label[contains(text(), 'Многоквартирные')]/..//input")
    LIMITATION_MULTI_PEOPLE = (By.XPATH, "//label[contains(text(), 'Многоквартирные')]/../.."
                                         "/following-sibling::div[1]//input")
    LIMITATION_SINGLE_HOUSES = (By.XPATH, "//label[contains(text(), 'Индивидуальные')]/..//input")
    LIMITATION_SINGLE_PEOPLE = (By.XPATH, "//label[contains(text(), 'Индивидуальные')]/../.."
                                          "/following-sibling::div[1]//input")
    LIMITATION_OTHER_OBJECTS = (By.XPATH, "//label[contains(text(), 'Перечень иных обьектов')]/..//input")
    LIMITATION_BUTTON_CLOSE = (By.XPATH, "//div[@class='MuiDialogActions-root MuiDialogActions-spacing']"
                                         "//span[contains(text(), 'Закрыть')]/parent::button")
    LIMITATION_BUTTON_SAVE = (By.XPATH, "//div[@class='MuiDialogActions-root MuiDialogActions-spacing']"
                                        "//span[contains(text(), 'Сохранить')]/parent::button")
    LIMITATION_DELETE_TITLE = (By.XPATH, "//h6[contains(text(), 'Подтвердите удаление ограничения')]")
    LIMITATION_DELETE_BUTTON_CANCEL = (By.XPATH, "//h6[contains(text(), 'Подтвердите удаление ограничения')]/../.."
                                                 "//span[contains(text(), 'Отмена')]/parent::button")
    LIMITATION_DELETE_BUTTON_CONFIRM = (By.XPATH, "//h6[contains(text(), 'Подтвердите удаление ограничения')]/../.."
                                                  "//span[contains(text(), 'Подтвердить')]/parent::button")
    LIMITATIONS_TABLE_EMPTY = (By.XPATH, "//div[contains(text(), 'Список ограничений')]/.."
                                         "//tbody//td[contains(text(), 'Данных не найдено')]")
    LIMITATIONS_TABLE_LIST = (By.XPATH, "//div[contains(text(), 'Список ограничений')]/..//tbody/tr")
    LIMITATIONS_TABLE_LIST_EDIT = (By.XPATH, "//div[contains(text(), 'Список ограничений')]/.."
                                             "//tbody/tr[contains(@class, 'tableRow')]"
                                             "[//td[contains(@class, 'RemoveButtonCell')]/button]")

    def _check_buttons(self, edit: bool):
        super()._check_buttons(edit=edit)
        if edit:
            self._check_element_visible(locator=self.BUTTON_ADD_LIMITATIONS, visibility=True)
            self._check_element_editable(locator=self.BUTTON_ADD_LIMITATIONS, disabled=False)
        else:
            self._check_element_visible(locator=self.BUTTON_ADD_LIMITATIONS, visibility=False)

    def _check_elements_editable(self, edit: bool):
        if self._is_element_visible(locator=self.LIMITATIONS_TABLE_EMPTY, visibility=False, timeout=3):
            if edit:
                rows = self._find_elements_visible(locator=self.LIMITATIONS_TABLE_LIST)
                #rows_edit = self._find_elements_visible(locator=self.LIMITATIONS_TABLE_LIST_EDIT)
                #assert len(rows_edit) == len(rows)
            else:
                self._check_element_visible(locator=self.LIMITATIONS_TABLE_LIST_EDIT, visibility=False)

    def _find_by_type(self, limitation_type: str):
        if self._is_element_visible(locator=self.LIMITATIONS_TABLE_EMPTY, visibility=False, timeout=3):
            rows = self._find_elements_visible(locator=self.LIMITATIONS_TABLE_LIST)
            found = False
            index = 0
            while (not found) and (index < len(rows)):
                type_locator = (By.XPATH, f"//div[contains(text(), 'Список ограничений')]/..//tbody"
                                          f"//tr[{index + 1}]/td[1]")
                row_type = self._check_element_visible(locator=type_locator)
                found = (row_type.text == limitation_type)
                index += 1
            if not found:
                index = -1
        else:
            index = -1
        return index

    def _get_form_data(self, empty: bool):
        def reverse_date_time(date_time: str):  # TODO: Remove
            if date_time != "":
                date_time_new = f"{date_time[6:10]}-{date_time[3:5]}-{date_time[0:2]} " \
                                f"{date_time[11:13]}:{date_time[14:16]}"
            else:
                date_time_new = ""
            return date_time_new

        if empty:
            data = {"NoData": "Данных не найдено"}
        else:
            _type = self._find_element(locator=self.LIMITATION_TYPE).text
            _addresses = ""
            elements = self._find_elements_visible(locator=self.LIMITATION_ADDRESS_ROWS)
            for element in elements[:-1]:
                if _addresses == "":
                    _addresses += element.text
                else:
                    _addresses += f", {element.text}"
            _date_time_on = self._get_element_attribute(locator=self.LIMITATION_DATE_TIME_ON, attr_name='value')
            _date_time_on = reverse_date_time(_date_time_on)  # TODO: Remove - Temporary date_time correction
            _date_time_off = self._get_element_attribute(locator=self.LIMITATION_DATE_TIME_OFF, attr_name='value')
            if _date_time_off != "":
                _date_time_on = f"{_date_time_on}\n",
                _date_time_off = reverse_date_time(_date_time_off)  # TODO: Remove - Temporary date_time correction
            _major_objects = self._get_element_attribute(locator=self.LIMITATION_MAJOR_OBJECTS, attr_name='value')
            _multi_houses = self._get_element_attribute(locator=self.LIMITATION_MULTI_HOUSES, attr_name='value')
            _multi_people = self._get_element_attribute(locator=self.LIMITATION_MULTI_PEOPLE, attr_name='value')
            _single_houses = self._get_element_attribute(locator=self.LIMITATION_SINGLE_HOUSES, attr_name='value')
            _single_people = self._get_element_attribute(locator=self.LIMITATION_SINGLE_PEOPLE, attr_name='value')
            _other_objects = self._get_element_attribute(locator=self.LIMITATION_OTHER_OBJECTS, attr_name='value')
            data = {
                "Type": _type,
                "Addresses": _addresses,
                "DateTimeOnOff": f"{_date_time_on}{_date_time_off}",
                "MajorObjects": _major_objects,
                "EmergencyData":
                {
                    "MultiHouses": _multi_houses,
                    "MultiPeople": _multi_people,
                    "SingleHouses": _single_houses,
                    "SinglePeople": _single_people
                },
                "OtherObjects": _other_objects
            }
        return data

    def _get_table_data(self):
        data_list = []
        rows = self._find_elements_visible(locator=self.LIMITATIONS_TABLE_LIST)
        td_locator = (By.XPATH, f"//div[contains(text(), 'Список ограничений')]/..//tbody//tr[1]/td")
        cells = self._find_elements_visible(locator=td_locator)
        if len(cells) == 1:
            data = {"NoData": cells[0].text}
            data_list.append(data)
        else:
            for index in range(len(rows)):
                if index > 0:
                    td_locator = (By.XPATH, f"//div[contains(text(), 'Список ограничений')]/../"
                                            f"/tbody//tr[{index + 1}]/td")
                    cells = self._find_elements_visible(locator=td_locator)
                data = {  # TODO: Возможно для ограничения с типом "Связанное" придется проверять Сферу ЖКХ (Area)
                    "Type": cells[0].text,
                    "Addresses": cells[1].text,
                    "DateTimeOnOff": cells[2].text,
                    "MajorObjects": cells[3].text,
                    "EmergencyData":
                    {
                        "MultiHouses": cells[4].text,
                        "MultiPeople": cells[5].text,
                        "SingleHouses": cells[6].text,
                        "SinglePeople": cells[7].text
                    },
                    "OtherObjects": cells[8].text
                }
                data_list.append(data)
        return data_list

    def _check_data(self, template: list):
        def sort_by_type(unsorted: list):
            result = list(unsorted)
            if len(unsorted) > 1:
                result = sorted(unsorted, key=lambda item: item['Type'])
            return result

        time.sleep(1)
        data = self._get_table_data()
        assert sort_by_type(data) == sort_by_type(template)

    def _fill_data(self, template: dict, limitation_save: bool, save: bool):
        # time.sleep(1)
        result = ""
        self._check_buttons(edit=False)
        self._check_elements_editable(edit=False)
        self._click_element(locator=self.BUTTON_EDIT)
        self._check_buttons(edit=True)
        self._check_elements_editable(edit=True)
        self._click_element(locator=self.BUTTON_ADD_LIMITATIONS)
        self._check_element_visible(locator=self.LIMITATION_TITLE_ADD)
        self._click_element(locator=self.LIMITATION_TYPE)
        elements = self._find_elements_visible(locator=self.LIMITATION_TYPE_OPTIONS)
        element = self._get_element_by_text(elements=elements, text=template['Type'])
        self._click_webelement(element=element)
        if template['Type'] == "Связанное":
            self._click_element(locator=self.LIMITATION_AREA)
            elements = self._find_elements_visible(locator=self.LIMITATION_AREA_OPTIONS)
            element = self._get_element_by_text(elements=elements, text=template['Area'])
            self._click_webelement(element=element)
            self._press_keyboard_key(key="TAB")
        self._click_element(locator=self.LIMITATION_DATE_TIME_ON)
        self._click_element(locator=self.LIMITATION_DATE_TIME_CONFIRM)
        for address in template['AddressesList']:
            self._add_address(open_form_locator=self.LIMITATION_ADDRESS_BUTTON_ADD, address=address)

        self._fill_input(locator=self.LIMITATION_MAJOR_OBJECTS, value=template['MajorObjects'])
        self._fill_input(locator=self.LIMITATION_MULTI_HOUSES, value=template['EmergencyData']['MultiHouses'])
        self._fill_input(locator=self.LIMITATION_MULTI_PEOPLE, value=template['EmergencyData']['MultiPeople'])
        self._fill_input(locator=self.LIMITATION_SINGLE_HOUSES, value=template['EmergencyData']['SingleHouses'])
        self._fill_input(locator=self.LIMITATION_SINGLE_PEOPLE, value=template['EmergencyData']['SinglePeople'])
        self._fill_input(locator=self.LIMITATION_OTHER_OBJECTS, value=template['OtherObjects'])
        if limitation_save:
            self._click_element(locator=self.LIMITATION_BUTTON_SAVE)
        else:
            self._click_element(locator=self.LIMITATION_BUTTON_CLOSE)
        self._check_element_visible(locator=self.LIMITATION_TITLE_ADD, visibility=False)
        self._check_elements_editable(edit=True)
        # Сохранить время последнего ограничения в таблице:
        if limitation_save and save:
            rows = self._find_elements_visible(locator=self.LIMITATIONS_TABLE_LIST)
            row = len(rows)
            td_locator = (By.XPATH, f"//div[contains(text(), 'Список ограничений')]/..//tbody//tr[{row}]/td[3]")
            result = self._check_element_visible(locator=td_locator).text
        if save:
            self._click_element(locator=self.BUTTON_SAVE)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
        self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=save)
        self._check_buttons(edit=False)
        self._check_elements_editable(edit=False)
        time.sleep(1)  # Для гарантированного сохранения данных TODO: Возможно надо будет поискать другое решение
        return result

    def _delete_data(self, deleted_type: str, delete_confirm: bool, save: bool):
        index = self._find_by_type(limitation_type=deleted_type)
        if index > 0:
            self._check_buttons(edit=False)
            self._check_elements_editable(edit=False)
            self._click_element(locator=self.BUTTON_EDIT)
            self._check_buttons(edit=True)
            self._check_elements_editable(edit=True)
            button_delete_locator = (By.XPATH, f"//div[contains(text(), 'Список ограничений')]/..//tbody"
                                               f"//tr[{index}]/td[10]/button")
            self._click_element(locator=button_delete_locator)
            self._check_element_visible(locator=self.LIMITATION_DELETE_TITLE)
            if delete_confirm:
                self._click_element(locator=self.LIMITATION_DELETE_BUTTON_CONFIRM)
            else:
                self._click_element(locator=self.LIMITATION_DELETE_BUTTON_CANCEL)
            self._check_element_visible(locator=self.LIMITATION_DELETE_TITLE, visibility=False)
            if save:
                self._click_element(locator=self.BUTTON_SAVE)
            else:
                self._click_element(locator=self.BUTTON_CANCEL)
            self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=save)
            self._check_buttons(edit=False)
            self._check_elements_editable(edit=False)

    @staticmethod
    def _get_emergency_type(houses: int, people: int):
        if people > 0:  # TODO: Ask for proper calculation formula of emergency type depending on houses and people values
            result = "Угроза: ЧС"
        else:
            result = "Нет угрозы ЧС"
        return result

    def _edit_emergency_data(self, edited_type: str, multi_houses: int, multi_people: int, limitation_save: bool,
                             save: bool):
        index = self._find_by_type(limitation_type=edited_type)
        if index > 0:
            self._check_buttons(edit=False)
            self._check_elements_editable(edit=False)
            self._click_element(locator=self.BUTTON_EDIT)
            self._check_buttons(edit=True)
            self._check_elements_editable(edit=True)
            type_locator = (By.XPATH, f"//div[contains(text(), 'Список ограничений')]/..//tbody//tr[{index}]/td[1]")
            self._click_element(locator=type_locator)
            self._check_element_visible(locator=self.LIMITATION_TITLE_EDIT)
            result = self._get_form_data(empty=False)
            self._fill_input(locator=self.LIMITATION_MULTI_HOUSES, value=str(multi_houses))
            self._fill_input(locator=self.LIMITATION_MULTI_PEOPLE, value=str(multi_people))
            if limitation_save:
                result_form = self._get_form_data(empty=False)
                self._click_element(locator=self.LIMITATION_BUTTON_SAVE)
            else:
                result_form = result
                self._click_element(locator=self.LIMITATION_BUTTON_CLOSE)
            self._check_element_visible(locator=self.LIMITATION_TITLE_EDIT, visibility=False)
            self._check_elements_editable(edit=True)
            if save:
                result = result_form
                self._click_element(locator=self.BUTTON_SAVE)
            else:
                self._click_element(locator=self.BUTTON_CANCEL)
            self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=save)
            self._check_buttons(edit=False)
            self._check_elements_editable(edit=False)
        else:
            result = {"NotFound": "Ограничение не найдено"}
        time.sleep(1)  # Для гарантированного сохранения данных TODO: Возможно надо будет поискать другое решение
        return result

    def _add_to_list(self, current_list: list, added: dict):
        result = list(current_list)
        added_temp = added
        if len(result) == 0:
            result.append(added_temp)
        elif "NoData" not in added_temp.keys():
            if "NoData" in result[0].keys():
                del result[0]

            addresses = ""
            for address in added_temp["AddressesList"]:
                if addresses == "":
                    addresses += address['Full']
                else:
                    addresses += f", {address['Full']}"
            added_temp["Addresses"] = addresses
            del added_temp["AddressesList"]
            del added_temp["DateTimeOn"]
            del added_temp["DateTimeOff"]
            if "Area" in added_temp.keys():
                del added_temp["Area"]

            result.append(added_temp)
        return result

    def _delete_from_list(self, current_list: list, deleted_type: str):
        result = list(current_list)
        if (len(result) > 0) and ("NoData" not in result[0].keys()):
            found = False
            index = 0
            while (not found) and (index < len(result)):
                found = (result[index]["Type"] == deleted_type)
                index += 1
            if found:
                del result[index - 1]
                if len(result) == 0:
                    result.append({"NoData": "Данных не найдено"})
        return result

    def _edit_list(self, current_list: list, edited: dict):
        result = list(current_list)
        if (len(result) > 0) and ("NoData" not in result[0].keys()) and ("NotFound" not in edited.keys()):
            found = False
            index = 0
            while (not found) and (index < len(result)):
                found = (result[index]["Type"] == edited["Type"])
                index += 1
            if found:
                result[index - 1] = edited
        return result
