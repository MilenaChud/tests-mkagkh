import allure
import time
from selenium.webdriver.common.by import By
from core.main.sections.events.event_form_full import EventFormFull


class EventsPage(EventFormFull):
    # Locators
    TITLE = (By.XPATH, "//h1[contains(text(), 'Реестр аварий и инцидентов')]")
    BUTTON_ADD = (By.XPATH, "//span[contains(text(), 'Добавить')]/parent::button")
    EVENTS_KEYS = (By.XPATH, "//div[@class='solo_event_data_block__Header description']")

    def _goto(self):
        if self._is_element_visible(locator=EventsPage.TITLE, visibility=False, timeout=3):
            self._open(added_path="eventCard")
            with allure.step("Check events page title"):
                self._check_element_visible(locator=EventsPage.TITLE)
        return self

    def _smart_open(self, credentials: dict):
        self._auth.smart_login(credentials=credentials)
        self._goto()

    def _find_event_by_key(self, key: str, presence: bool):
        elements = self._find_elements_visible(locator=self.EVENTS_KEYS)
        if presence:
            return self._get_element_by_text(elements=elements, text=key)
        else:
            self._check_no_elements_by_text(elements=elements, text=key)

    def _open_event_by_key(self, key: str):
        element = self._find_event_by_key(key=key, presence=True)
        self._click_webelement(element=element)
        self._check_description(key=key)

    def _check_event_alarm(self, key: str, alarm_scale: str):
        alarm_locator = (By.XPATH, f"//div[contains(text(), '{key}')]/ancestor::div[@class='issueLink']"
                                   f"//div[@class='solo_event_data_block__Header description alarm']")
        match alarm_scale:
            case "Локальный":
                self._check_element_text(locator=alarm_locator, text="Угроза: ЧС локального масштаба")
            case "Местный" | "Муниципальный":
                self._check_element_text(locator=alarm_locator, text="Угроза: ЧС местного (муниципального) масштаба")
            case "Территориальный" | "Межмуниципальный" | "Региональный":
                self._check_element_text(locator=alarm_locator, text="Угроза: ЧС территориального (межмуниципального "
                                                                     "и регионального) масштаба")
            case _:
                self._check_element_visible(locator=alarm_locator, visibility=False)

    def _check_event_agree_status(self, key: str, agree_status: str, open_event: bool = False):
        agree_status_locator = (By.XPATH, f"//div[contains(text(), '{key}')]/../.."
                                          f"//div[contains(text(), 'Статус подтверждения:')]/..//span")
        element = self._check_element_visible(locator=agree_status_locator)
        self._check_webelement_text(element=element, text=agree_status)
        if open_event:
            self._click_webelement(element=element)
            self._check_description(key=key)
