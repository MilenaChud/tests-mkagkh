# ***
# Разработать автотесты по тест-кейсам:
# https://jira.iskrauraltel.ru/browse/MKAGKH-1006
# https://jira.iskrauraltel.ru/browse/MKAGKH-1007
# ***

import allure
import pytest
import time
from datetime import datetime
from core.main.sections.events.events_page import EventsPage
from core.main.sections.events.event_form_start import EventFormStart
from core.main.sections.events.event_form_full import EventFormFull
from core.main.sections.objects_communal.objects_communal_page import ObjectsCommunalPage
from core.main.sections.objects_communal.object_communal_form import ObjectCommunalForm


@allure.title("Test new event card creation")
@pytest.mark.parametrize("area_key", ["electro"])
def test_event_card_create(run_test, area_key):
    events_page = EventsPage(driver=run_test)
    user_credentials = events_page._auth.get_credentials(user="autotest_01")
    events_page._smart_open(credentials=user_credentials)

    event_card_start = EventFormStart(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_event_{area_key}.json"
    event = event_card_start._prepare_data_from_template(filename=filename, area_key=area_key)

    event_description = event['StartData']['Description']
    event_card_key_1 = None
    try:
        event_card_key_1 = event_card_start._fill_data(template=event['StartData'], save=False)
        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._find_event_by_key(key=event_card_key_1, presence=False)

        print(f"\nCARD ONE: {datetime.now()}\n")

        event_card_key_1 = event_card_start._fill_data(template=event['StartData'], save=True)
        event['StartData']['Description'] = event_card_key_1
        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        time.sleep(2)
        events_page._open_event_by_key(key=event_card_key_1)

        event_card_full = EventFormFull(driver=run_test)
        event_card_tab = event_card_full._switch_tab(tab_name="ПЕРВИЧНЫЕ ДАННЫЕ")
        event_card_tab._check_data(template=event['StartData'])
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=False)

        event_card_tab = event_card_full._switch_tab(tab_name="ХАРАКТЕРИСТИКИ")
        event['Properties']['EmergencyData'] = {'Injured': 2, 'Lost': 1}
        event_properties = event_card_tab._get_data()
        event_card_tab._fill_data(template=event['Properties'], save=False)
        event_card_tab._check_data(template=event_properties)
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=False)

        event_card_tab._fill_data(template=event['Properties'], save=True, duplicate_save=True)
        event_card_tab._check_data(template=event['Properties'])
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=True)

        objects_page = ObjectsCommunalPage(driver=run_test)
        object_card = ObjectCommunalForm(driver=run_test)
        objects_page._goto()
        objects_page._open_card_by_key(key=event['Object']['Name'], into="objects_communal")
        object_data = object_card._get_data()

        events_page._goto()._check_event_alarm(key=event_card_key_1, alarm_scale="Локальный")
        time.sleep(15)

        # *** Create duplicate (second) card and delete it ***

        print(f"\nCARD TWO: {datetime.now()}\n")

        event['StartData']['Description'] = event_description
        event_card_key_2 = event_card_start._fill_data(template=event['StartData'], save=True)
        event['StartData']['Description'] = event_card_key_2
        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._open_event_by_key(key=event_card_key_2)

        event_card_tab = event_card_full._switch_tab(tab_name="ПЕРВИЧНЫЕ ДАННЫЕ")
        event_card_tab._check_data(template=event['StartData'])
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=False)

        event_card_tab = event_card_full._switch_tab(tab_name="ХАРАКТЕРИСТИКИ")
        event['Properties']['DuplicateKey'] = event_card_key_1
        event_card_tab._fill_data(template=event['Properties'], save=True, duplicate_save=False)

        event_card_full._check_description(key=event_card_key_1)

        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._find_event_by_key(key=event_card_key_2, presence=False)
        events_page._open_event_by_key(key=event_card_key_1)

        event_card_tab = event_card_full._switch_tab(tab_name="ХАРАКТЕРИСТИКИ")
        event['Properties']['EmergencyData'] = {'Injured': 0, 'Lost': 0}
        event_card_tab._edit_emergency_data(emergency_data=event['Properties']['EmergencyData'], save=True)
        event_card_tab._check_data(template=event['Properties'])
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=False)

        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._check_event_alarm(key=event_card_key_1, alarm_scale="Отсутствует")
        events_page._open_event_by_key(key=event_card_key_1)
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=False)

        event_card_tab = event_card_full._switch_tab(tab_name="ОБЪЕКТ")
        event_object = event_card_tab._get_data()
        event_card_tab._fill_data(template=event['Object'], save=False)
        event_card_tab._check_data(template=event_object)
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=False)

        event_card_tab._fill_data(template=event['Object'], save=True)
        event_card_tab._check_data(template=object_data)
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=False)

        event_card_tab = event_card_full._switch_tab(tab_name="ОГРАНИЧЕНИЯ")
        event_limitations = [{"NoData": "Данных не найдено"}]
        event['Limitations']['Full']['EmergencyData'] = {
            "MultiHouses": "0",
            "MultiPeople": "0",
            "SingleHouses": "2",
            "SinglePeople": "10"
        }
        event['Limitations']['Partial']['EmergencyData'] = {
            "MultiHouses": "0",
            "MultiPeople": "0",
            "SingleHouses": "0",
            "SinglePeople": "0"
        }
        event['Limitations']['Related']['EmergencyData'] = {
            "MultiHouses": "1",
            "MultiPeople": "100",
            "SingleHouses": "0",
            "SinglePeople": "0"
        }

        event_limitations_table = event_card_tab._get_table_data()
        event_card_tab._fill_data(template=event['Limitations']['Partial'], limitation_save=True, save=False)
        event_card_tab._check_data(template=event_limitations_table)
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=False)

        event_limitation_date_time = event_card_tab._fill_data(template=event['Limitations']['Partial'],
                                                               limitation_save=True, save=True)
        event['Limitations']['Partial']['DateTimeOnOff'] = event_limitation_date_time
        event_limitations = event_card_tab._add_to_list(current_list=event_limitations,
                                                        added=event['Limitations']['Partial'])
        event_card_tab._check_data(template=event_limitations)
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=False)
        # TODO: Вставить проверку events_page._check_event_alarm(key=event_card_key_1, emergency_type=event_card_emergency_type)

        event_limitations_table = event_card_tab._get_table_data()
        event_card_tab._fill_data(template=event['Limitations']['Full'], limitation_save=False, save=True)
        event_card_tab._check_data(template=event_limitations_table)
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=False)

        event_limitation_date_time = event_card_tab._fill_data(template=event['Limitations']['Full'],
                                                               limitation_save=True, save=True)
        event['Limitations']['Full']['DateTimeOnOff'] = event_limitation_date_time
        event_limitations = event_card_tab._add_to_list(current_list=event_limitations,
                                                        added=event['Limitations']['Full'])
        event_card_tab._check_data(template=event_limitations)
        event_card_full._check_attention_block(presence=True)
        # houses += int(event['Limitations']['Full']['EmergencyData']['MultiHouses']) + int(event['Limitations']['Full']['EmergencyData']['SingleHouses'])
        # people += int(event['Limitations']['Full']['EmergencyData']['MultiPeople']) + int(event['Limitations']['Full']['EmergencyData']['SinglePeople'])
        # event_card_emergency_type = event_card_tab._get_emergency_type(houses=houses, people=people)
        event_card_full._check_tab_emergency(presence=True)
        # TODO: Вставить проверку events_page._check_event_alarm(key=event_card_key_1, emergency_type=event_card_emergency_type)

        event_card_tab._delete_data(deleted_type="Частичное", delete_confirm=False, save=True)
        event_card_tab._check_data(template=event_limitations)
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=True)

        event_card_tab._delete_data(deleted_type="Полное", delete_confirm=True, save=True)
        event_limitations = event_card_tab._delete_from_list(current_list=event_limitations, deleted_type="Полное")
        event_card_tab._check_data(template=event_limitations)
        event_card_full._check_attention_block(presence=True)
        # houses -= int(event['Limitations']['Full']['EmergencyData']['MultiHouses']) + int(event['Limitations']['Full']['EmergencyData']['SingleHouses'])
        # people -= int(event['Limitations']['Full']['EmergencyData']['MultiPeople']) + int(event['Limitations']['Full']['EmergencyData']['SinglePeople'])
        # event_card_emergency_type = event_card_tab._get_emergency_type(houses=houses, people=people)
        event_card_full._check_tab_emergency(presence=False)
        # TODO: Вставить проверку events_page._check_event_alarm(key=event_card_key_1, emergency_type=event_card_emergency_type)

        event_limitation_date_time = event_card_tab._fill_data(template=event['Limitations']['Related'],
                                                               limitation_save=True, save=True)
        event['Limitations']['Related']['DateTimeOnOff'] = event_limitation_date_time
        event_limitations = event_card_tab._add_to_list(current_list=event_limitations,
                                                        added=event['Limitations']['Related'])
        event_card_tab._check_data(template=event_limitations)
        event_card_full._check_attention_block(presence=True)
        # houses += int(event['Limitations']['Related']['EmergencyData']['MultiHouses']) + int(event['Limitations']['Related']['EmergencyData']['SingleHouses'])
        # people += int(event['Limitations']['Related']['EmergencyData']['MultiPeople']) + int(event['Limitations']['Related']['EmergencyData']['SinglePeople'])
        # TODO: Правильно ли складываать houses и people из всех сохраненных ограничений?
        # event_card_emergency_type = event_card_tab._get_emergency_type(houses=houses, people=people)
        event_card_full._check_tab_emergency(presence=True)
        # TODO: Вставить проверку events_page._check_event_alarm(key=event_card_key_1, emergency_type=event_card_emergency_type)

        event_card_tab = event_card_full._switch_tab(tab_name="ДОПОЛНИТЕЛЬНО")
        event_responsibles = [{"NoData": "Данных не найдено"}]

        event_additional_data = event_card_tab._get_data()
        event_card_tab._fill_data(template=event['Additional'], save=False)
        event_card_tab._check_responsibles(template_list=event_additional_data['Responsibles'])
        event_card_tab._check_inputs(template=event_additional_data['Inputs'])

        event_card_tab._fill_data(template=event['Additional'], save=True)
        event_responsibles = event_card_tab._add_to_responsibles_list(current_list=event_responsibles,
                                                                      added_list=event['Additional']['Responsibles'])
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

        deleted = event['Additional']['Responsibles'][1]

        event_card_tab._delete_table_row(deleted=deleted, delete_confirm=False, save=True)
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

        event_card_tab._delete_table_row(deleted=deleted, delete_confirm=True, save=False)
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

        event_card_tab._delete_table_row(deleted=deleted, delete_confirm=True, save=True)
        event_responsibles = event_card_tab._delete_from_responsibles_list(current_list=event_responsibles,
                                                                           deleted=deleted)
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

        event_card_tab = event_card_full._switch_tab(tab_name="ФАЙЛЫ")
        file_png = f"{run_test.data_paths['uploads']}/{event['Files']['File_PNG']}"
        file_jpg = f"{run_test.data_paths['uploads']}/{event['Files']['File_JPG']}"
        file_pdf = f"{run_test.data_paths['uploads']}/{event['Files']['File_PDF']}"

        event_files = [{"NoData": "Данных не найдено"}]
        event_card_tab._add_file(filename=file_png, save=False)
        event_card_tab._check_files_list(template_list=event_files)

        event_card_tab._add_file(filename=file_jpg, save=True)
        event_files = event_card_tab._add_to_files_list(current_list=event_files, filename=file_jpg)
        event_card_full._refresh()._switch_tab(tab_name="ФАЙЛЫ")
        event_card_tab._check_files_list(template_list=event_files)

        event_card_tab._add_file(filename=file_pdf, save=True)
        event_files = event_card_tab._add_to_files_list(current_list=event_files, filename=file_pdf)
        event_card_full._refresh()._switch_tab(tab_name="ФАЙЛЫ")
        event_card_tab._check_files_list(template_list=event_files)

        event_card_tab._delete_file(filename=file_jpg, save=False)
        event_card_tab._check_files_list(template_list=event_files)

        event_card_tab._delete_file(filename=file_pdf, save=True)
        event_files = event_card_tab._delete_from_files_list(current_list=event_files, filename=file_pdf)
        event_card_tab._check_files_list(template_list=event_files)

        # *****
        event_card_tab = event_card_full._switch_tab(tab_name="УЧЁТ РЕЖИМА ЧС")
        event_data = event_card_tab._fill_data(template=event['Emergency'], save=False)
        event_card_full._check_attention_block(presence=False)
        event_card_full._check_tab_emergency(presence=True)

        event_data = event_card_tab._fill_data(template=event['Emergency'], save=True)
        event_card_full._check_attention_block(presence=False)
        event_card_full._check_tab_emergency(presence=True)

    finally:
        events_page._goto()._delete_card(key=event_card_key_1, confirm=True, into="events")


@pytest.mark.parametrize("area_key", ["electro"])
def test_experiment_limitatins(run_test, area_key):
    events_page = EventsPage(driver=run_test)
    user_credentials = events_page._auth.get_credentials(user="autotest_01")
    events_page._smart_open(credentials=user_credentials)

    event_card_start = EventFormStart(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_event_{area_key}.json"
    event = event_card_start._prepare_data_from_template(filename=filename, area_key=area_key)
    event_card_key = None
    try:
        event_card_emergency_type = "Нет угрозы ЧС"
        event_card_key = event_card_start._fill_data(template=event['StartData'], save=True)
        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._open_event_by_key(key=event_card_key)

        event_card_full = EventFormFull(driver=run_test)
        event_card_tab = event_card_full._switch_tab(tab_name="ОГРАНИЧЕНИЯ")

        event_limitations = [{"NoData": "Данных не найдено"}]

        event_limitations_table = event_card_tab._get_table_data()
        event_card_tab._fill_data(template=event['Limitations']['Partial'], limitation_save=True, save=False)
        event_card_tab._check_data(template=event_limitations_table)

        event_limitation_date_time = event_card_tab._fill_data(template=event['Limitations']['Partial'],
                                                               limitation_save=True, save=True)
        event['Limitations']['Partial']['DateTimeOnOff'] = event_limitation_date_time
        event_limitations = event_card_tab._add_to_list(current_list=event_limitations,
                                                        added=event['Limitations']['Partial'])
        event_card_tab._check_data(template=event_limitations)

        event_limitations_table = event_card_tab._get_table_data()
        event_card_tab._fill_data(template=event['Limitations']['Related'], limitation_save=False, save=True)
        event_card_tab._check_data(template=event_limitations_table)

        event_limitation_date_time = event_card_tab._fill_data(template=event['Limitations']['Related'],
                                                               limitation_save=True, save=True)
        event['Limitations']['Related']['DateTimeOnOff'] = event_limitation_date_time
        event_limitations = event_card_tab._add_to_list(current_list=event_limitations,
                                                        added=event['Limitations']['Related'])
        event_card_tab._check_data(template=event_limitations)

        event_card_tab._delete_data(deleted_type="Частичное", delete_confirm=True, save=True)
        event_limitations = event_card_tab._delete_from_list(current_list=event_limitations, deleted_type="Частичное")
        event_card_tab._check_data(template=event_limitations)

        # event_data = event_card_tab._edit_emergency_data(edited_type="Связанное", multi_houses=5, multi_people=200, limitation_save=True, save=True)
        # event_limitations = event_card_tab._edit_list(current_list=event_limitations, edited=event_data)
        # event_card_tab._check_data(template=event_limitations)

    finally:
        events_page._goto()._delete_card(key=event_card_key, confirm=True, into="events")


@pytest.mark.parametrize("area_key", ["electro"])
def test_experiment_additional(run_test, area_key):
    events_page = EventsPage(driver=run_test)
    user_credentials = events_page._auth.get_credentials(user="autotest_01")
    events_page._smart_open(credentials=user_credentials)

    event_card_start = EventFormStart(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_event_{area_key}.json"
    event = event_card_start._prepare_data_from_template(filename=filename, area_key=area_key)
    event_card_key = None
    try:
        event_card_emergency_type = "Нет угрозы ЧС"
        event_card_key = event_card_start._fill_data(template=event['StartData'], save=True)
        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._open_event_by_key(key=event_card_key)

        event_card_full = EventFormFull(driver=run_test)
        event_card_tab = event_card_full._switch_tab(tab_name="ДОПОЛНИТЕЛЬНО")

        event_responsibles = [{"NoData": "Данных не найдено"}]

        event_additional_data = event_card_tab._get_data()
        event_card_tab._fill_data(template=event['Additional'], save=False)
        event_card_tab._check_responsibles(template_list=event_additional_data['Responsibles'])
        event_card_tab._check_inputs(template=event_additional_data['Inputs'])

        event_card_tab._fill_data(template=event['Additional'], save=True)
        event_responsibles = event_card_tab._add_to_responsibles_list(current_list=event_responsibles,
                                                                      added_list=event['Additional']['Responsibles'])
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

        deleted = event['Additional']['Responsibles'][1]

        event_card_tab._delete_table_row(deleted=deleted, delete_confirm=False, save=True)
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

        event_card_tab._delete_table_row(deleted=deleted, delete_confirm=True, save=False)
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

        event_card_tab._delete_table_row(deleted=deleted, delete_confirm=True, save=True)
        event_responsibles = event_card_tab._delete_from_responsibles_list(current_list=event_responsibles,
                                                                           deleted=deleted)
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

        deleted = event['Additional']['Responsibles'][0]
        event_card_tab._delete_table_row(deleted=deleted, delete_confirm=True, save=True)
        event_responsibles = event_card_tab._delete_from_responsibles_list(current_list=event_responsibles,
                                                                           deleted=deleted)
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

        deleted = {"Organization": "Главная", "Position": "Директор", "FullName": "Боссов Босс"}
        event_card_tab._delete_table_row(deleted=deleted, delete_confirm=True, save=True)
        event_responsibles = event_card_tab._delete_from_responsibles_list(current_list=event_responsibles,
                                                                           deleted=deleted)
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

    finally:
        events_page._goto()._delete_card(key=event_card_key, confirm=True, into="events")


@pytest.mark.parametrize("area_key", ["electro"])
def test_experiment_files(run_test, area_key):
    events_page = EventsPage(driver=run_test)
    user_credentials = events_page._auth.get_credentials(user="autotest_01")
    events_page._smart_open(credentials=user_credentials)

    event_card_start = EventFormStart(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_event_{area_key}.json"
    event = event_card_start._prepare_data_from_template(filename=filename, area_key=area_key)
    event_card_key = None
    try:
        event_card_emergency_type = "Нет угрозы ЧС"
        event_card_key = event_card_start._fill_data(template=event['StartData'], save=True)
        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._open_event_by_key(key=event_card_key)

        event_card_full = EventFormFull(driver=run_test)
        event_card_tab = event_card_full._switch_tab(tab_name="ФАЙЛЫ")

        event_files = [{"NoData": "Данных не найдено"}]
        filename1 = f"{run_test.data_paths['uploads']}/autotest_upload_cat.jpeg"
        event_card_tab._upload_file(filename=filename1, save=False)
        event_card_tab._check_files_list(template_list=event_files)

        filename2 = f"{run_test.data_paths['uploads']}/autotest_upload_cat.jpeg"
        event_card_tab._upload_file(filename=filename2, save=True)
        event_files = event_card_tab._add_to_files_list(current_list=event_files, filename=filename2)
        event_card_full._refresh()._switch_tab(tab_name="ФАЙЛЫ")
        event_card_tab._check_files_list(template_list=event_files)

        source_info_full = event_card_tab._get_file_info(filename=filename2, full=True)
        event_card_tab._prepare_download(filename=filename2)._download_file(filename=filename2)
        target_info_full = event_card_tab._get_download_info(filename=filename2)
        assert source_info_full == target_info_full

        filename3 = f"{run_test.data_paths['uploads']}/autotest_upload_event.png"
        event_card_tab._upload_file(filename=filename3, save=True)
        event_files = event_card_tab._add_to_files_list(current_list=event_files, filename=filename3)
        event_card_full._refresh()._switch_tab(tab_name="ФАЙЛЫ")
        event_card_tab._check_files_list(template_list=event_files)

        source_info_full = event_card_tab._get_file_info(filename=filename3, full=True)
        event_card_tab._prepare_download(filename=filename3)._download_file(filename=filename3)
        target_info_full = event_card_tab._get_download_info(filename=filename3)
        assert source_info_full == target_info_full

        event_card_tab._delete_file(filename=filename2, save=False)
        event_card_tab._check_files_list(template_list=event_files)

        event_card_tab._delete_file(filename=filename3, save=True)
        event_files = event_card_tab._delete_from_files_list(current_list=event_files, filename=filename3)
        event_card_tab._check_files_list(template_list=event_files)

    finally:
        events_page._goto()._delete_card(key=event_card_key, confirm=True, into="events")


@pytest.mark.parametrize("area_key", ["electro"])
def test_experiment_emergency(run_test, area_key):
    events_page = EventsPage(driver=run_test)
    user_credentials = events_page._auth.get_credentials(user="autotest_01")
    events_page._smart_open(credentials=user_credentials)

    event_card_start = EventFormStart(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_event_{area_key}.json"
    event = event_card_start._prepare_data_from_template(filename=filename, area_key=area_key)
    event_card_key = None
    try:
        event_card_emergency_type = "Нет угрозы ЧС"
        event_card_key = event_card_start._fill_data(template=event['StartData'], save=True)
        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._open_event_by_key(key=event_card_key)

        event_card_full = EventFormFull(driver=run_test)
        event_card_tab = event_card_full._switch_tab(tab_name="ОГРАНИЧЕНИЯ")
        event_limitations = [{"NoData": "Данных не найдено"}]
        event_limitation_date_time = event_card_tab._fill_data(template=event['Limitations']['Full'],
                                                               limitation_save=True, save=True)
        event['Limitations']['Full']['DateTimeOnOff'] = event_limitation_date_time
        event_limitations = event_card_tab._add_to_list(current_list=event_limitations,
                                                        added=event['Limitations']['Full'])
        event_card_tab._check_data(template=event_limitations)
        event_card_full._check_attention_block(presence=True)
        event_card_full._check_tab_emergency(presence=True)

        event_card_tab = event_card_full._switch_tab(tab_name="УЧЁТ РЕЖИМА ЧС")
        event_data = event_card_tab._fill_data(template=event['Emergency'], save=False)
        print(f"\nEVENT_DATA_CANCEL = {event_data}\n")

        event_data = event_card_tab._fill_data(template=event['Emergency'], save=True)
        event_card_tab._press_keyboard_key(key="PAGE UP")
        time.sleep(5)
        print(f"\nEVENT_DATA_SAVE = {event_data}\n")

    finally:
        events_page._goto()._delete_card(key=event_card_key, confirm=True, into="events")


@pytest.mark.parametrize("area_key", ["electro"])
def test_experiment_agree(run_test, area_key):
    events_page = EventsPage(driver=run_test)
    user_credentials = events_page._auth.get_credentials(user="autotest_01")

    event_card_start = EventFormStart(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_event_{area_key}.json"
    event = event_card_start._prepare_data_from_template(filename=filename, area_key=area_key)
    event_card_key = None

    objects_page = ObjectsCommunalPage(driver=run_test)
    objects_page._smart_open(credentials=user_credentials)
    object_card = ObjectCommunalForm(driver=run_test)
    try:
        objects_page._open_card_by_key(key=event['Object']['Name'], into="objects_communal")
        object_data = object_card._get_data()

        events_page._goto()
        event_card_key = event_card_start._fill_data(template=event['StartData'], save=True)
        event['StartData']['Description'] = event_card_key
        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._open_event_by_key(key=event_card_key)

        event_card_full = EventFormFull(driver=run_test)
        event_card_tab = event_card_full._switch_tab(tab_name="ПЕРВИЧНЫЕ ДАННЫЕ")
        event_card_tab._check_data(template=event['StartData'])

        event_card_tab = event_card_full._switch_tab(tab_name="ХАРАКТЕРИСТИКИ")
        event_card_tab._fill_data(template=event['Properties'], save=True, duplicate_save=True)
        event_card_tab._check_data(template=event['Properties'])

        event_card_tab = event_card_full._switch_tab(tab_name="ОБЪЕКТ")
        event_card_tab._fill_data(template=event['Object'], save=True)
        event_card_tab._check_data(template=object_data)

        event_card_tab = event_card_full._switch_tab(tab_name="ОГРАНИЧЕНИЯ")
        event_limitations = [{"NoData": "Данных не найдено"}]
        event_limitation_date_time = event_card_tab._fill_data(template=event['Limitations']['Partial'],
                                                               limitation_save=True, save=True)
        event['Limitations']['Partial']['DateTimeOnOff'] = event_limitation_date_time
        event_limitations = event_card_tab._add_to_list(current_list=event_limitations,
                                                        added=event['Limitations']['Partial'])
        event_card_tab._check_data(template=event_limitations)

        event_card_tab = event_card_full._switch_tab(tab_name="ДОПОЛНИТЕЛЬНО")
        event_responsibles = [{"NoData": "Данных не найдено"}]
        event_card_tab._fill_data(template=event['Additional'], save=True)
        event_responsibles = event_card_tab._add_to_responsibles_list(current_list=event_responsibles,
                                                                      added_list=event['Additional']['Responsibles'])
        event_card_tab._check_responsibles(template_list=event_responsibles)
        event_card_tab._check_inputs(template=event['Additional']['Inputs'])

        event_card_tab = event_card_full._switch_tab(tab_name="СОГЛАСОВАНИЕ")
        event_agree_history = [{"NoData": "Данных не найдено"}]

        event_card_tab._send_to_responsible(responsible=event['Agree']['Approve'], action="На согласование")
        event_agree_history = event_card_tab._add_to_list(current_list=event_agree_history,
                                                          added=event['Agree']['Approve']['History']['Wait'])
        event_card_tab._check_history(template_list=event_agree_history)

        approve_credentials = events_page._auth.get_credentials(user=event['Agree']['Approve']['Username'])
        events_page._smart_open(credentials=approve_credentials)

        keys = f"{event_card_key}; Новая карточка на согласование!"
        event_notes_new, event_notes_read = events_page._notif._get_notes_by_keys(keys=keys, max_notes=10)
        assert len(event_notes_new) == len(event_notes_read) == 1

        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._check_event_agree_status(key=event_card_key, agree_status="Ожидает согласования", open_event=True)
        event_card_tab = event_card_full._switch_tab(tab_name="СОГЛАСОВАНИЕ")
        event_card_tab._accept_event(action="Согласовать")
        event_agree_history = event_card_tab._add_to_list(current_list=event_agree_history,
                                                          added=event['Agree']['Approve']['History']['Accepted'])
        event_card_tab._check_history(template_list=event_agree_history)

        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._check_event_agree_status(key=event_card_key, agree_status="Согласовано", open_event=True)
        event_card_tab = event_card_full._switch_tab(tab_name="СОГЛАСОВАНИЕ")
        event_card_tab._send_to_responsible(responsible=event['Agree']['Confirm'], action="На утверждение")
        event_agree_history = event_card_tab._add_to_list(current_list=event_agree_history,
                                                          added=event['Agree']['Confirm']['History']['Wait'])
        event_card_tab._check_history(template_list=event_agree_history)

        confirm_credentials = events_page._auth.get_credentials(user=event['Agree']['Confirm']['Username'])
        events_page._smart_open(credentials=confirm_credentials)

        keys = f"{event_card_key}; Новая карточка на утверждение!"
        event_notes_new, event_notes_read = events_page._notif._get_notes_by_keys(keys=keys, max_notes=10)
        assert len(event_notes_new) == len(event_notes_read) == 1

        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._check_event_agree_status(key=event_card_key, agree_status="Ожидание утверждения", open_event=True)
        event_card_tab = event_card_full._switch_tab(tab_name="СОГЛАСОВАНИЕ")
        event_card_tab._accept_event(action="Утвердить", gkh_send_checkbox=False)
        event_agree_history = event_card_tab._add_to_list(current_list=event_agree_history,
                                                          added=event['Agree']['Confirm']['History']['Accepted'])
        event_card_tab._check_history(template_list=event_agree_history)

        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._check_event_agree_status(key=event_card_key, agree_status="Утверждено")

        events_page._smart_open(credentials=approve_credentials)
        keys = f"{event_card_key}; утверждена"
        event_notes_new, event_notes_read = events_page._notif._get_notes_by_keys(keys=keys, max_notes=10)
        assert len(event_notes_new) == len(event_notes_read) == 1

        events_page._smart_open(credentials=user_credentials)
        keys = f"{event_card_key}; согласована"
        event_notes_new, event_notes_read = events_page._notif._get_notes_by_keys(keys=keys, max_notes=10)
        assert len(event_notes_new) == len(event_notes_read) == 1

        user_credentials = events_page._auth.get_credentials(user="autotest_02")
        events_page._smart_open(credentials=user_credentials)

        keys = f"{event_card_key}; Создана карточка события"
        event_notes_new, event_notes_read = events_page._notif._get_notes_by_keys(keys=keys, max_notes=10,
                                                                                  close_panel=False)
        assert len(event_notes_new) == len(event_notes_read) == 1

        keys = f"{event_card_key}; Изменена карточка события"
        event_notes_new, event_notes_read = events_page._notif._get_notes_by_keys(keys=keys, max_notes=10,
                                                                                  close_panel=False)
        assert len(event_notes_new) == len(event_notes_read) == 4

        keys = f"{event_card_key}; введено Частичное ограничение"
        event_notes_new, event_notes_read = events_page._notif._get_notes_by_keys(keys=keys, max_notes=10)
        assert len(event_notes_new) == len(event_notes_read) == 1

    finally:
        events_page._goto()._delete_card(key=event_card_key, confirm=True, into="events")


@pytest.mark.parametrize("area_key", ["electro"])
def test_experiment_properties(run_test, area_key):
    events_page = EventsPage(driver=run_test)
    user_credentials = events_page._auth.get_credentials(user="autotest_01")
    events_page._smart_open(credentials=user_credentials)

    event_card_start = EventFormStart(driver=run_test)
    filename = f"{run_test.data_paths['templates']}/template_event_{area_key}.json"
    event = event_card_start._prepare_data_from_template(filename=filename, area_key=area_key)
    event_card_key = None
    try:
        event_card_key = event_card_start._fill_data(template=event['StartData'], save=True)

        events_page._goto()._switch_sort(sort_type="Дата и время возникновения события (по убыванию)")
        events_page._open_event_by_key(key=event_card_key)

        event_card_full = EventFormFull(driver=run_test)

        event_card_tab = event_card_full._switch_tab(tab_name="ХАРАКТЕРИСТИКИ")

        event_properties = event_card_tab._get_data()
        event_card_tab._fill_data(template=event['Properties'], save=False)
        event_card_tab._check_data(template=event_properties)

        event_card_tab._fill_data(template=event['Properties'], save=True, duplicate_save=True)
        event_card_tab._check_data(template=event['Properties'])

    finally:
        events_page._goto()._delete_card(key=event_card_key, confirm=True, into="events")
