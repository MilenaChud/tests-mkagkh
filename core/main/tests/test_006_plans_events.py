import pytest
from core.main.sections.plans_events.plans_events_page import PlansEventsPage
from core.main.sections.plans_events.plan_event_form import PlansEventsForm


@pytest.mark.parametrize("area_key", ["electro"])
def test_plans_events_create_save(run_test, area_key):
    page_events = PlansEventsPage(driver=run_test)
    user_credentials = page_events._auth.get_credentials(user="autotest_01")
    page_events._smart_open(credentials=user_credentials)
    template = None
    try:
        new_event = PlansEventsForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_plan_event_{area_key}.json"
        template = new_event._prepare_data_from_template(filename=filename, area_key=area_key)

        new_event._fill_plans(template=template['Incident'], save=True)
        new_event._fill_extra_information(template=template['Incident'])
        new_event._check_describe_events(template=template['Incident'])
        filename = f"{run_test.data_paths['uploads']}/autotest_upload_cat.jpeg"
        new_event._upload_files(filename=filename)
    finally:
        page_events._goto()._delete_card(key=template['Incident']['TypeEvents'], confirm=True, into="plans_events",
                                         template=template['Incident'])


@pytest.mark.parametrize("area_key", ["electro"])
def test_plans_events_create_cancel(run_test, area_key):
    page_events = PlansEventsPage(driver=run_test)
    user_credentials = page_events._auth.get_credentials(user="autotest_01")
    page_events._smart_open(credentials=user_credentials)
    new_event = PlansEventsForm(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_plan_event_{area_key}.json"
    template = new_event._prepare_data_from_template(filename=filename, area_key=area_key)

    new_event._fill_plans(template=template['Incident'])


@pytest.mark.parametrize("area_key", ["electro"])
def test_plans_events_edite(run_test, area_key):
    page_events = PlansEventsPage(driver=run_test)
    user_credentials = page_events._auth.get_credentials(user="autotest_01")
    page_events._smart_open(credentials=user_credentials)
    template = None
    try:
        new_event = PlansEventsForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_plan_event_{area_key}.json"
        template = new_event._prepare_data_from_template(filename=filename, area_key=area_key)

        new_event._fill_plans(template=template['Incident'], save=True)
        new_event._fill_extra_information(template=template['Incident'])
        new_event._check_describe_events(template=template['Incident'])
        filename = f"{run_test.data_paths['uploads']}/autotest_upload_cat.jpeg"
        new_event._upload_files(filename=filename, save=False)
        new_event._edite_card(template=template['Incident'])
    finally:
        page_events._goto()._delete_card(key=template['Incident']['TypeEvents'], confirm=True, into="plans_events",
                                         template=template['Incident'])
