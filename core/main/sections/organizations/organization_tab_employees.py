import time
from selenium.webdriver.common.by import By
from core.main.sections.organizations.organization_tabs_common import OrganizationTabsCommon


class OrganizationTabEmployees(OrganizationTabsCommon):
    # Locators
    EMPLOYEES_TABLE_EMPTY = (By.XPATH, "//div[contains(text(), 'Список сотрудников')]/../../.."
                                       "//tbody//td[contains(text(), 'Данных не найдено')]")
    EMPLOYEES_TABLE_LIST = (By.XPATH, "//div[contains(text(), 'Список сотрудников')]/../../..//tbody/tr")
    BUTTON_ADD_EMPLOYEE = (By.XPATH, "//span[contains(text(), 'Добавить сотрудника')]/parent::button")
    EMPLOYEE_TITLE_ADD = (By.XPATH, "//h2[contains(text(), 'Добавление сотрудника')]")
    EMPLOYEE_POSITION = (By.XPATH, "//label[contains(text(), 'Должность')]/..//input")
    EMPLOYEE_LAST_NAME = (By.XPATH, "//label[contains(text(), 'Фамилия')]/..//input")
    EMPLOYEE_FIRST_NAME = (By.XPATH, "//label[contains(text(), 'Имя')]/..//input")
    EMPLOYEE_MIDDLE_NAME = (By.XPATH, "//label[contains(text(), 'Отчество')]/..//input")
    EMPLOYEE_WORK_PHONE = (By.XPATH, "//label[contains(text(), 'Рабочий телефон')]/..//input")
    EMPLOYEE_MOBILE_PHONE = (By.XPATH, "//label[contains(text(), 'Мобильный телефон')]/..//input")
    EMPLOYEE_BUTTON_CANCEL = (By.XPATH, "//h2[contains(text(), 'Добавление сотрудника')]/../.."
                                        "//span[contains(text(), 'Отмена')]/parent::button")
    EMPLOYEE_BUTTON_SAVE = (By.XPATH, "//h2[contains(text(), 'Добавление сотрудника')]/../.."
                                      "//span[contains(text(), 'Сохранить')]/parent::button")

    def _find_employee(self, employee: dict):
        if self._is_element_visible(locator=self.EMPLOYEES_TABLE_EMPTY, visibility=False, timeout=3):
            expected = (employee['Position'], employee['FullName'], employee['Phone'], employee['MobilePhone'],
                        employee['UserExists'])
            elements = self._find_elements_visible(locator=self.EMPLOYEES_TABLE_LIST)
            rows = len(elements)
            found = False
            row = 0
            while (not found) and (row < rows):
                row += 1
                col = 1
                flag = True
                while flag and (col <= len(expected)):
                    if col < 5:
                        td_locator = (By.XPATH, f"//div[contains(text(), 'Список сотрудников')]/../../.."
                                                f"//tbody//tr[{row}]/td{[col]}")
                        td_text = self._check_element_visible(locator=td_locator).text.strip()
                        flag = (td_text == expected[col - 1])
                    else:
                        td_locator = (By.XPATH, f"//div[contains(text(), 'Список сотрудников')]/../../.."
                                                f"//tbody//tr[{row}]/td{[col]}/div")
                        flag = (self._is_element_visible(locator=td_locator, visibility=True, timeout=3) is expected[4])
                    col += 1
                found = flag
            if not found:
                row = -1
        else:
            row = -1
        return row

    def _add_employees(self, employees: list, employees_save: bool, save: bool):
        self._click_element(locator=self.BUTTON_EDIT)
        for employee in employees:
            self._click_element(locator=self.BUTTON_ADD_EMPLOYEE)
            self._check_element_visible(locator=self.EMPLOYEE_TITLE_ADD)
            # time.sleep(0.5)
            self._fill_input(locator=self.EMPLOYEE_POSITION, value=employee['Position'])
            self._fill_input(locator=self.EMPLOYEE_LAST_NAME, value=employee['LastName'])
            self._fill_input(locator=self.EMPLOYEE_FIRST_NAME, value=employee['FirstName'])
            self._fill_input(locator=self.EMPLOYEE_MIDDLE_NAME, value=employee['MiddleName'])
            self._fill_input(locator=self.EMPLOYEE_WORK_PHONE, value=employee['Phone'])
            self._fill_input(locator=self.EMPLOYEE_MOBILE_PHONE, value=employee['MobilePhone'])
            employee['FullName'] = f"{employee['LastName']} {employee['FirstName']} {employee['MiddleName']}"
            employee['UserExists'] = False
            if employees_save:
                self._click_element(locator=self.EMPLOYEE_BUTTON_SAVE)
            else:
                self._click_element(locator=self.EMPLOYEE_BUTTON_CANCEL)
            self._check_element_visible(locator=self.EMPLOYEE_TITLE_ADD, visibility=False, timeout=3)

        if save:
            self._click_element(locator=self.BUTTON_SAVE)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
