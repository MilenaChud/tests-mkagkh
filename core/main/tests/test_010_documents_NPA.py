import pytest
from core.main.sections.documents_and_NPA.documents_NPA_page import DocumentsNPAPage
from core.main.sections.documents_and_NPA.documents_NPA_form import DocumentsNPAForm


@pytest.mark.parametrize("area_key", ["public_utilities"])
def test_documents_NPA_card_save(run_test, area_key):
    page_npa = DocumentsNPAPage(driver=run_test)
    user_credentials = page_npa._auth.get_credentials(user="autotest_01")
    page_npa._smart_open(credentials=user_credentials)
    template = None
    try:
        npa_form = DocumentsNPAForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_documents_{area_key}.json"
        template = npa_form._prepare_data_from_template(filename=filename, area_key=area_key)
        file = f"{run_test.data_paths['uploads']}/autotest_upload_cat.jpeg"
        npa_form._fill_start_documents_card(template=template['StartData'], file=file)
        npa_form._check_tab_start(template=template['StartData'])
    finally:
        page_npa._goto()._delete_card(key=template['StartData']['NameDocument'], confirm=True, into="documents_npa")


@pytest.mark.parametrize("area_key", ["public_utilities"])
def test_documents_NPA_card_cancel(run_test, area_key):
    page_npa = DocumentsNPAPage(driver=run_test)
    user_credentials = page_npa._auth.get_credentials(user="autotest_01")
    page_npa._smart_open(credentials=user_credentials)
    npa_form = DocumentsNPAForm(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_documents_{area_key}.json"
    template = npa_form._prepare_data_from_template(filename=filename, area_key=area_key)
    file = f"{run_test.data_paths['uploads']}/autotest_upload_cat.jpeg"
    npa_form._fill_start_documents_card(template=template['StartData'], file=file, save=False)
    page_npa._find_by_key(key=template['StartData']['NameDocument'], template=template["AreaSearch"], presence=False)


@pytest.mark.parametrize("area_key", ["public_utilities"])
def test_documents_NPA_card_edite(run_test, area_key):
    page_npa = DocumentsNPAPage(driver=run_test)
    user_credentials = page_npa._auth.get_credentials(user="autotest_01")
    page_npa._smart_open(credentials=user_credentials)
    template = None
    try:
        npa_form = DocumentsNPAForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_documents_{area_key}.json"
        template = npa_form._prepare_data_from_template(filename=filename, area_key=area_key)
        file = f"{run_test.data_paths['uploads']}/autotest_upload_cat.jpeg"
        npa_form._fill_start_documents_card(template=template['StartData'], file=file)
        page_npa._open_by_key(key=template['StartData']['NameDocument'], template=template['StartData'])
        npa_form._edit_tab(template=template['EditeData'], save=True)
        npa_form._check_tab_start(template=template['EditeData'])
    finally:
        page_npa._goto()._delete_card(key=template['StartData']['NameDocument'], confirm=True, into="documents_npa", template=template['StartData'])
