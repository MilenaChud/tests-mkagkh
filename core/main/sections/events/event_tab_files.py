import time
from selenium.webdriver.common.by import By
from core.main.sections.events.event_tabs_common import EventTabsCommon


class EventTabFiles(EventTabsCommon):
    # Locators
    FILE_DROPZONE_DISABLED = (By.XPATH, "//div[@class='attachment']//div[@class='dzu-dropzone disabled']")
    FILE_DROPZONE_ENABLED = (By.XPATH, "//div[@class='attachment']//div[@class='dzu-dropzone']")
    FILE_INPUT = (By.XPATH, "//label[@class='dzu-inputLabel']//input")
    FILES_TABLE_EMPTY = (By.XPATH, "//table//tbody//td[contains(text(), 'Данных не найдено')]")
    FILES_TABLE_LIST = (By.XPATH, "//table//tbody/tr")

    MESSAGE_DELETE_SUCCESS = (By.XPATH, "//div[contains(text(), 'Файл удален успешно')]")

    def _find_file_index(self, filename: str):
        if self._is_element_visible(locator=self.FILES_TABLE_EMPTY, visibility=False, timeout=3):
            file_basename = self._get_file_basename(filename=filename)
            rows = self._find_elements_visible(locator=self.FILES_TABLE_LIST)
            found = False
            index = 0
            while (not found) and (index < len(rows)):
                file_locator = (By.XPATH, f"//table//tbody//tr[{index + 1}]/td[2]//a")
                file_element = self._check_element_visible(locator=file_locator)
                found = (file_element.text == file_basename)
                index += 1
            if not found:
                index = -1
        else:
            index = -1
        return index

    def _check_elements_editable(self, edit: bool):
        if edit:
            self._check_element_visible(locator=self.FILE_DROPZONE_ENABLED, visibility=True)
        else:
            self._check_element_visible(locator=self.FILE_DROPZONE_DISABLED, visibility=True)

    def _get_files_list(self):
        files_list = []
        rows = self._find_elements_visible(locator=self.FILES_TABLE_LIST)
        td_locator = (By.XPATH, f"//table//tbody//tr[1]/td")
        cells = self._find_elements_visible(locator=td_locator)
        if len(cells) == 1:
            file = {"NoData": cells[0].text}
            files_list.append(file)
        else:
            for index in range(len(rows)):
                image_locator = (By.XPATH, f"//table//tbody//tr[{index + 1}]/td[1]/img")
                file_image_flag = self._is_element_visible(locator=image_locator, visibility=True, timeout=3)
                file_locator = (By.XPATH, f"//table//tbody//tr[{index + 1}]/td[2]//a")
                file_name = self._check_element_visible(locator=file_locator).text
                file_info = {
                    "Image": file_image_flag,
                    "Name": file_name
                }
                files_list.append(file_info)
        return files_list

    def _check_files_list(self, template_list: list):
        def sort_by_name(unsorted: list):
            result = unsorted
            if len(unsorted) > 1:
                result = sorted(unsorted, key=lambda item: item['Name'])
            return result

        files_list = self._get_files_list()
        assert sort_by_name(files_list) == sort_by_name(template_list)

    def _upload_file(self, filename: str, save: bool):
        self._check_buttons(edit=False)
        self._check_elements_editable(edit=False)

        self._press_keyboard_key(key="PAGE UP")

        self._click_element(locator=self.BUTTON_EDIT)
        self._check_buttons(edit=True)
        self._check_elements_editable(edit=True)
        file_input = self._find_element(locator=self.FILE_INPUT)
        file_input.send_keys(filename)
        self._press_keyboard_key(key="PAGE DOWN")
        if save:
            element = self._check_element_visible(locator=self.BUTTON_SAVE)
        else:
            element = self._check_element_visible(locator=self.BUTTON_CANCEL)

        self._press_keyboard_key(key="PAGE DOWN")
        self._click_webelement(element=element)

        self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=save)
        self._check_buttons(edit=False)
        self._check_elements_editable(edit=False)
        time.sleep(1)

    def _download_file(self, filename: str):
        index = self._find_file_index(filename=filename)
        if index > 0:
            file_locator = (By.XPATH, f"//table//tbody//tr[{index}]/td[2]//a")
            self._click_element(locator=file_locator)

    def _delete_file(self, filename: str, save: bool):
        index = self._find_file_index(filename=filename)
        if index > 0:
            self._check_buttons(edit=False)
            self._check_elements_editable(edit=False)
            self._click_element(locator=self.BUTTON_EDIT)
            self._check_buttons(edit=True)
            self._check_elements_editable(edit=True)
            button_delete_locator = (By.XPATH, f"//table//tbody//tr[{index}]/td[3]//button")
            self._click_element(locator=button_delete_locator)
            if save:
                self._click_element(locator=self.BUTTON_SAVE)
            else:
                self._click_element(locator=self.BUTTON_CANCEL)
            self._check_element_visible(locator=self.MESSAGE_DELETE_SUCCESS, visibility=save)
            self._check_element_visible(locator=self.MESSAGE_SAVE_SUCCESS, visibility=save)
            self._check_buttons(edit=False)
            self._check_elements_editable(edit=False)

    def _add_to_files_list(self, current_list: list, filename: str):
        result = list(current_list)
        if (len(result) > 0) and ("NoData" in result[0].keys()):
            del result[0]
        file_info = self._get_file_info(filename=filename)
        result.append(file_info)  # TODO: Добавить проверку, что файла нет в списке (когда это реализуют в интерфейсе)
        return result

    def _delete_from_files_list(self, current_list: list, filename: str):
        result = list(current_list)
        file_basename = self._get_file_basename(filename=filename)
        if (len(result) > 0) and ("NoData" not in result[0].keys()):
            found = False
            index = 0
            while (not found) and (index < len(result)):
                found = (result[index]["Name"] == file_basename)
                index += 1
            if found:
                del result[index - 1]
                if len(result) == 0:
                    result.append({"NoData": "Данных не найдено"})
        return result
