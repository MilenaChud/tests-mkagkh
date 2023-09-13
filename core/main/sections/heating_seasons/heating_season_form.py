import time
from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper


class HeatingSeasonForm(AppSectionsHelper):
    BUTTON_ADD = (By.XPATH, "//span[contains(text(), 'Добавить')]/parent::button")
    TITLE_CARD = (By.XPATH, "//h1[contains(text(), 'Карточка учета начала и окончания отопительного сезона')]")
    MUNICIPALITY = (By.XPATH, "//label[contains(text(), 'Муниципальное образование')]/..//input")
    CHOOSE_MUNICIPALITY_TITLE = (By.XPATH, "//p[contains(text(), 'Выберите муниципальное образование')]")
    CHOOSE_MUNICIPALITY = (By.XPATH, "//p[contains(text(), 'Выберите муниципальное образование')]/"
                                     "..//label[contains(text(), 'Муниципальное образование')]/..//input")
    LOCALITY = (By.XPATH, "//p[contains(text(), 'Выберите муниципальное образование')]/"
                          "..//label[contains(text(), 'Населенный пункт')]/..//input")
    SAVE_MUNICIPALITY = (By.XPATH, "//div[@role='dialog']/..//span[contains(text(), 'Сохранить')]")
    PERIOD_HEATING_SEASON = (By.XPATH, "//label[contains(text(), 'Период отопительного сезона')]/..//input")
    START_DATE_PLAN = (By.XPATH, "//label[contains(text(), 'Планируемая дата начала отопительного сезона')]/..//input")
    START_DATE_REAL = (By.XPATH, "//label[contains(text(), 'Фактическая дата начала отопительного сезона')]/..//input")
    PDF_DOCUMENT_START = (By.XPATH, "//label[contains(text(), 'Распоряжение/постановление о начале отопительного "
                                    "сезона')]/..//input")
    ADD_INFO = (By.XPATH, "//label[contains(text(), 'Дополнительная текстовая информация')]/..//textarea[1]")
    REASONS_START = (By.XPATH, "//label[contains(text(), 'Причины отклонения фактической даты начала от"
                               " планируемой даты')]/..//input")
    FINAL_DATE_PLAN = (By.XPATH, "//label[contains(text(), 'Планируемая дата окончания отопительного сезона')]/.."
                                 "//input")
    FINAL_DATE_REAL = (By.XPATH, "//label[contains(text(), 'Фактическая дата окончания отопительного сезона')]/.."
                                 "//input")
    PDF_DOCUMENT_FINAL = (By.XPATH, "//label[contains(text(), 'Распоряжение/постановление об окончании отопительного "
                                    "сезона')]/..//input")
    REASONS_FINAL = (By.XPATH, "//label[contains(text(), 'Причины отклонения фактической даты окончания от"
                               " планируемой даты')]/..//input")
    BUTTON_EDIT = (By.XPATH, "//span[contains(text(), 'Редактировать')]/parent::button")
    BUTTON_NEXT = (By.XPATH, "//span[contains(text(), 'Далее')]/parent::button")
    BUTTON_SAVE = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Сохранить')]/parent::button")
    BUTTON_CANCEL = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Отмена')]/parent::button")
    BUTTON_BACK = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Назад')]/parent::button")
    MESSAGE_CREATE_SUCCESS = (By.XPATH, "//div[contains(text(), 'Отопительный сезон успешно добавлен')]")
    MESSAGE_UPDATE_SUCCESS = (By.XPATH, "//div[contains(text(), 'Отопительный сезон успешно обновлен')]")
    TAB_START = (By.XPATH, "//span[contains(text(), 'Начало отопительного сезона')]")
    TAB_FINAL = (By.XPATH, "//span[contains(text(), 'Окончание отопительного сезона')]")

    def _fill_start_heating_plans(self, template: dict, file_pdf: str, save: bool = True):
        self._click_element(locator=self.BUTTON_ADD)
        self._check_element_visible(locator=self.TITLE_CARD)
        self._click_element(locator=self.MUNICIPALITY)
        self._check_element_visible(locator=self.CHOOSE_MUNICIPALITY_TITLE)
        self._fill_input_by_symbols(locator=self.CHOOSE_MUNICIPALITY, value=template['Municipality']['Region'])
        time.sleep(1)
        self._press_keyboard_key(key="PAGE DOWN, ENTER")
        self._fill_input_by_symbols(locator=self.LOCALITY, value=template['Municipality']['Locality'])
        time.sleep(1)
        self._press_keyboard_key(key="PAGE DOWN, ENTER")
        self._click_element(locator=self.SAVE_MUNICIPALITY)
        elements = self._find_elements_visible(locator=self.PERIOD_HEATING_SEASON)
        for i in range(len(elements)):
            value = str(int(template['PeriodFrom']) + i)
            self._fill_input(locator=elements[i], value=value)
        self._set_calendar(input_locator=self.START_DATE_PLAN, target_date_time=template['StartPlanFullDate'])
        self._set_calendar(input_locator=self.START_DATE_REAL, target_date_time=template['StartRealFullDate'])
        pdf_document = self._find_element(locator=self.PDF_DOCUMENT_START)
        pdf_document.send_keys(file_pdf)
        self._fill_input(locator=self.ADD_INFO, value=template['StartAddInfo'])
        self._fill_input(locator=self.REASONS_START, value=template['StartReasons'])
        if save:
            self._click_element(locator=self.BUTTON_NEXT)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
            self._click_element(locator=self.BUTTON_BACK)

    def _fill_final_heating_plans(self, template: dict, file_pdf: str, save: bool = True):
        self._check_element_visible(locator=self.MUNICIPALITY, visibility=False, timeout=3)
        self._set_calendar(input_locator=self.FINAL_DATE_PLAN, target_date_time=template['FinalPlanFullDate'])
        pdf_document = self._find_element(locator=self.PDF_DOCUMENT_FINAL)
        pdf_document.send_keys(file_pdf)
        self._fill_input(locator=self.ADD_INFO, value=template['FinalAddInfo'])
        self._set_calendar(input_locator=self.FINAL_DATE_REAL, target_date_time=template['FinalRealFullDate'])
        self._fill_input(locator=self.REASONS_FINAL, value=template['FinalReasons'])
        if save:
            self._click_element(locator=self.BUTTON_SAVE)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
            self._click_element(locator=self.BUTTON_BACK)
        self._check_element_visible(locator=self.MESSAGE_CREATE_SUCCESS, visibility=save)

    def _check_tab_start(self, template: dict):
        self._check_element_value(locator=self.MUNICIPALITY, value=template['Municipality']['FullValue'])
        self._check_element_value(locator=self.PERIOD_HEATING_SEASON, value=template['PeriodFrom'])
        self._check_element_value(locator=self.START_DATE_PLAN, value=template['StartPlanFullDate'])
        self._check_element_value(locator=self.START_DATE_REAL, value=template['StartRealFullDate'])
        self._check_element_value(locator=self.ADD_INFO, value=template['StartAddInfo'])
        self._check_element_value(locator=self.REASONS_START, value=template['StartReasons'])

    def _check_tab_final(self, template: dict, edited: bool):
        self._click_element(locator=self.BUTTON_NEXT)
        if not edited:
            self._check_element_value(locator=self.FINAL_DATE_PLAN, value=template['FinalPlanFullDate'])
            self._check_element_value(locator=self.ADD_INFO, value=template['FinalAddInfo'])
            self._check_element_value(locator=self.FINAL_DATE_REAL, value=template['FinalRealFullDate'])
            self._check_element_value(locator=self.REASONS_FINAL, value=template['FinalReasons'])
        else:
            self._check_element_value(locator=self.FINAL_DATE_PLAN, value=template['FinalPlanFullDateEdit'])
            self._check_element_value(locator=self.ADD_INFO, value=template['FinalAddInfoEdit'])
            self._check_element_value(locator=self.FINAL_DATE_REAL, value=template['FinalRealFullDateEdit'])
            self._check_element_value(locator=self.REASONS_FINAL, value=template['FinalReasonsEdit'])

    def _edit_tab(self, template: dict, save: bool = True):
        self._click_element(locator=self.TAB_FINAL)
        self._click_element(locator=self.BUTTON_EDIT)
        self._set_calendar(input_locator=self.FINAL_DATE_PLAN, target_date_time=template['FinalPlanFullDateEdit'])
        self._fill_input(locator=self.ADD_INFO, value=template['FinalAddInfoEdit'])
        self._set_calendar(input_locator=self.FINAL_DATE_REAL, target_date_time=template['FinalRealFullDateEdit'])
        self._fill_input(locator=self.REASONS_FINAL, value=template['FinalReasonsEdit'])
        if save:
            self._click_element(locator=self.BUTTON_SAVE)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
            self._click_element(locator=self.BUTTON_BACK)
        self._check_element_visible(locator=self.MESSAGE_UPDATE_SUCCESS, visibility=save)
