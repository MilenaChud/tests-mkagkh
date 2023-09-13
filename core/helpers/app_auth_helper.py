import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from core.helpers.base_helper import BaseHelper


class AppAuthHelper(BaseHelper):
    # Locators
    LOGIN_TITLE = (By.XPATH, "//h1[@id='kc-page-title' and contains(text(), 'Вход в учетную запись')]")
    PASSWORD_UPDATE_TITLE = (By.XPATH, "//h1[@id='kc-page-title' and contains(text(), 'Обновление пароля')]")
    USERNAME_INPUT = (By.XPATH, "//input[@id='username']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='password']")
    PASSWORD_NEW_INPUT = (By.XPATH, "//input[@id='password-new']")
    PASSWORD_CONFIRM_INPUT = (By.XPATH, "//input[@id='password-confirm']")
    LOGO = (By.XPATH, "//div[contains(@class, 'headerLogo')]")
    USER_PROFILE_BUTTON = (By.XPATH, "//img[contains(@src, 'lk-user')]/../parent::button")
    LOGIN_BUTTON = (By.XPATH, "//input[@id='kc-login' and @value='Вход']")
    CONFIRM_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Подтвердить']")
    LOGOUT_BUTTON = (By.XPATH, "//li[contains(text(), 'Выйти')]")
    MESSAGE_INVALID_LOGIN = (By.XPATH, "//span[contains(text(), 'Неправильное имя пользователя или пароль')]")
    MESSAGE_INVALID_PASSWORD_UPDATE = (By.XPATH, "//span[contains(text(), 'Пароли не совпадают')]")
    MESSAGE_BLOCKED_LOGIN = (By.XPATH, "//span[contains(text(), 'Учетная запись заблокирована, свяжитесь с "
                                       "администратором')]")

    __user = None

    @allure.step("Get credentials for user {user}")
    def get_credentials(self, user: str, filename: str = "data/templates/users_credentials.json"):
        self._logger.info(f"Get credentials for user \'{user}\'")
        data = self._read_data_from_file(filename=filename)
        credentials = list(filter(lambda item: item['Username'] == user, data))
        if len(credentials) > 0:
            with allure.step("Successfully get user credentials"):
                self._logger.info(msg="Successfully get user credentials")
                return credentials[0]
        else:
            with allure.step(f"Failed to get user credentials - can't find user \'{user}\' in file \'{filename}\'"):
                self._logger.error(msg=f"Assertion Error: Failed to get user credentials - can't find user \'{user}\' "
                                       f" in file \'{filename}\'")
                raise AssertionError(f"Failed to get user credentials - can't find user \'{user}\'"
                                     f" in file \'{filename}\'")

    @allure.step("Execute login attempt with credentials: {credentials}")
    def _login(self, credentials: dict, valid: bool, blocked: bool, password_update_valid: bool):
        self._logger.info(f"Execute login attempt with credentials {credentials}")
        self._check_element_visible(locator=self.LOGIN_TITLE)
        self._fill_input(locator=self.USERNAME_INPUT, value=credentials['Username'])
        self._fill_input(locator=self.PASSWORD_INPUT, value=credentials['Password'])
        self._click_element(locator=self.LOGIN_BUTTON)
        if valid:
            if blocked:
                self._check_element_visible(locator=self.MESSAGE_BLOCKED_LOGIN)
                self._check_element_visible(locator=self.LOGIN_TITLE)
                with allure.step(f"Successful check that given credentials are blocked for login"):
                    self._logger.info(msg=f"Successful check that given credentials are blocked for login")
            elif self._check_password_update(credentials=credentials, valid=password_update_valid):
                try:
                    self._check_element_visible(self.LOGO, raise_error=False)
                except NoSuchElementException:
                    with allure.step(f"Failed login with given credentials: {credentials}"):
                        self._logger.error(msg=f"Failed login with given credentials: {credentials}")
                        self._check_element_visible(locator=self.MESSAGE_INVALID_LOGIN)
                        self._check_element_visible(locator=self.LOGIN_TITLE)
                        self._logger.error(msg="Given credentials are invalid for login")
                        raise AssertionError("Given credentials are invalid for login")
                else:
                    with allure.step(f"Successful login with given credentials"):
                        self._logger.info(msg=f"Successful login with given credentials")
                        AppAuthHelper.__user = credentials['Username']
        else:
            self._check_element_visible(locator=self.MESSAGE_INVALID_LOGIN)
            self._check_element_visible(locator=self.LOGIN_TITLE)
            with allure.step(f"Successful check that given credentials are invalid for login"):
                self._logger.info(msg=f"Successful check that given credentials are invalid for login")

    @allure.step("Execute logout procedure")
    def _logout(self):
        self._check_element_visible(locator=self.LOGO)
        self._click_element(locator=self.USER_PROFILE_BUTTON)
        self._click_element(locator=self.LOGOUT_BUTTON)
        self._check_element_visible(locator=self.LOGIN_TITLE)
        with allure.step("Successful logout"):
            self._logger.info(msg=f"Successful logout")
            AppAuthHelper.__user = None

    @allure.step("Check password update procedure")
    def _check_password_update(self, credentials: dict, valid: bool = True):
        self._logger.info(f"Check password update procedure")
        stop = False
        if self._is_element_visible(locator=self.PASSWORD_UPDATE_TITLE, visibility=True, timeout=3):
            self._fill_input(locator=self.PASSWORD_NEW_INPUT, value=credentials['PasswordNew'])
            self._fill_input(locator=self.PASSWORD_CONFIRM_INPUT, value=credentials['PasswordConfirm'])
            self._click_element(locator=self.CONFIRM_BUTTON)
            if valid:
                try:
                    self._check_element_visible(self.LOGO, raise_error=False)
                except NoSuchElementException:
                    stop = True
                    with allure.step("Failed password update with given credentials: {credentials}"):
                        self._logger.error(msg=f"Failed password update with given credentials: {credentials}")
                        self._check_element_visible(locator=self.MESSAGE_INVALID_PASSWORD_UPDATE)
                        self._check_element_visible(locator=self.PASSWORD_UPDATE_TITLE)
                        self._logger.error(msg="Given credentials are invalid for password update")
                        raise AssertionError("Given credentials are invalid for password update")
                else:
                    with allure.step(f"Successful password update with given credentials"):
                        self._logger.info(msg=f"Successful password update with given credentials")
            else:
                stop = True
                self._check_element_visible(locator=self.MESSAGE_INVALID_PASSWORD_UPDATE)
                self._check_element_visible(locator=self.PASSWORD_UPDATE_TITLE)
                with allure.step(f"Successful check that given credentials are invalid for password update"):
                    self._logger.info(msg=f"Successful check that given credentials are invalid for password update")
        return not stop

    def smart_login(self, credentials: dict, valid: bool = True, blocked: bool = False,
                    password_update_valid: bool = True):
        if (AppAuthHelper.__user is not None) and (AppAuthHelper.__user != credentials['Username']):
            self._logout()
        if AppAuthHelper.__user is None:
            if self._is_element_visible(locator=self.LOGIN_TITLE, visibility=False, timeout=3):
                self._open()
            self._login(credentials=credentials, valid=valid, blocked=blocked,
                        password_update_valid=password_update_valid)

    def smart_logout(self):
        if AppAuthHelper.__user is not None:
            if self._is_element_visible(locator=self.LOGO, visibility=True, timeout=3):
                self._logout()
