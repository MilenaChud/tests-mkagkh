from selenium.webdriver.common.by import By
from core.main.sections.events.event_tabs_common import EventTabsCommon


class EventTabPrimary(EventTabsCommon):
    # Locators
    AREAS_LIST = (By.XPATH, "//label[contains(text(), 'Сфера ЖКХ')]/..//select")
    DATE_TIME_LOCAL = (By.XPATH, "//label[contains(text(), 'Дата и время возникновения события (местное)')]/..//input")
    DATE_TIME_MSK = (By.XPATH, "//label[contains(text(), 'Дата и время возникновения события (МСК)')]/..//input")
    ADDRESS_INPUT = (By.XPATH, "//label[contains(text(), 'Адрес события')]/..//input")
    SOURCES_LIST = (By.XPATH, "//label[contains(text(), 'Источник первичной информации')]/..//select")
    DESCRIPTION = (By.XPATH, "//label[contains(text(), 'Краткое описание события')]/..//input")

    Sources = {
        "PHONE": "По телефону",
        "SOCIAL_NETWORK": "Социальные сети",
        "NEWS_OR_INTERNET": "Новостные порталы и источники информации в сети",
        "OTHER": "Другие средства связи",
        "BID": "Обращение гражданина",
        "DISPATCH_SERVICE": "Диспетчерская служба городского округа или муниципального района"
    }

    def _check_data(self, template: dict):
        _area = self._get_element_attribute(locator=self.AREAS_LIST, attr_name="value")
        assert self.Areas[_area] == template['Area']
        assert self._get_element_attribute(locator=self.ADDRESS_INPUT, attr_name="value") == template['Address']['Full']
        _source = self._get_element_attribute(locator=self.SOURCES_LIST, attr_name="value")
        assert self.Sources[_source] == template['Source']
        assert self._get_element_attribute(locator=self.DESCRIPTION, attr_name="value") == template['Description']
