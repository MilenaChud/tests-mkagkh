import allure
import pytest
from core.main.sections.organizations.organization_form import OrganizationForm
from core.main.sections.organizations.organizations_page import OrganizationsPage
from core.main.sections.users.user_form import UserForm
from core.main.sections.users.users_page import UsersPage


@pytest.mark.parametrize("area_key", ["all"])
def test_organization_create(run_test, area_key):
    users_page = UsersPage(driver=run_test)
    user_form = UserForm(driver=run_test)
    admin_credentials = users_page._auth.get_credentials(user="admin")
    user_credentials = users_page._auth.get_credentials(user="autotest_03")

    organizations_page = OrganizationsPage(driver=run_test)
    organization_form = OrganizationForm(driver=run_test)
    organizations_page._smart_open(credentials=user_credentials)

    filename = f"{run_test.data_paths['templates']}/template_organization_{area_key}.json"
    organization = organization_form._prepare_data_from_template(filename=filename, area_key="all")
    organization_key = None

    try:
        organization_key = organizations_page._add_card(template=organization['Information'], save=False)
        assert organizations_page._find_card_by_key(key=organization_key, presence=False, close_search=True,
                                                    into="organizations")
        organization_key = organizations_page._add_card(template=organization['Information'], save=True)
        # TODO: Проверка сохраненных данных

        users_page._smart_open(credentials=admin_credentials)
        users_page._open_card_by_key(key='autotest_03', into="users")
        user_form._set_organization(name=organization_key)

        organizations_page._smart_open(credentials=user_credentials)
        organizations_page._goto()._open_card_by_key(key=organization_key, into="organizations")
        organization_form._switch_tab(tab_name="Список сотрудников")

        organization_form._tab_employees._add_employees(employees=organization['Employees'], employees_save=True,
                                                        save=False)
        # TODO: Поиск добавленных сотрудников
        # TODO: Удаление сотрудника

    finally:
        users_page._smart_open(credentials=admin_credentials)
        users_page._open_card_by_key(key='autotest_03', into="users")
        user_form._set_organization(name=user_credentials['Organization'])
        organizations_page._goto()._delete_card(key=organization_key, confirm=True, into="organizations")
