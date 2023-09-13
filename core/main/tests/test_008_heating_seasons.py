import pytest
from core.main.sections.heating_seasons.heating_seasons_page import HeatingSeasonsPage
from core.main.sections.heating_seasons.heating_season_form import HeatingSeasonForm


@pytest.mark.parametrize("area_key", ["all"])
def test_heating_seasons_card_save(run_test, area_key):
    page_seasons = HeatingSeasonsPage(driver=run_test)
    user_credentials = page_seasons._auth.get_credentials(user="autotest_01")
    page_seasons._smart_open(credentials=user_credentials)
    municipality = None
    try:
        new_season = HeatingSeasonForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_heating_season_{area_key}.json"
        template = new_season._prepare_data_from_template(filename=filename, area_key=area_key)
        file_pdf = f"{run_test.data_paths['uploads']}/autotest_upload_2.pdf"
        municipality = template['Start']['Municipality']['ShortValue']
        new_season._fill_start_heating_plans(template=template['Start'], file_pdf=file_pdf)
        new_season._fill_final_heating_plans(template=template['Final'], file_pdf=file_pdf)
        page_seasons._goto()._open_by_key(key=municipality)
        new_season._check_tab_start(template=template['Start'])
        new_season._check_tab_final(template=template['Final'], edited=False)

    finally:
        page_seasons._goto()._delete_card(key=municipality, confirm=True, into="heating_seasons")


@pytest.mark.parametrize("area_key", ["all"])
def test_heating_seasons_card_cancel(run_test, area_key):
    page_seasons = HeatingSeasonsPage(driver=run_test)
    user_credentials = page_seasons._auth.get_credentials(user="autotest_01")
    page_seasons._smart_open(credentials=user_credentials)
    new_season = HeatingSeasonForm(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_heating_season_{area_key}.json"
    template = new_season._prepare_data_from_template(filename=filename, area_key=area_key)
    file_pdf = f"{run_test.data_paths['uploads']}/autotest_upload_2.pdf"
    municipality = template['Start']['Municipality']['ShortValue']
    new_season._fill_start_heating_plans(template=template['Start'], file_pdf=file_pdf)
    new_season._fill_final_heating_plans(template=template['Final'], file_pdf=file_pdf, save=False)

    # Создаваемая из шаблона карточка отопительного сезона должна быть уникальной - тогда можно проверять, что ничего не создалось
    page_seasons._find_by_key(key=municipality, presence=False, template=template)


@pytest.mark.parametrize("area_key", ["all"])
def test_heating_seasons_card_edit_save(run_test, area_key):
    page_seasons = HeatingSeasonsPage(driver=run_test)
    user_credentials = page_seasons._auth.get_credentials(user="autotest_01")
    page_seasons._smart_open(credentials=user_credentials)
    municipality = None
    try:
        new_season = HeatingSeasonForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_heating_season_{area_key}.json"
        template = new_season._prepare_data_from_template(filename=filename, area_key=area_key)
        file_pdf = f"{run_test.data_paths['uploads']}/autotest_upload_2.pdf"
        municipality = template['Start']['Municipality']['ShortValue']
        new_season._fill_start_heating_plans(template=template['Start'], file_pdf=file_pdf)
        new_season._fill_final_heating_plans(template=template['Final'], file_pdf=file_pdf)
        page_seasons._goto()._open_by_key(key=municipality, template=template)
        new_season._edit_tab(template=template['Final'], save=True)
        page_seasons._goto()._open_by_key(key=municipality, template=template)
        new_season._check_tab_final(template=template['Final'], edited=True)
    finally:
        page_seasons._goto()._delete_card(key=municipality, confirm=True, into="heating_seasons")


@pytest.mark.parametrize("area_key", ["all"])
def test_heating_seasons_card_edit_cancel(run_test, area_key):
    page_seasons = HeatingSeasonsPage(driver=run_test)
    user_credentials = page_seasons._auth.get_credentials(user="autotest_01")
    page_seasons._smart_open(credentials=user_credentials)
    municipality = None
    try:
        new_season = HeatingSeasonForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_heating_season_{area_key}.json"
        template = new_season._prepare_data_from_template(filename=filename, area_key=area_key)
        file_pdf = f"{run_test.data_paths['uploads']}/autotest_upload_2.pdf"
        municipality = template['Start']['Municipality']['ShortValue']
        new_season._fill_start_heating_plans(template=template['Start'], file_pdf=file_pdf)
        new_season._fill_final_heating_plans(template=template['Final'], file_pdf=file_pdf)
        page_seasons._goto()._open_by_key(key=municipality, template=template)
        new_season._edit_tab(template=template['Final'], save=False)
        page_seasons._goto()._open_by_key(key=municipality, template=template)
        new_season._check_tab_final(template=template['Final'], edited=False)
    finally:
        page_seasons._goto()._delete_card(key=municipality, confirm=True, into="heating_seasons")
