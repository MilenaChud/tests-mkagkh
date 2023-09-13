import allure
import hashlib
import keyboard
import logging
import os
import time
from datetime import datetime
from json import load
from typing import List
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedTagNameException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.relative_locator import locate_with


class BaseHelper:
    def __init__(self, driver):
        self._driver = driver
        self._actions = ActionChains(driver=driver)
        self._config_logger()

    def _config_logger(self):
        self._logger = logging.getLogger(name=type(self).__name__)
        self._handler = logging.FileHandler(filename=self._driver.log_name, encoding="utf-8")
        self._handler.setFormatter(fmt=logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s"))
        self._logger.handlers.clear()
        self._logger.addHandler(hdlr=self._handler)
        self._logger.setLevel(level=self._driver.log_level)

    @allure.step("Get key from current date and time")
    def _get_date_time_key(self):
        self._logger.info(msg=f"Get key from current date and time")
        return str(datetime.now().strftime("%Y%m%d_%H%M%S"))  # TODO: Get datetime with region timezone

    def _get_file_basename(self, filename: str):
        file_basename = os.path.basename(p=filename)
        return file_basename

    def _get_file_size(self, filename: str):
        file_size = os.path.getsize(filename=filename)
        return file_size

    def _get_file_hash(self, filename: str):
        size = 65536
        with open(file=filename, mode="rb") as file:
            hasher = hashlib.sha1()
            buffer = file.read(size)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = file.read(size)
        file_hash = hasher.hexdigest()
        return file_hash

    @allure.step("Read data from file {filename}")
    def _read_data_from_file(self, filename: str):
        self._logger.info(msg=f"Read data from file \'{filename}\'")
        with open(file=filename, mode="r", encoding="utf-8") as json_file:
            data = load(fp=json_file)
        return data

    def _attach_screenshot(self):
        date_time = self._get_date_time_key()
        screenshot_name = f"{date_time}_{self._driver.session_id}.png"
        with allure.step(f"Attach screenshot file \'{screenshot_name}\' to allure report"):
            self._logger.info(msg=f"Attach screenshot file \'{screenshot_name}\' to allure report")
            allure.attach(
                attachment_type=allure.attachment_type.PNG,
                name=screenshot_name,
                body=self._driver.get_screenshot_as_png()
            )

    def _open(self, added_path: str = ""):
        url = self._driver.base_url + added_path
        with allure.step(f"Open URL {url}"):
            self._logger.info(msg=f"Open URL {url}")
            self._driver.get(url=url)

    @allure.step("Check if element with locator {locator} is clickable")
    def _check_element_clickable(self, locator: tuple, timeout: int = -1, raise_error: bool = True):
        self._logger.info(msg=f"Check if element with locator {locator} is clickable")
        try:
            if timeout < 0:
                timeout = self._driver.timeout
            return WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=ec.element_to_be_clickable(mark=locator))
        except TimeoutException:
            if raise_error:
                self._logger.error(msg=f"Assertion Error: Can't find clickable element with locator {locator}")
                self._attach_screenshot()
                raise AssertionError(f"Can't find clickable element with locator {locator}")
            else:
                self._logger.info(msg=f"Timeout {timeout}s has expired while checking if element with locator {locator}"
                                      f" is clickable")
                raise NoSuchElementException

    @allure.step("Return boolean result depending on actual clickablility of element with locator {locator}")
    def _is_element_clickable(self, locator: tuple, timeout: int = -1):
        self._logger.info(msg=f"Return boolean result depending on actual clickability of element with"
                              f" locator {locator}")
        result = None
        try:
            self._check_element_clickable(locator=locator, timeout=timeout, raise_error=False)
        except NoSuchElementException:
            result = False
        else:
            result = True
        finally:
            with allure.step(f"Returned result is {result}"):
                self._logger.info(msg=f"Returned result is {result}")
                return result

    @allure.step("Check if given WebElement is clickable")
    def _check_webelement_clickable(self, element: WebElement, timeout: int = -1):
        self._logger.info(msg=f"Check if given WebElement is clickable")
        try:
            if timeout < 0:
                timeout = self._driver.timeout
            return WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=ec.element_to_be_clickable(mark=element))
        except TimeoutException:
            self._logger.error(msg=f"Assertion Error: Given WebElement is either invalid or not clickable")
            self._attach_screenshot()
            raise AssertionError(f"Given WebElement is either invalid or not clickable")

    @allure.step("Check if element with locator {locator} has required visibility")
    def _check_element_visible(self, locator: tuple, visibility: bool = True, timeout: int = -1,
                               raise_error: bool = True):
        self._logger.info(msg=f"Check if element with locator {locator} has required visibility")
        try:
            if timeout < 0:
                timeout = self._driver.timeout
            if visibility:
                method = ec.visibility_of_element_located
            else:
                method = ec.invisibility_of_element_located
            return WebDriverWait(driver=self._driver, timeout=timeout).until(method=method(locator=locator))
        except TimeoutException:
            state = "visible" if visibility else "absent or invisible"
            if raise_error:
                self._logger.error(msg=f"Assertion Error: Can't find {state} element with locator {locator}")
                self._attach_screenshot()
                raise AssertionError(f"Can't find {state} element with locator {locator}")
            else:
                self._logger.info(msg=f"Timeout {timeout}s has expired while checking if element with locator {locator}"
                                      f" is {state}")
                raise NoSuchElementException

    @allure.step("Return boolean result depending on given visibility of element with locator {locator}")
    def _is_element_visible(self, locator: tuple, visibility: bool = True, timeout: int = -1):
        self._logger.info(msg=f"Return boolean result depending on given visibility of element with locator {locator}")
        result = None
        try:
            self._check_element_visible(locator=locator, visibility=visibility, timeout=timeout, raise_error=False)
        except NoSuchElementException:
            result = False
        else:
            result = True
        finally:
            with allure.step(f"Returned result is {result}"):
                self._logger.info(msg=f"Returned result is {result}")
                return result

    @allure.step("Check if given WebElement has required visibility")
    def _check_webelement_visible(self, element: WebElement, visibility: bool = True, timeout: int = -1):
        self._logger.info(msg=f"Check if given WebElement has required visibility")
        try:
            if timeout < 0:
                timeout = self._driver.timeout
            if visibility:
                method = ec.visibility_of
            else:
                method = ec.invisibility_of_element
            return WebDriverWait(driver=self._driver, timeout=timeout).until(method=method(element=element))
        except TimeoutException:
            self._logger.error(msg=f"Assertion Error: Given WebElement is invalid or has wrong visibility")
            self._attach_screenshot()
            raise AssertionError(f"Given WebElement is invalid or has wrong visibility")

    @allure.step("Check if text {text} is present in element with locator {locator}")
    def _check_element_text(self, locator: tuple, text: str, timeout: int = -1):
        self._logger.info(msg=f"Check if text \'{text}\' is present in element with locator {locator}")
        try:
            if timeout < 0:
                timeout = self._driver.timeout
            return WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=ec.text_to_be_present_in_element(locator=locator, text_=text))
        except TimeoutException:
            self._logger.error(msg=f"Assertion Error: Can't find text \'{text}\' in element with locator {locator}")
            self._attach_screenshot()
            raise AssertionError(f"Can't find text \'{text}\' in element with locator {locator}")

    @allure.step("Check if value {value} is present in element with locator {locator}")
    def _check_element_value(self, locator: tuple, value: str, timeout: int = -1):
        self._logger.info(msg=f"Check if value \'{value}\' is present in element with locator {locator}")
        try:
            if timeout < 0:
                timeout = self._driver.timeout
            return WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=ec.text_to_be_present_in_element_value(locator=locator, text_=value))
        except TimeoutException:
            self._logger.error(msg=f"Assertion Error: Can't find value \'{value}\' in element with locator {locator}")
            self._attach_screenshot()
            raise AssertionError(f"Can't find value \'{value}\' in element with locator {locator}")

    @allure.step("Check if text {text} is present in given WebElement")
    def _check_webelement_text(self, element: WebElement, text: str):
        self._logger.info(msg=f"Check if text \'{text}\' is present in given WebElement")
        try:
            assert text in element.text
        except Exception:
            self._logger.error(msg=f"Assertion Error: Can't find text \'{text}\' in given WebElement")
            self._attach_screenshot()
            raise AssertionError(f"Can't find text \'{text}\' in given WebElement")

    @allure.step("Check if value {value} is present in given WebElement")
    def _check_webelement_value(self, element: WebElement, value: str):
        self._logger.info(msg=f"Check if value \'{value}\' is present in given WebElement")
        try:
            assert value in element.get_attribute(name="value")
        except Exception:
            self._logger.error(msg=f"Assertion Error: Can't find value \'{value}\' in given WebElement")
            self._attach_screenshot()
            raise AssertionError(f"Can't find value \'{value}\' in given WebElement")

    @allure.step("Check if one of text options {texts} is present in given WebElement")
    def _check_webelement_text_options(self, element: WebElement, texts: tuple):
        self._logger.info(msg=f"Check if one of text options {texts} is present in given WebElement")
        result = list(filter(lambda item: item in element.text, texts))
        try:
            assert len(result) > 0
        except Exception:
            self._logger.error(msg=f"Assertion Error: Can't find none of text options {texts} in given WebElement")
            self._attach_screenshot()
            raise AssertionError(f"Can't find none of text options {texts} in given WebElement")

    @allure.step("Click element with locator {locator}")
    def _click_element(self, locator: tuple, timeout: int = -1):
        if timeout < 0:
            timeout = self._driver.timeout
        element = self._check_element_clickable(locator=locator, timeout=timeout)
        self._actions.move_to_element(to_element=element).click(on_element=element).perform()
        self._logger.info(msg=f"Click element with locator {locator}")
        return element

    @allure.step("Click given WebElement")
    def _click_webelement(self, element: WebElement, timeout: int = -1):
        if timeout < 0:
            timeout = self._driver.timeout
        self._check_webelement_clickable(element=element, timeout=timeout)
        self._actions.move_to_element(to_element=element).click(on_element=element).perform()
        self._logger.info(msg=f"Click given WebElement")

    @allure.step("Select option by text {text} for given selector")
    def _select_option_by_text(self, selector: WebElement, text: str):
        self._logger.info(msg=f"Select option by text \'{text}\' for given selector")
        try:
            Select(selector).select_by_visible_text(text=text)
        except (NoSuchElementException, UnexpectedTagNameException):
            self._logger.error(msg=f"Assertion Error: Can't select option by text \'{text}\' for given selector")
            self._attach_screenshot()
            raise AssertionError(f"Can't select option by text \'{text}\' for given selector")

    @allure.step("Get selected option text and value for select with locator {select_locator}")
    def _get_selected_option(self, select_locator: tuple):
        self._logger.info(msg=f"Get selected option text and value for select with locator {select_locator}")
        try:
            selector = self._find_element(locator=select_locator)
            element = Select(selector).first_selected_option
            text = element.text
            value = self._get_webelement_attribute(element=element, attr_name="value")
            result = {
                "Text": text,
                "Value": value
            }
            return result
        except UnexpectedTagNameException:
            self._logger.error(msg=f"Assertion Error: Can't get selected option for element with"
                                   f" locator {select_locator}")
            self._attach_screenshot()
            raise AssertionError(f"Can't get selected option for element with locator {select_locator}")

    @allure.step("Find visible elements with locator {locator}")
    def _find_elements_visible(self, locator: tuple, timeout: int = -1):
        self._logger.info(msg=f"Find visible elements with locator {locator}")
        try:
            if timeout < 0:
                timeout = self._driver.timeout
            return WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=ec.visibility_of_all_elements_located(locator=locator))
        except TimeoutException:
            self._logger.error(msg=f"Assertion Error: Can't find elements with locator {locator} or some of them"
                                   f" are not visible")
            self._attach_screenshot()
            raise AssertionError(f"Can't find elements with locator {locator} or some of them are not visible")

    @allure.step("Find element with locator {locator}")
    def _find_element(self, locator: tuple):
        self._logger.info(msg=f"Find element with locator {locator}")
        try:
            return self._driver.find_element(*locator)
        except NoSuchElementException:
            self._logger.error(msg=f"Assertion Error: Can't find element with locator {locator}")
            self._attach_screenshot()
            raise AssertionError(f"Can't find element with locator {locator}")

    @allure.step("Find element by relative tag {tag} around given base WebElement")
    def _find_element_by_relative_tag(self, base: WebElement, tag: str, location: str):
        self._logger.info(msg=f"Find element by relative tag {tag} around base {base}")
        try:
            match location:
                case "above":
                    relative_by = locate_with(by=By.TAG_NAME, using=tag).above(element_or_locator=base)
                case "below":
                    relative_by = locate_with(by=By.TAG_NAME, using=tag).below(element_or_locator=base)
                case "near":
                    relative_by = locate_with(by=By.TAG_NAME, using=tag).near(element_or_locator_distance=base)
                case "left":
                    relative_by = locate_with(by=By.TAG_NAME, using=tag).to_left_of(element_or_locator=base)
                case "right":
                    relative_by = locate_with(by=By.TAG_NAME, using=tag).to_right_of(element_or_locator=base)
                case _:
                    raise ValueError
        except ValueError:
            self._logger.error(msg=f"Assertion Error: Unknown value \'{location}\' for parameter location")
            raise AssertionError(f"Unknown value \'{location}\' for parameter location")
        except NoSuchElementException:
            self._logger.error(msg=f"Assertion Error: Can't find element by relative tag \'{tag}\' around "
                                   f"given WebElement")
            self._attach_screenshot()
            raise AssertionError(f"Can't find element by relative tag \'{tag}\' around given WebElement")
        else:
            return self._driver.find_element(relative_by)

    @allure.step("Find element with locator {locator} from given base WebElement")
    def _find_element_from_base(self, base: WebElement, locator: tuple):
        self._logger.info(msg=f"Find element with locator {locator} from base {base}")
        try:
            return base.find_element(*locator)
        except NoSuchElementException:
            self._logger.error(msg=f"Assertion Error: Can't find element with locator {locator} from given"
                                   f" base WebElement")
            self._attach_screenshot()
            raise AssertionError(f"Can't find element with locator {locator} from given base WebElement")

    @allure.step("Get attribute {attr_name} from element with locator {locator}")
    def _get_element_attribute(self, locator: tuple, attr_name: str):
        self._logger.info(msg=f"Get attribute \'{attr_name}\' from element with locator {locator}")
        attribute = self._find_element(locator=locator).get_attribute(name=attr_name)
        if attribute is not None:
            return attribute
        else:
            self._logger.error(msg=f"Assertion Error: Can't find attribute \'{attr_name}\' in element with"
                                   f" locator {locator}")
            self._attach_screenshot()
            raise AssertionError(f"Can't find attribute \'{attr_name}\' in element with locator {locator}")

    @allure.step("Get attribute {attr_name} from given WebElement")
    def _get_webelement_attribute(self, element: WebElement, attr_name: str):
        self._logger.info(msg=f"Get attribute \'{attr_name}\' from given WebElement")
        attribute = element.get_attribute(name=attr_name)
        if attribute is not None:
            return attribute
        else:
            self._logger.error(msg=f"Assertion Error: Can't find attribute \'{attr_name}\' in given WebElement")
            self._attach_screenshot()
            raise AssertionError(f"Can't find attribute \'{attr_name}\' in given WebElement")

    @allure.step("Get element with text {text} from given list of WebElements")
    def _get_element_by_text(self, elements: List[WebElement], text: str, strict_mode: bool = False):
        self._logger.info(msg=f"Get element with text \'{text}\' from given list of WebElements")
        if strict_mode:
            result = list(filter(lambda item: text == item.text, elements))
        else:
            result = list(filter(lambda item: text in item.text, elements))
        if len(result) > 0:
            return result[0]
        else:
            self._logger.error(msg=f"Assertion Error: Can't find element with text \'{text}\' in given list"
                                   f" of WebElements")
            self._attach_screenshot()
            raise AssertionError(f"Can't find element with text \'{text}\' in given list of WebElements")

    @allure.step("Check no elements with text {text} present in given list of WebElements")
    def _check_no_elements_by_text(self, elements: List[WebElement], text: str):
        self._logger.info(msg=f"Check no elements with text \'{text}\' present in given list of WebElements")
        result = list(filter(lambda item: text in item.text, elements))
        try:
            assert len(result) == 0
        except Exception:
            self._logger.error(msg=f"Assertion Error: Found elements with text \'{text}\' in given list of WebElements")
            self._attach_screenshot()
            raise AssertionError(f"Found elements with text \'{text}\' in given list of WebElements")

    @allure.step("Return boolean result depending of property 'disabled' state for element with locator {locator}")
    def _is_element_editable(self, locator: tuple, disabled: bool):
        self._logger.info(msg=f"Return boolean result depending on property 'disabled' state for element with"
                              f" locator {locator}")
        result = (self._find_element(locator=locator).get_property(name="disabled") == disabled)
        with allure.step(f"Returned result is {result}"):
            self._logger.info(msg=f"Returned result is {result}")
            return result

    @allure.step("Check if element with locator {locator} has required state of property 'disabled'")
    def _check_element_editable(self, locator: tuple, disabled: bool, timeout: int = -1):
        def __is_element_editable():
            def __wrapper(__driver):
                return self._is_element_editable(locator=locator, disabled=disabled)

            return __wrapper

        self._logger.info(msg=f"Check if element with locator {locator} has required state of property 'disabled'")
        try:
            if timeout < 0:
                timeout = self._driver.timeout
            return WebDriverWait(driver=self._driver, timeout=timeout).until(method=__is_element_editable())
        except TimeoutException:
            state = "disabled" if disabled else "not disabled"
            self._logger.error(msg=f"Assertion Error: Can't find {state} element with locator {locator}")
            self._attach_screenshot()
            raise AssertionError(f"Can't find {state} element with locator {locator}")

    @allure.step("Enter value {value} into input with locator {locator}")
    def _fill_input(self, locator: tuple, value: str, timeout: int = -1):
        if timeout < 0:
            timeout = self._driver.timeout
        input_to_fill = self._click_element(locator=locator, timeout=timeout)
        self._press_keyboard_key(key="CTRL + A, DEL")
        input_to_fill.send_keys(value)
        self._logger.info(msg=f"Enter value \'{value}\' into input with locator {locator}")

    @allure.step("Enter value {value} by symbols into input with locator {locator}")
    def _fill_input_by_symbols(self, locator: tuple, value: str, timeout: int = -1):
        if timeout < 0:
            timeout = self._driver.timeout
        input_to_fill = self._click_element(locator=locator, timeout=timeout)
        self._press_keyboard_key(key="CTRL + A, DEL")
        for symbol in value:
            input_to_fill.send_keys(symbol)
            time.sleep(1)
        self._logger.info(msg=f"Enter value \'{value}\' by symbols into input with locator {locator}")

    @allure.step("Accept native browser alert")
    def _accept_native_alert(self, timeout: int = -1):
        try:
            if timeout < 0:
                timeout = self._driver.timeout
            alert = WebDriverWait(driver=self._driver, timeout=timeout).until(method=ec.alert_is_present())
        except TimeoutException:
            self._logger.error(msg=f"Assertion Error: Can't find native browser alert")
            self._attach_screenshot()
            raise AssertionError("Can't find native browser alert")
        else:
            self._logger.info(msg="Accept native browser alert")
            alert.accept()

    @allure.step("Press keyboard key {key}")
    def _press_keyboard_key(self, key: str, timeout: int = 0):
        time.sleep(timeout)  # TODO: Probably this timeout is not needed
        self._logger.info(msg=f"Press keyboard key {key}")
        keyboard.send(hotkey=key)

    def _refresh(self):
        self._driver.refresh()
        return self
