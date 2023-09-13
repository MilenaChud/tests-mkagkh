import allure
import time
from selenium.webdriver.common.by import By
from core.helpers.base_helper import BaseHelper


class AppNotifHelper(BaseHelper):
    PANEL_TITLES = (By.XPATH, "//h6[contains(text(), 'Уведомления') or contains(text(), 'Журнал уведомлений')]")
    PANEL_TITLE_JOURNAL = (By.XPATH, "//h6[contains(text(), 'Журнал уведомлений')]")
    PANEL_BUTTON_OPEN = (By.XPATH, "//button[contains(@class, 'notificationMainBuble')]")
    PANEL_BUTTON_CLOSE = (By.XPATH, "//h6[contains(text(), 'Уведомления') or contains(text(), 'Журнал уведомлений')]/.."
                                    "/div[1]/button[2]")
    PANEL_BUTTON_JOURNAL_OPEN = (By.XPATH, "//span[contains(text(), 'Журнал')]/parent::button")
    PANEL_BUTTON_JOURNAL_CLOSE = (By.XPATH, "//h6[contains(text(), 'Журнал уведомлений')]/button")
    PANEL_BUTTON_READ_ALL = (By.XPATH, "//span[contains(text(), 'Прочитать все')]/parent::button")
    PANEL_BUTTON_READ_NOTE = (By.XPATH, "./..//span[text()='Прочитать']/parent::button")
    PANEL_NOTES_NEW = (By.XPATH, "//h6[contains(text(), 'Уведомления')/../ul//span/span")

    def _open_panel(self):
        if self._is_element_visible(locator=self.PANEL_TITLES, visibility=False, timeout=3):
            self._click_element(locator=self.PANEL_BUTTON_OPEN)
            self._check_element_visible(locator=self.PANEL_TITLES, visibility=True, timeout=3)
        return self

    def _close_panel(self):
        if self._is_element_visible(locator=self.PANEL_TITLES, visibility=True, timeout=3):
            self._click_element(locator=self.PANEL_BUTTON_CLOSE)
            self._check_element_visible(locator=self.PANEL_TITLES, visibility=False, timeout=3)
        return self

    def _open_journal(self):
        if self._is_element_visible(locator=self.PANEL_TITLE_JOURNAL, visibility=False, timeout=3):
            self._click_element(locator=self.PANEL_BUTTON_JOURNAL_OPEN)
            self._check_element_visible(locator=self.PANEL_TITLE_JOURNAL, visibility=True, timeout=3)
        return self

    def _close_journal(self):
        if self._is_element_visible(locator=self.PANEL_TITLE_JOURNAL, visibility=True, timeout=3):
            self._click_element(locator=self.PANEL_BUTTON_JOURNAL_CLOSE)
            self._check_element_visible(locator=self.PANEL_TITLE_JOURNAL, visibility=False, timeout=3)
        return self

    def _find_notes_by_keys(self, keys: str, max_notes: int = -1):
        result = []
        keys_tuple = tuple(keys.split("; "))
        keys_len = len(keys_tuple)
        if max_notes > 0:
            notes_locator = (By.XPATH, f"(//h6[contains(text(), 'Уведомления') or "
                                       f"contains(text(), 'Журнал уведомлений')]/.."
                                       f"/ul//span/span)[position()<={max_notes}]")
        else:
            notes_locator = (By.XPATH, f"//h6[contains(text(), 'Уведомления') or "
                                       f"contains(text(), 'Журнал уведомлений')]/.."
                                       f"/ul//span/span")
        elements = self._find_elements_visible(locator=notes_locator)
        for element in elements:
            flag = True
            index = 0
            while flag and (index < keys_len):
                flag = (keys_tuple[index] in element.text)
                index += 1
            if flag:
                result.append(element)
        if len(result) > 0:
            return result
        else:
            self._logger.error(msg=f"Assertion Error: Can't find notes with keys {keys}")
            self._attach_screenshot()
            raise AssertionError(f"Can't find notes with keys {keys}")

    def _read_notes_from_list(self, notes: list):
        for note in notes:
            time.sleep(0.5)
            button_read = self._find_element_from_base(base=note, locator=self.PANEL_BUTTON_READ_NOTE)
            self._click_webelement(element=button_read)
        return self

    def _read_notes_all(self):
        self._click_element(locator=self.PANEL_BUTTON_READ_ALL)
        self._check_element_visible(locator=self.PANEL_NOTES_NEW, visibility=False, timeout=3)
        return self

    def _get_notes_by_keys(self, keys: str, max_notes: int, close_panel: bool = True):
        notes_new = self._open_panel()._find_notes_by_keys(keys=keys, max_notes=max_notes)
        self._read_notes_from_list(notes=notes_new)
        notes_read = self._open_journal()._find_notes_by_keys(keys=keys, max_notes=max_notes)
        self._close_journal()
        if close_panel:
            self._close_panel()
        return notes_new, notes_read
