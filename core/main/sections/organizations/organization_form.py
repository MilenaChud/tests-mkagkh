import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from core.helpers.app_sections_helper import AppSectionsHelper
from core.main.sections.organizations.organization_tab_information import OrganizationTabInformation
from core.main.sections.organizations.organization_tab_employees import OrganizationTabEmployees
from core.main.sections.organizations.organization_tab_resources import OrganizationTabResources


class OrganizationForm(AppSectionsHelper):
    # Locators
    TITLE = (By.XPATH, "//h1[contains(text(), 'Карточка организации')]")
    TAB_INFORMATION =(By.XPATH, "//div[@class='stepper']//span[contains(text(), 'Сведения об организации')]"
                                "/ancestor::div[@role='button']")
    TAB_EMPLOYEES = (By.XPATH, "//div[@class='stepper']//span[contains(text(), 'Список сотрудников организации')]"
                               "/ancestor::div[@role='button']")
    TAB_RESOURCES = (By.XPATH, "//div[@class='stepper']//span[contains(text(), 'Силы и средства')]"
                               "/ancestor::div[@role='button']")
    NAME = (By.XPATH, "//label[contains(text(), 'Наименование организации')]/..//input")

    def __init__(self, driver):
        super().__init__(driver=driver)
        self._tab_information = OrganizationTabInformation(driver=driver)
        self._tab_employees = OrganizationTabEmployees(driver=driver)
        self._tab_resources = OrganizationTabResources(driver=driver)

    def _is_tab_selected(self, tab_element: WebElement):
        result = (self._get_webelement_attribute(element=tab_element, attr_name="class") == "step active")
        return result

    def _switch_tab(self, tab_name: str):
        self._check_element_visible(locator=self.TITLE)

        tab_element = None
        tab_object = None
        match tab_name:
            case "Сведения об организации":
                tab_element = self._check_element_clickable(locator=self.TAB_INFORMATION)
                tab_object = self._tab_information

            case "Список сотрудников":
                tab_element = self._check_element_clickable(locator=self.TAB_EMPLOYEES)
                tab_object = self._tab_employees

            case "Силы и средства":
                tab_element = self._check_element_clickable(locator=self.TAB_RESOURCES)
                tab_object = self._tab_resources

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

    def _check_name(self, key: str):
        self._switch_tab(tab_name="Сведения об организации")
        self._check_element_value(locator=self.NAME, value=key)
