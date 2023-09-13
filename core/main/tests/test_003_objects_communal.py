import pytest
from core.main.sections.objects_communal.objects_communal_page import ObjectsCommunalPage
from core.main.sections.objects_communal.object_communal_form import ObjectCommunalForm


@pytest.mark.parametrize("area_key", ["electro", "drainage"])
def test_object_communal_card_create_save(run_test, area_key):
    gkh_card = ObjectsCommunalPage(driver=run_test)
    user_credentials = gkh_card._auth.get_credentials(user="autotest_01")
    gkh_card._smart_open(credentials=user_credentials)
    object_card = None
    try:
        form_card = ObjectCommunalForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_object_communal_{area_key}.json"
        template = form_card._prepare_data_from_template(filename=filename, area_key=area_key)
        object_card = form_card._fill_new_card_object(template=template['Object_GKH'], save=True)
        form_card._check_data_object_gkh(template=template['Object_GKH'])
        form_card._fill_main_properties(template=template['Main_Properties'], area_key=area_key)
        form_card._check_data_main_properties(template=template['Main_Properties'])
    finally:
        gkh_card._goto()._delete_card(key=object_card, confirm=True, into="objects_communal")


@pytest.mark.parametrize("area_key", ["electro", "drainage"])
def test_object_communal_card_create_cancel(run_test, area_key):
    gkh_card = ObjectsCommunalPage(driver=run_test)
    user_credentials = gkh_card._auth.get_credentials(user="autotest_01")
    gkh_card._smart_open(credentials=user_credentials)
    object_card = None
    try:
        form_card = ObjectCommunalForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_object_communal_{area_key}.json"
        template = form_card._prepare_data_from_template(filename=filename, area_key=area_key)
        object_card = form_card._fill_new_card_object(template=template['Object_GKH'], save=False)
    finally:
        gkh_card._goto()._delete_card(key=object_card, confirm=True, into="objects_communal")


@pytest.mark.parametrize("area_key", ["electro", "drainage"])
def test_object_communal_card_check_edit(run_test, area_key):
    gkh_card = ObjectsCommunalPage(driver=run_test)
    user_credentials = gkh_card._auth.get_credentials(user="autotest_01")
    gkh_card._smart_open(credentials=user_credentials)
    object_card = None
    try:
        form_card = ObjectCommunalForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_object_communal_{area_key}.json"
        template = form_card._prepare_data_from_template(filename=filename, area_key=area_key)
        object_card = form_card._fill_new_card_object(template=template['Object_GKH'], save=True)
        form_card._fill_main_properties(template=template['Main_Properties'], area_key=area_key)
        form_card._check_data_main_properties(template=template['Main_Properties'])
        form_card._edit_card(template=template['Main_Properties'])
    finally:
        gkh_card._goto()._delete_card(key=object_card, confirm=True, into="objects_communal")
