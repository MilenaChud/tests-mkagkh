# ***
# Разработать автотесты по тест-кейсам:
# https://jira.iskrauraltel.ru/browse/MKAGKH-1074
# https://jira.iskrauraltel.ru/browse/MKAGKH-1045
# ***

import allure
import pytest
from core.helpers.app_auth_helper import AppAuthHelper
from core.main.sections.organizations.organization_form import OrganizationForm
from core.main.sections.organizations.organizations_page import OrganizationsPage
from core.main.sections.users.users_page import UsersPage
from core.main.sections.users.user_form import UserForm


@allure.title("Test authorization with invalid credentials")
@pytest.mark.parametrize("user_credentials_invalid", [
    {"Username": "", "Password": ""},
    {"Username": "", "Password": "1"},
    {"Username": "autotest_01", "Password": ""},
    {"Username": "autotest_01", "Password": "2"}
])
def test_authorization_negative(run_test, user_credentials_invalid):
    auth = AppAuthHelper(driver=run_test)
    auth.smart_login(credentials=user_credentials_invalid, valid=False)


@allure.title("Test authorization with valid credentials")
@pytest.mark.parametrize("user_credentials_valid", [
    {"Username": "autotest_01", "Password": "1"}
])
def test_authorization_positive(run_test, user_credentials_valid):
    auth = AppAuthHelper(driver=run_test)
    auth.smart_login(credentials=user_credentials_valid, valid=True)
    auth.smart_logout()


@allure.title("Test new user creation")
def test_create_user(run_test):
    with allure.step("Prepare new user data"):
        user_form = UserForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_user_all.json"
        user = user_form._prepare_data_from_template(filename=filename, area_key="all")
        user = user_form._modify_template_data(template=user)
        user_credentials = {
            "Username": user['Username'],
            "Password": user['Password'],
        }
        username = None

    with allure.step("Login with admin credentials"):
        users_page = UsersPage(driver=run_test)
        admin_credentials = users_page._auth.get_credentials(user="admin")
        users_page._smart_open(credentials=admin_credentials)

    try:
        with allure.step("Fill new user data and press 'Cancel' button"):
            user_form._fill_data(template=user, save=False)

        with allure.step("Check that new user can't be found"):
            assert user_form._find_card_by_key(key=user['Username'], presence=False, close_search=True, into="users")

        with allure.step("Fill new user data and press 'Save' button"):
            user_form._fill_data(template=user, save=True)
            username = user['Username']

        with allure.step("Find, open and close card of created user"):
            users_page._open_card_by_key(key=user['Username'], into="users")
            user_form._close()

        with allure.step("Login with created user credentials and invalid data for password update"):
            user_credentials['PasswordNew'] = "2"
            user_credentials['PasswordConfirm'] = "3"
            users_page._auth.smart_login(credentials=user_credentials, password_update_valid=False)

        with allure.step("Login with created user credentials and valid data for password update"):
            user_credentials['PasswordNew'] = user['PasswordNew']
            user_credentials['PasswordConfirm'] = user['PasswordConfirm']
            users_page._auth.smart_login(credentials=user_credentials, password_update_valid=True)

        with allure.step("Login with admin credentials"):
            users_page._auth.smart_login(credentials=admin_credentials)

        with allure.step("Check that created user is present in the employees list of corresponding organization"):
            organizations_page = OrganizationsPage(driver=run_test)
            organization_form = OrganizationForm(driver=run_test)
            organizations_page._goto()
            organizations_page._open_card_by_key(key=user['Organization'], into="organizations")
            organization_form._switch_tab(tab_name="Список сотрудников")
            assert organization_form._tab_employees._find_employee(employee=user) > 0

        with allure.step("Delete created user without confirmation"):
            users_page._goto()._delete_card(key=user['Username'], confirm=False, into="users")

        with allure.step("Check that created user is present in the employees list of corresponding organization"):
            organizations_page._goto()
            organizations_page._open_card_by_key(key=user['Organization'], into="organizations")
            organization_form._switch_tab(tab_name="Список сотрудников")
            assert organization_form._tab_employees._find_employee(employee=user) > 0

        with allure.step("Delete created user with confirmation"):
            users_page._goto()._delete_card(key=user['Username'], confirm=True, into="users")
            username = None

        with allure.step("Check that deleted user is absent in the employees list of corresponding organization"):
            organizations_page._goto()
            organizations_page._open_card_by_key(key=user['Organization'], into="organizations")
            organization_form._switch_tab(tab_name="Список сотрудников")
            assert organization_form._tab_employees._find_employee(employee=user) < 0

        with allure.step("Check that deleted user credentials are blocked"):
            user_credentials['Password'] = user['PasswordNew']
            users_page._auth.smart_login(credentials=user_credentials, blocked=True)

    finally:
        with allure.step("Delete created user if it was not done before"):
            execute = (username is not None)
            users_page._smart_open(credentials=admin_credentials, execute=execute)
            users_page._delete_card(key=username, confirm=True, into="users")


@allure.title("Test new superuser creation")
def test_create_superuser(run_test):
    with allure.step("Prepare new superuser data"):
        user_form = UserForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_superuser_all.json"
        superuser = user_form._prepare_data_from_template(filename=filename, area_key="all")
        superuser = user_form._modify_template_data(template=superuser, superuser=True)
        superuser_credentials = {
            "Username": superuser['Username'],
            "Password": superuser['Password'],
        }
        username = None

    with allure.step("Login with admin credentials"):
        users_page = UsersPage(driver=run_test)
        admin_credentials = users_page._auth.get_credentials(user="admin")
        users_page._smart_open(credentials=admin_credentials)

    try:
        with allure.step("Fill new superuser data and press 'Cancel' button"):
            user_form._fill_data(template=superuser, save=False, superuser=True)

        with allure.step("Check that new superuser can't be found"):
            assert user_form._find_card_by_key(key=superuser['Username'], presence=False, close_search=True,
                                               into="users")

        with allure.step("Fill new superuser data and press 'Save' button"):
            user_form._fill_data(template=superuser, save=True, superuser=True)
            username = superuser['Username']

        with allure.step("Find, open and close card of created superuser"):
            users_page._open_card_by_key(key=superuser['Username'], into="users")
            user_form._close()

        with allure.step("Login with created superuser credentials and invalid data for password update"):
            superuser_credentials['PasswordNew'] = "2"
            superuser_credentials['PasswordConfirm'] = "3"
            users_page._auth.smart_login(credentials=superuser_credentials, password_update_valid=False)

        with allure.step("Login with created superuser credentials and valid data for password update"):
            superuser_credentials['PasswordNew'] = superuser['PasswordNew']
            superuser_credentials['PasswordConfirm'] = superuser['PasswordConfirm']
            users_page._auth.smart_login(credentials=superuser_credentials, password_update_valid=True)

        with allure.step("Login with admin credentials"):
            users_page._smart_open(credentials=admin_credentials)

        with allure.step("Delete created superuser without confirmation"):
            users_page._delete_card(key=superuser['Username'], confirm=False, into="users")

        with allure.step("Delete created superuser with confirmation"):
            users_page._delete_card(key=superuser['Username'], confirm=True, into="users")
            username = None

        with allure.step("Check that deleted superuser credentials are blocked"):
            superuser_credentials['Password'] = superuser['PasswordNew']
            users_page._auth.smart_login(credentials=superuser_credentials, blocked=True)

    finally:
        with allure.step("Delete created superuser if it was not done before"):
            execute = (username is not None)
            users_page._smart_open(credentials=admin_credentials, execute=execute)
            users_page._delete_card(key=username, confirm=True, into="users")
