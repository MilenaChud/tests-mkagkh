import pytest
from core.main.sections.plans_standard.plans_standard_page import PlansStandardEventsPage
from core.main.sections.plans_standard.plan_standard_form import PlanStandardEventsForm


@pytest.mark.parametrize("area_key", ["heating"])
def test_standard_plans_save(run_test, area_key):
    page_events = PlansStandardEventsPage(driver=run_test)
    user_credentials = page_events._auth.get_credentials(user="autotest_01")
    page_events._smart_open(credentials=user_credentials)
    template = None
    try:
        new_event = PlanStandardEventsForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_plan_standard_{area_key}.json"
        template = new_event._prepare_data_from_template(filename=filename, area_key=area_key)
        new_event._fill_plans(template=template['Incident'], save=True)
        new_event._check_tab(template=template['Incident'])
    finally:
        page_events._goto()._delete_card(key=template['Incident']['NameEvent'], confirm=True, into="plans_standard",
                                         template=template['Incident'])


@pytest.mark.parametrize("area_key", ["heating"])
def test_standard_plans_cancel(run_test, area_key):
    page_events = PlansStandardEventsPage(driver=run_test)
    user_credentials = page_events._auth.get_credentials(user="autotest_01")
    page_events._smart_open(credentials=user_credentials)
    new_event = PlanStandardEventsForm(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_plan_standard_{area_key}.json"
    template = new_event._prepare_data_from_template(filename=filename, area_key=area_key)
    new_event._fill_plans(template=template['Incident'])


@pytest.mark.parametrize("area_key", ["heating"])
def test_plans_events_edite(run_test, area_key):
    page_events = PlansStandardEventsPage(driver=run_test)
    user_credentials = page_events._auth.get_credentials(user="autotest_01")
    page_events._smart_open(credentials=user_credentials)
    template = None
    try:
        new_event = PlanStandardEventsForm(driver=run_test)
        filename = f"{run_test.data_paths['templates']}/template_plan_standard_{area_key}.json"
        template = new_event._prepare_data_from_template(filename=filename, area_key=area_key)
        new_event._fill_plans(template=template['Incident'], save=True)
        new_event._check_tab(template=template['Incident'])
        new_event._edite_card(template=template['Incident'])
    finally:
        page_events._goto()._delete_card(key=template['Incident']['NameEvent'], confirm=True, into="plans_standard",
                                         template=template['Incident'])
