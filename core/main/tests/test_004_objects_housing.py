import pytest
from core.main.sections.objects_housing.objects_housing_page import ObjectsHousingPage
from core.main.sections.objects_housing.object_housing_form import ObjectHousingForm


@pytest.mark.parametrize("area_key", ["simple"])
def test_object_housing_create_save(run_test, area_key):
    live_object = ObjectsHousingPage(driver=run_test)
    user_credentials = live_object._auth.get_credentials(user="autotest_01")
    live_object._smart_open(credentials=user_credentials)
    template = None
    try:
        form_register = ObjectHousingForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_object_housing_{area_key}.json"
        template = form_register._prepare_data_from_template(filename=filename, area_key=area_key)
        form_register._fill_new_card_object(template=template['LiveHouse'], save=True, double=False)
        form_register._check_data_object_living_house(template=template['LiveHouse'])
        form_register._fill_new_service_inf(template=template['ServiceInformation'], save=True, switch=False)
        form_register._check_service_inf(template=template['ServiceInformation'])

    finally:
        live_object._goto()._delete_card(key=template['LiveHouse']['FullAddress'], confirm=True,
                                         into="objects_housing", other=template['LiveHouse']['Address'])


@pytest.mark.parametrize("area_key", ["simple"])
def test_object_housing_create_cancel(run_test, area_key):
    live_object = ObjectsHousingPage(driver=run_test)
    user_credentials = live_object._auth.get_credentials(user="autotest_01")
    live_object._smart_open(credentials=user_credentials)
    template = None
    try:
        form_register = ObjectHousingForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_object_housing_{area_key}.json"
        template = form_register._prepare_data_from_template(filename=filename, area_key=area_key)
        form_register._fill_new_card_object(template=template['LiveHouse'], save=True, double=False)
        form_register._check_data_object_living_house(template=template['LiveHouse'])
        form_register._fill_new_service_inf(template=template['ServiceInformation'], save=False, switch=False)

    finally:
        live_object._goto()._delete_card(key=template['LiveHouse']['FullAddress'], confirm=True,
                                         into="objects_housing", other=template['LiveHouse']['Address'])


@pytest.mark.parametrize("area_key", ["simple"])
def test_object_housing_switch_tab(run_test, area_key):
    live_object = ObjectsHousingPage(driver=run_test)
    user_credentials = live_object._auth.get_credentials(user="autotest_01")
    live_object._smart_open(credentials=user_credentials)
    template = None
    try:
        form_register = ObjectHousingForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_object_housing_{area_key}.json"
        template = form_register._prepare_data_from_template(filename=filename, area_key=area_key)
        form_register._fill_new_card_object(template=template['LiveHouse'], save=True, double=False)
        form_register._check_data_object_living_house(template=template['LiveHouse'])
        form_register._fill_new_service_inf(template=template['ServiceInformation'], save=False, switch=True)

    finally:
        live_object._goto()._delete_card(key=template['LiveHouse']['FullAddress'], confirm=True,
                                         into="objects_housing", other=template['LiveHouse']['Address'])


@pytest.mark.parametrize("area_key", ["double"])
def test_object_housing_double_data(run_test, area_key):
    live_object = ObjectsHousingPage(driver=run_test)
    user_credentials = live_object._auth.get_credentials(user="autotest_01")
    live_object._smart_open(credentials=user_credentials)
    template = None
    try:
        form_register = ObjectHousingForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_object_housing_{area_key}.json"
        template = form_register._prepare_data_from_template(filename=filename, area_key=area_key)
        form_register._fill_new_card_object(template=template['LiveHouse'], save=True, double=True)
        form_register._check_data_object_living_house(template=template['LiveHouse'])

    finally:
        live_object._goto()._delete_card(key=template['LiveHouse']['FullAddress'], confirm=True,
                                         into="objects_housing", other=template['LiveHouse']['Address'])
