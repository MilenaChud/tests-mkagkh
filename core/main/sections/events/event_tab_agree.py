import time
from selenium.webdriver.common.by import By
from core.main.sections.events.event_tabs_common import EventTabsCommon


class EventTabAgree(EventTabsCommon):
    # Locators
    APPROVE_PERSON = (By.XPATH, "//label[contains(text(), 'Согласующее лицо')]/..//input/parent::div")
    APPROVE_ORGANIZATION = (By.XPATH, "//label[contains(text(), 'Согласующая организация')]/..//input")
    APPROVE_DECLINE_REASON = (By.XPATH, "//label[contains(text(), 'Причина отклонения')]/..//input")
    APPROVE_REVISION_CHECKBOX = (By.XPATH, "//span[contains(text(), 'Отправить на доработку')]/..//input")
    APPROVE_BUTTON_SEND = (By.XPATH, "//span[contains(text(), 'Отправить на согласование')]/parent::button")
    APPROVE_BUTTON_ACCEPT = (By.XPATH, "//span[contains(text(), 'Согласовать')]/parent::button")
    APPROVE_BUTTON_DECLINE = (By.XPATH, "//span[contains(text(), 'Отклонить')]/parent::button")

    CONFIRM_PERSON = (By.XPATH, "//label[contains(text(), 'Утверждающее лицо')]/..//input/parent::div")
    CONFIRM_GKH_SEND_CHECKBOX = (By.XPATH, "//span[contains(text(), 'в Реформу ЖКХ')]/..//input/parent::span")
    CONFIRM_GKH_SEND_INPUT = (By.XPATH, "//span[contains(text(), 'в Реформу ЖКХ')]/..//input")
    CONFIRM_BUTTON_SEND = (By.XPATH, "//span[contains(text(), 'Отправить на утверждение')]/parent::button")
    CONFIRM_BUTTON_ACCEPT = (By.XPATH, "//span[contains(text(), 'Утвердить')]/parent::button")

    HISTORY_TABLE_LIST = (By.XPATH, "//label[contains(text(), 'История согласования')]/../..//tbody/tr")

    # TODO: Написать метод, проверяющий состояние кнопок

    def _send_to_responsible(self, responsible: dict, action: str):
        time.sleep(0.5)
        match action:
            case "На согласование":
                self._add_responsible(open_form_locator=self.APPROVE_PERSON, responsible=responsible)
                self._click_element(locator=self.APPROVE_BUTTON_SEND)
                self._check_element_visible(locator=self.APPROVE_BUTTON_SEND, visibility=False)

            case "На утверждение":
                self._add_responsible(open_form_locator=self.CONFIRM_PERSON, responsible=responsible)
                self._click_element(locator=self.CONFIRM_BUTTON_SEND)
                self._check_element_visible(locator=self.CONFIRM_BUTTON_SEND, visibility=False)

    def _accept_event(self, action: str, gkh_send_checkbox: bool = False):
        match action:
            case "Согласовать":
                self._click_element(locator=self.APPROVE_BUTTON_ACCEPT)
                self._check_element_visible(locator=self.APPROVE_BUTTON_ACCEPT, visibility=False)
                self._check_element_visible(locator=self.APPROVE_BUTTON_DECLINE, visibility=False)
                self._check_element_visible(locator=self.APPROVE_DECLINE_REASON, visibility=False)
                self._check_element_visible(locator=self.APPROVE_REVISION_CHECKBOX, visibility=False)

            case "Утвердить":
                if gkh_send_checkbox:
                    self._click_element(locator=self.CONFIRM_GKH_SEND_CHECKBOX)
                self._click_element(locator=self.CONFIRM_BUTTON_ACCEPT)
                self._check_element_visible(locator=self.CONFIRM_BUTTON_ACCEPT, visibility=False)
                self._check_element_editable(locator=self.CONFIRM_GKH_SEND_INPUT, disabled=True)

    def _check_history(self, template_list: list):
        time.sleep(3)  # TODO: Подумать над другим вариантом задержки, без явного применения sleep
        history_list = []
        rows = self._find_elements_visible(locator=self.HISTORY_TABLE_LIST)
        td_locator = (By.XPATH, f"//label[contains(text(), 'История согласования')]/../..//tbody//tr[1]/td")
        cells = self._find_elements_visible(locator=td_locator)
        if len(cells) == 1:
            history_line = {"NoData": cells[0].text}
            history_list.append(history_line)
        else:
            for index in range(len(rows)):
                if index > 0:
                    td_locator = (By.XPATH, f"//label[contains(text(), 'История согласования')]/../.."
                                            f"//tbody//tr[{index + 1}]/td")
                    cells = self._find_elements_visible(locator=td_locator)
                history_line = {
                    "Phase": cells[0].text,
                    "Status": cells[1].text,
                    "DeclineReason": cells[3].text,
                    "Responsible": cells[4].text.strip()
                }
                history_list.append(history_line)
        assert history_list == template_list

    def _add_to_list(self, current_list: list, added: dict):  # TODO: Возможно этот метод надо будет перенести выше
        result = list(current_list)
        if (len(result) > 0) and ("NoData" in result[0].keys()):
            del result[0]
        result.append(added)
        return result
