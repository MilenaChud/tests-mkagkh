import time
from selenium.webdriver.common.by import By
from core.main.sections.events.event_tabs_common import EventTabsCommon


class EventTabAdditional(EventTabsCommon):
    # Locators
    BUTTON_ADD_RESPONSIBLE = (By.XPATH, "//div[contains(text(), 'Ответственные лица')]/../../.."
                                        "//span[contains(text(), 'Добавить')]/parent::button")
    BUTTON_ADD_PLAN = (By.XPATH, "//label[contains(text(), 'Планы мероприятий')]/../.."
                                 "//span[contains(text(), 'Добавить')]/parent::button")
    RESPONSIBLE_DELETE_TITLE = (By.XPATH, "//h2[contains(text(), 'Удалить ответственное лицо?')]")
    RESPONSIBLE_DELETE_BUTTON_CANCEL = (By.XPATH, "//h2[contains(text(), 'Удалить ответственное лицо?')]/../.."
                                                  "//span[contains(text(), 'отмена')]/parent::button")
    RESPONSIBLE_DELETE_BUTTON_CONFIRM = (By.XPATH, "//h2[contains(text(), 'Удалить ответственное лицо?')]/../.."
                                                   "//span[contains(text(), 'Удалить')]/parent::button")
    RESPONSIBLES_TABLE_EMPTY = (By.XPATH, "//div[contains(text(), 'Ответственные лица')]/../../.."
                                          "//tbody//td[contains(text(), 'Данных не найдено')]")
    RESPONSIBLES_TABLE_LIST = (By.XPATH, "//div[contains(text(), 'Ответственные лица')]/../../..//tbody/tr")
    RESPONSIBLES_TABLE_LIST_EDIT = (By.XPATH, "//div[contains(text(), 'Ответственные лица')]/../../.."
                                              "//tbody/tr[//td//button]")
    RESPONSIBLES_TABLE_DELETE_LAST = (By.XPATH, "//span[contains(text(), 'Должен быть хотя бы один ответственный!')]")
    OTHER_INFO = (By.XPATH, "//label[contains(text(), 'Иная дополнительная информация')]/..//input")
    INFO_SOURCE = (By.XPATH, "//label[contains(text(), 'Источник оперативной информации')]/..//input")
    PLANS = (By.XPATH, "//label[contains(text(), 'Планы мероприятий')]/..//input")

    def _check_buttons(self, edit: bool):
        super()._check_buttons(edit=edit)
        if edit:
            self._check_element_visible(locator=self.BUTTON_ADD_RESPONSIBLE, visibility=True)
            self._check_element_editable(locator=self.BUTTON_ADD_RESPONSIBLE, disabled=False)
            self._check_element_visible(locator=self.BUTTON_ADD_PLAN, visibility=True)
            self._check_element_editable(locator=self.BUTTON_ADD_PLAN, disabled=False)
        else:
            self._check_element_visible(locator=self.BUTTON_ADD_RESPONSIBLE, visibility=True)
            self._check_element_editable(locator=self.BUTTON_ADD_RESPONSIBLE, disabled=True)
            self._check_element_visible(locator=self.BUTTON_ADD_PLAN, visibility=True)
            self._check_element_editable(locator=self.BUTTON_ADD_PLAN, disabled=True)

    def _check_elements_editable(self, edit: bool):
        if self._is_element_visible(locator=self.RESPONSIBLES_TABLE_EMPTY, visibility=False, timeout=3):
            if edit:
                rows = self._find_elements_visible(locator=self.RESPONSIBLES_TABLE_LIST)
                rows_edit = self._find_elements_visible(locator=self.RESPONSIBLES_TABLE_LIST_EDIT)
                assert len(rows_edit) == len(rows)
            else:
                self._check_element_visible(locator=self.RESPONSIBLES_TABLE_LIST_EDIT, visibility=False)
        if edit:
            self._check_element_editable(locator=self.OTHER_INFO, disabled=False)
        else:
            self._check_element_editable(locator=self.OTHER_INFO, disabled=True)
        self._check_element_editable(locator=self.INFO_SOURCE, disabled=True)
        self._check_element_editable(locator=self.PLANS, disabled=True)

    def _find_row_to_use(self, responsible: dict):
        rows = 0
        if self._is_element_visible(locator=self.RESPONSIBLES_TABLE_EMPTY, visibility=False, timeout=3):
            expected = (responsible['Organization'], responsible['Position'], responsible['FullName'])
            elements = self._find_elements_visible(locator=self.RESPONSIBLES_TABLE_LIST)
            rows = len(elements)
            found = False
            row = 0
            while (not found) and (row < rows):
                row += 1
                col = 1
                flag = True
                while flag and (col <= len(expected)):
                    td_locator = (By.XPATH, f"//div[contains(text(), 'Ответственные лица')]/../../.."
                                            f"//tbody//tr[{row}]/td{[col]}")
                    td_text = self._check_element_visible(locator=td_locator).text.strip()
                    flag = (td_text == expected[col - 1])
                    col += 1
                found = flag
            if not found:
                row = -1
        else:
            row = -1
        return row, rows

    def _get_responsibles_list(self):
        responsibles_list = []
        rows = self._find_elements_visible(locator=self.RESPONSIBLES_TABLE_LIST)
        td_locator = (By.XPATH, f"//div[contains(text(), 'Ответственные лица')]/../../..//tbody//tr[1]/td")
        cells = self._find_elements_visible(locator=td_locator)
        if len(cells) == 1:
            responsible = {"NoData": cells[0].text}
            responsibles_list.append(responsible)
        else:
            for index in range(len(rows)):
                if index > 0:
                    td_locator = (By.XPATH, f"//div[contains(text(), 'Ответственные лица')]/../../.."
                                            f"//tbody//tr[{index + 1}]/td")
                    cells = self._find_elements_visible(locator=td_locator)
                responsible = {
                    "Organization": cells[0].text,
                    "Position": cells[1].text,
                    "FullName": cells[2].text
                }
                responsibles_list.append(responsible)
        return responsibles_list

    def _get_data(self):
        _responsibles_list = self._get_responsibles_list()
        _other_info = self._get_element_attribute(locator=self.OTHER_INFO, attr_name="value")
        _info_source = self._get_element_attribute(locator=self.INFO_SOURCE, attr_name="value")
        _plans = self._get_element_attribute(locator=self.PLANS, attr_name="value")
        data = {
            "Responsibles": _responsibles_list,
            "Inputs":
            {
                "OtherInfo": _other_info,
                "InfoSource": _info_source,
                "Plans": _plans
            }
        }
        return data

    def _check_responsibles(self, template_list: list):
        def sort_by_keys(unsorted: list):
            result = list(unsorted)
            if len(unsorted) > 1:
                result = sorted(unsorted,
                                key=lambda item: f"{item['Organization']} {item['Position']} {item['FullName']}")
            return result

        responsibles_list = self._get_responsibles_list()
        assert sort_by_keys(responsibles_list) == sort_by_keys(template_list)

    def _check_inputs(self, template: dict):
        self._check_element_value(locator=self.OTHER_INFO, value=template['OtherInfo'])
        self._check_element_value(locator=self.INFO_SOURCE, value=template['InfoSource'])
        self._check_element_value(locator=self.PLANS, value=template['Plans'])

    def _fill_data(self, template: dict, save: bool):
        # time.sleep(1)
        self._check_buttons(edit=False)
        self._check_elements_editable(edit=False)
        self._press_keyboard_key(key="PAGE UP")
        # time.sleep(0.5)
        self._click_element(locator=self.BUTTON_EDIT)
        self._check_buttons(edit=True)
        self._check_elements_editable(edit=True)

        for responsible in template['Responsibles']:
            time.sleep(0.5)
            self._add_responsible(open_form_locator=self.BUTTON_ADD_RESPONSIBLE, responsible=responsible)

        # time.sleep(0.5)
        self._fill_input(locator=self.OTHER_INFO, value=template['Inputs']['OtherInfo'])

        if save:
            element = self._check_element_visible(locator=self.BUTTON_SAVE)
        else:
            element = self._check_element_visible(locator=self.BUTTON_CANCEL)

        # self._press_keyboard_key(key="CTRL + END")
        self._press_keyboard_key(key="PAGE DOWN")
        # time.sleep(0.5)

        self._click_webelement(element=element)
        self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=save)
        self._check_buttons(edit=False)
        self._check_elements_editable(edit=False)

        time.sleep(1)  # Для гарантированного сохранения данных TODO: Возможно надо будет поискать другое решение

    def _delete_table_row(self, deleted: dict, delete_confirm: bool, save: bool):
        row, rows = self._find_row_to_use(responsible=deleted)
        if row > 0:
            self._check_buttons(edit=False)
            self._check_elements_editable(edit=False)
            self._press_keyboard_key(key="PAGE UP")
            time.sleep(0.5)
            self._click_element(locator=self.BUTTON_EDIT)
            self._check_buttons(edit=True)
            self._check_elements_editable(edit=True)
            button_delete_locator = (By.XPATH, f"//div[contains(text(), 'Ответственные лица')]/../../..//tbody"
                                               f"//tr[{row}]/td[6]//button")
            self._click_element(locator=button_delete_locator)
            self._check_element_visible(locator=self.RESPONSIBLE_DELETE_TITLE)
            if delete_confirm:
                self._click_element(locator=self.RESPONSIBLE_DELETE_BUTTON_CONFIRM)
                # if rows == 1:
                #     self._check_element_visible(locator=self.RESPONSIBLES_TABLE_DELETE_LAST)
            else:
                self._click_element(locator=self.RESPONSIBLE_DELETE_BUTTON_CANCEL)
            self._check_element_visible(locator=self.RESPONSIBLE_DELETE_TITLE, visibility=False)
            if save:
                element = self._check_element_visible(locator=self.BUTTON_SAVE)
            else:
                element = self._check_element_visible(locator=self.BUTTON_CANCEL)
            self._press_keyboard_key(key="PAGE DOWN")
            time.sleep(0.5)
            self._click_webelement(element=element)
            self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=save)
            self._check_buttons(edit=False)
            self._check_elements_editable(edit=False)

    def _add_to_responsibles_list(self, current_list: list, added_list: list):
        result = list(current_list)
        if (len(result) > 0) and ("NoData" in result[0].keys()):
            del result[0]
        for element in added_list:
            if element not in result:
                result.append(element)
        return result

    def _delete_from_responsibles_list(self, current_list: list, deleted: dict):
        result = list(current_list)
        if len(result) > 1:  # Do not delete last responsible
            found = False
            index = 0
            while (not found) and (index < len(result)):
                found = (result[index]["Organization"] == deleted["Organization"]) and \
                        (result[index]["Position"] == deleted["Position"]) and \
                        (result[index]["FullName"] == deleted["FullName"])
                index += 1
            if found:
                del result[index - 1]
        return result
