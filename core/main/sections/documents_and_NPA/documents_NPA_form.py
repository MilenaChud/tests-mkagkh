import time
from selenium.webdriver.common.by import By
from core.helpers.app_sections_helper import AppSectionsHelper


class DocumentsNPAForm(AppSectionsHelper):
    BUTTON_ADD = (By.XPATH, "//span[contains(text(), 'Добавить')]/parent::button")
    TITLE_CARD = (By.XPATH, "//h1[contains(text(), 'Карточка справочного документа и НПА')]")
    NAME_DOCUMENT = (By.XPATH, "//label[contains(text(), 'Наименование документа')]/..//input")
    DOCUMENT_NUMBER = (By.XPATH, "//label[contains(text(), 'Номер документа')]/..//input")
    TYPE_DOCUMENT = (By.XPATH, "//label[contains(text(), 'Тип документа')]/..//select")
    KIND_DOCUMENT = (By.XPATH, "//label[contains(text(), 'Вид документа')]/..//select")
    DATE_PUBLISH = (By.XPATH, "//label[contains(text(), 'Дата публикации')]/..//input")
    DESCRIBE_DOCUMENT = (By.XPATH, "//label[contains(text(), 'Описание документа')]/..//input")
    RECEIVING_AUTHORITY_BUTTON = (
        By.XPATH, "//label[contains(text(), 'Принявший орган')]/..//span[@class='MuiTouchRipple-root']")
    BUTTON_SAVE = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Сохранить')]/parent::button")
    BUTTON_CANCEL = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Отмена')]/parent::button")
    LOAD_DOCUMENT = (By.XPATH, "//div[contains(text(), 'Для загрузки файла перетащите его в эту область')]/..//input")
    BUTTON_EDIT = (By.XPATH, "//span[contains(text(), 'Редактировать')]/parent::button")
    BUTTON_BACK = (By.XPATH, "//div[@class='buttons-container']//span[contains(text(), 'Назад')]/parent::button")

    TYPE_DOCUMENTS = {"NPA": "НПА",
                      "REFERENCE": "Справочный документ"}

    KIND_DOCUMENTS = {"1": "Административный регламент",
                      "2": "Ветеринарно-санитарные правила",
                      "3": "Ветеринарные правила",
                      "4": "Гигиенические нормативы",
                      "5": "Директива",
                      "6": "Договор",
                      "7": "Доктрина",
                      "8": "Должностная инструкция",
                      "9": "Дорожные нормы",
                      "10": "Инструкция"
                      }

    def _fill_start_documents_card(self, template: dict, file: str, save: bool = True):
        self._click_element(locator=self.BUTTON_ADD)
        self._check_element_visible(locator=self.TITLE_CARD)
        self._fill_input(locator=self.NAME_DOCUMENT, value=template['NameDocument'])
        self._fill_input(locator=self.DOCUMENT_NUMBER, value=template['NumberDocument'])
        self._set_calendar(input_locator=self.DATE_PUBLISH, target_date_time=template['DatePublish'])
        self._fill_input(locator=self.DESCRIBE_DOCUMENT, value=template['DescribeDocument'])
        elements = self._click_element(locator=self.KIND_DOCUMENT)
        self._select_option_by_text(selector=elements, text=template['KindDocument'])
        elements = self._click_element(locator=self.TYPE_DOCUMENT)
        self._select_option_by_text(selector=elements, text=template['TypeDocument'])
        #self._click_element(locator=self.RECEIVING_AUTHORITY_BUTTON)
        RUBRICATOR = (By.XPATH, f"//span[contains(text(), '{template['Area']}')]")
        self._click_element(locator=RUBRICATOR)  # Уточнить
        file_load = self._find_element(locator=self.LOAD_DOCUMENT)
        file_load.send_keys(file)
        time.sleep(5)
        self._press_keyboard_key(key="PAGE DOWN")
        self._press_keyboard_key(key="PAGE DOWN")
        self._click_element(locator=self.BUTTON_SAVE)
        time.sleep(3)

    def _check_tab_start(self, template: dict):
        self._check_element_value(locator=self.NAME_DOCUMENT, value=template['NameDocument'])
        self._check_element_value(locator=self.DOCUMENT_NUMBER, value=template['NumberDocument'])
        self._check_element_value(locator=self.DATE_PUBLISH, value=template['StartPlanFullDate'])
        self._check_element_value(locator=self.DESCRIBE_DOCUMENT, value=template['StartRealFullDate'])
        kind_document = self._get_element_attribute(locator=self.KIND_DOCUMENT, attr_name="value")
        assert self.KIND_DOCUMENTS[kind_document] == template['KindDocument']
        type_document = self._get_element_attribute(locator=self.TYPE_DOCUMENT, attr_name="value")
        assert self.TYPE_DOCUMENTS[type_document] == template['TypeDocument']

    def _edit_tab(self, template: dict, save: bool = True):
        self._click_element(locator=self.BUTTON_EDIT)
        self._fill_input(locator=self.NAME_DOCUMENT, value=template['NameDocument'])
        self._fill_input(locator=self.DOCUMENT_NUMBER, value=template['NumberDocument'])
        self._set_calendar(input_locator=self.DATE_PUBLISH, target_date_time=template['DatePublish'])
        self._fill_input(locator=self.DESCRIBE_DOCUMENT, value=template['DescribeDocument'])
        elements = self._click_element(locator=self.KIND_DOCUMENT)
        self._select_option_by_text(selector=elements, text=template['KindDocument'])
        elements = self._click_element(locator=self.TYPE_DOCUMENT)
        self._select_option_by_text(selector=elements, text=template['TypeDocument'])
        if save:
            self._click_element(locator=self.BUTTON_SAVE)
        else:
            self._click_element(locator=self.BUTTON_CANCEL)
            self._click_element(locator=self.BUTTON_BACK)
        #self._check_element_visible(locator=self.MESSAGE_UPDATE_SUCCESS, visibility=save)
