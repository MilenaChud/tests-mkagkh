import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from core.helpers.app_sections_helper import AppSectionsHelper
from core.main.sections.events.event_tab_primary import EventTabPrimary
from core.main.sections.events.event_tab_properties import EventTabProperties
from core.main.sections.events.event_tab_object import EventTabObject
from core.main.sections.events.event_tab_limitations import EventTabLimitations
from core.main.sections.events.event_tab_additional import EventTabAdditional
from core.main.sections.events.event_tab_files import EventTabFiles
from core.main.sections.events.event_tab_emergency import EventTabEmergency
from core.main.sections.events.event_tab_agree import EventTabAgree


class EventFormFull(AppSectionsHelper):
    # Locators
    TITLE = (By.XPATH, "//h1[contains(text()[1], 'Карточка события') and contains(text()[2], 'на объекте ЖКХ')]")
    TAB_PRIMARY = (By.XPATH, "//div[contains(text(), 'Первичные данные')]/../parent::button")
    TAB_PROPERTIES = (By.XPATH, "//div[contains(text(), 'Характеристики')]/../parent::button")
    TAB_OBJECT = (By.XPATH, "//div[contains(text(), 'Объект')]/../parent::button")
    TAB_LIMITATIONS = (By.XPATH, "//div[contains(text(), 'Ограничения')]/../parent::button")
    TAB_ADDITIONAL = (By.XPATH, "//div[contains(text(), 'Дополнительно')]/../parent::button")
    TAB_FILES = (By.XPATH, "//span[contains(text(), 'Файлы')]/parent::button")
    TAB_EMERGENCY = (By.XPATH, "//span[contains(text(), 'Учёт режима ЧС')]/parent::button")
    TAB_AGREE = (By.XPATH, "//span[contains(text(), 'Согласование')]/parent::button")
    ATTENTION_BLOCK = (By.XPATH, "//div[@class='attentionBlock']")

    def _check_attention_block(self, presence: bool):
        self._check_element_visible(locator=self.ATTENTION_BLOCK, visibility=presence)

    def _check_tab_emergency(self, presence: bool):
        self._check_element_visible(locator=self.TAB_EMERGENCY, visibility=presence)

    def _is_tab_selected(self, tab_element: WebElement):
        result = (self._get_webelement_attribute(element=tab_element, attr_name="aria-selected") == "true")
        return result

    def _switch_tab(self, tab_name: str):
        self._check_element_visible(locator=EventFormFull.TITLE)

        tab_element = None
        tab_object = None
        match tab_name:
            case "ПЕРВИЧНЫЕ ДАННЫЕ":
                tab_element = self._check_element_clickable(locator=self.TAB_PRIMARY)
                tab_object = EventTabPrimary(driver=self._driver)

            case "ХАРАКТЕРИСТИКИ":
                tab_element = self._check_element_clickable(locator=self.TAB_PROPERTIES)
                tab_object = EventTabProperties(driver=self._driver)

            case "ОБЪЕКТ":
                tab_element = self._check_element_clickable(locator=self.TAB_OBJECT)
                tab_object = EventTabObject(driver=self._driver)

            case "ОГРАНИЧЕНИЯ":
                tab_element = self._check_element_clickable(locator=self.TAB_LIMITATIONS)
                tab_object = EventTabLimitations(driver=self._driver)

            case "ДОПОЛНИТЕЛЬНО":
                tab_element = self._check_element_clickable(locator=self.TAB_ADDITIONAL)
                tab_object = EventTabAdditional(driver=self._driver)

            case "ФАЙЛЫ":
                tab_element = self._check_element_clickable(locator=self.TAB_FILES)
                tab_object = EventTabFiles(driver=self._driver)

            case "УЧЁТ РЕЖИМА ЧС":
                tab_element = self._check_element_clickable(locator=self.TAB_EMERGENCY)
                tab_object = EventTabEmergency(driver=self._driver)

            case "СОГЛАСОВАНИЕ":
                tab_element = self._check_element_clickable(locator=self.TAB_AGREE)
                tab_object = EventTabAgree(driver=self._driver)

        with allure.step(f"Switch to tab {tab_name}"):
            self._logger.info(msg=f"Switch to tab {tab_name}")
            if self._is_tab_selected(tab_element=tab_element):
                return tab_object
            else:
                self._click_webelement(element=tab_element)
                if self._is_tab_selected(tab_element=tab_element):
                    return tab_object
                else:
                    self._logger.error(msg=f"Assertion Error: Can't switch to tab {tab_name}")
                    self._attach_screenshot()
                    raise AssertionError(f"Can't switch to tab {tab_name}")

    def _check_description(self, key: str):
        self._switch_tab(tab_name="ПЕРВИЧНЫЕ ДАННЫЕ")
        self._check_element_value(locator=EventTabPrimary.DESCRIPTION, value=key)
