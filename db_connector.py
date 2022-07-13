
from concurrent.futures import process
from ensurepip import version
from multiprocessing.dummy import Process
from optparse import Option
from tkinter.tix import INTEGER
from pony.orm import *
from datetime import datetime
from uuid import uuid4
import env
import os

DB = Database()
def setup_db():
    if not os.path.isdir("database"):
        os.mkdir("database")
    if env.DB["provider"] == "postgres":
        DB.bind(**env.DB)
    else:
        DB.bind(provider="sqlite", filename="database/database.sqlite", create_db=True)
    DB.generate_mapping(create_tables=True)
    set_sql_debug(True)

class Event(DB.Entity):
    model_name = Required(str)
    instance_id = Required(str)
    activity_id = Required(str)
    timestamp = Required(datetime, precision=6)
    pending = Required(StrArray)
    activity_variables = Required(Json)

class RunningInstance(DB.Entity):
    running = Required(bool)
    instance_id = Required(str, unique=True)

class Services(DB.Entity):
    name = Required(str)
    type = Required(str) #connector?
    url = Required(str)

class Process_Definition(DB.Entity):
    process_definition_id = PrimaryKey(int, auto=True)
    process_definition_key = Required(str)
    process_definition_name = Required(str)
    file_name = Optional(str, nullable=True)
    created = Required(datetime, precision=6)
    last_modified_date = Required(datetime, precision=6)
    xml_definition = Required(str)
    is_active = Required(bool)
    active_version_id = Optional(int, nullable=True)
    active_version_number = Optional(int, nullable=True)
    active_version_name = Optional(str, nullable=True)
    versions = Optional(StrArray, nullable=True)
    number_of_versions = Required(int)
    process_version = Set(lambda: Process_Version)

@db_session(sql_debug=True)
def delete_process_definition():
    pass

#Versions must be shown on the activation dialog
@db_session(sql_debug=True)
def activate_process_definition(process_id, version_id):
    process_definition = Process_Definition.get_for_update(lambda pd: pd.process_definition_id == process_id)
    if not version_id:
        version_id = process_definition.versions[-1]
    process_version = Process_Version.get_for_update(lambda pv: pv.process_version_id == version_id)
    process_definition.is_active = True
    
    process_definition.last_modified_date = datetime.now()
    process_definition.active_version_id = process_version.process_version_id
    process_definition.active_version_name = process_version.process_version_name
    process_definition.active_version_number = process_version.process_version_number
    
    process_version.is_active = True
    process_version.last_modified_date = process_definition.last_modified_date

    return process_definition.to_dict()

@db_session(sql_debug=True)
def deactivate_process_definition(id):
    process_definition = Process_Definition.get_for_update(lambda pd: pd.process_definition_id == id)
    if not process_definition:
        return None

    process_definition.is_active = False
    process_definition.active_version_id = None
    process_definition.active_version_name = None
    process_definition.active_version_number = None
    process_definition.last_modified_date = datetime.now()

    versions_ids = process_definition.versions
    if versions_ids:
        process_versions = []
        for version_id in versions_ids:
            process_version = Process_Version.get_for_update(lambda pv: pv.process_version_id == version_id)
            if process_version is not None:
                process_versions.append(process_version)

        if process_versions:
            for version in process_versions:
                if version.is_active:
                    version.is_active = False
                    version.last_modified_date = datetime.now()

    return process_definition.to_dict()

@db_session(sql_debug=True)
def get_process_definitions():
    process_definitions = select(pd for pd in Process_Definition)[:].to_list()
    if not process_definitions:
        return {}
    transformed_process_definitions = [process.to_dict() for process in process_definitions]
    return transformed_process_definitions

@db_session(sql_debug=True)
def get_process_definition_by_id(id):
    process_definition = Process_Definition.get(lambda pd: pd.process_definition_id == id)
    return {} if process_definition is None else process_definition.to_dict()

@db_session(sql_debug=True)
def get_process_definition_by_key(key):
    process_definition = Process_Definition.get(lambda pd: pd.process_definition_key == key)
    return {} if process_definition is None else process_definition.to_dict()

@db_session(sql_debug=True)
def add_process_definition(payload):
    process_definition = Process_Definition(
        process_definition_key = str(uuid4()),
        process_definition_name = payload.get('process_name'),
        file_name = payload.get('file_name'),
        created = datetime.now(),
        last_modified_date = datetime.now(),
        xml_definition = payload.get('xml_definition'),
        is_active = payload.get('is_active'),
        active_version_id = None,
        active_version_name = None,
        active_version_number = None,
        versions = None,
        number_of_versions = 1,
    )
    process_definition.flush()

    process_version = Process_Version(
        process_version_key = str(uuid4()),
        process_version_name = payload.get('process_name') + ' v1',
        process_version_number = 1,
        file_name = payload.get('file_name'),
        created = process_definition.created,
        last_modified_date = process_definition.created,
        xml_definition = payload.get('xml_definition'),
        is_active = payload.get('is_active'),
        process_definition_id = process_definition
    )
    process_version.flush()

    if payload.get('is_active'):
        process_definition.active_version_id = process_version.process_version_id
        process_definition.active_version_name = process_version.process_version_name
        process_definition.active_version_number = process_version.process_version_number
        process_definition.versions = [process_version.process_version_id]
        process_definition.process_version = process_version

    return process_definition.to_dict()

class Process_Version(DB.Entity):
    process_version_id = PrimaryKey(int, auto=True)
    process_version_key = Required(str)
    process_version_name = Required(str)
    process_version_number = Optional(int)
    file_name = Optional(str)
    created = Required(datetime, precision=6)
    last_modified_date = Required(datetime, precision=6)
    xml_definition = Required(str)
    is_active = Required(bool)
    process_definition_id = Optional(Process_Definition) #FK
    process_instance = Set(lambda: Process_Instance)
    #Move tasks here? -check engine parsing

@db_session(sql_debug=True)
def add_process_version(payload):
    process_definition_id = payload.get('process_definition_id')
    process_definition = Process_Definition.get(lambda pd: pd.process_definition_id == process_definition_id)
    last_process_version = process_definition.number_of_versions

    process_version = Process_Version(
        process_version_key = str(uuid4()),
        process_version_name = payload.get('process_name'),
        process_version_number = last_process_version + 1,
        file_name = payload.get('file_name'),
        created = datetime.now(),
        last_modified_date = datetime.now(),
        xml_definition = payload.get('xml_definition'),
        is_active = payload.get('is_active'),
        process_definition_id = process_definition
    )
    process_version.flush()

    if payload.get('is_active'):
        process_definition.is_active = True
        process_definition.active_version_name = process_version.process_version_name
        process_definition.active_version_number = process_version.process_version_number

    process_definition.versions.append(process_version.process_version_id)
    process_definition.number_of_versions += 1
    process_definition.last_modified_date = process_version.last_modified_date

    return process_definition.to_dict()

@db_session(sql_debug=True)
def get_process_versions(id):
    process_versions = select(process for process in Process_Version if process.process_definition_id.process_definition_id == id)[:]
    if not process_versions:
        return []
    transformed_process_versions = [process.to_dict() for process in process_versions]
    return transformed_process_versions

@db_session(sql_debug=True)
def activate_process_version(process_id, version_id):
    process_definition = Process_Definition.get_for_update(lambda pd: pd.process_definition_id == process_id)
    if not process_definition:
        return None

    process_versions_ids = process_definition.versions
    for process_version_id in process_versions_ids:
        version = Process_Version.get_for_update(lambda pv: pv.process_version_id == process_version_id)
        if version.process_version_id != version_id and version.is_active == True:
            version.is_active = False
            version.last_modified_date = datetime.now()
        elif version.process_version_id == version_id:
            process_definition.is_active = True
            process_definition.active_version_id = version.process_version_id
            process_definition.active_version_name = version.process_version_name
            process_definition.active_version_number = version.process_version_number
            process_definition.last_modified_date = datetime.now()
            version.is_active = True
            version.last_modified_date = datetime.now()
            process_version = version

    return {
        "process_definition": process_definition.to_dict(),
        "process_version": process_version.to_dict()
    }

@db_session(sql_debug=True)
def deactivate_process_version(process_id, version_id):
    process_definition = Process_Definition.get_for_update(lambda pd: pd.process_definition_id == process_id)
    if not process_definition:
        return None
    process_version = Process_Version.get_for_update(lambda pv: pv.process_version_id == version_id)
    if not process_version:
        return None

    process_definition.is_active = False
    process_definition.active_version_id = None
    process_definition.active_version_name = None
    process_definition.active_version_number = None
    process_definition.last_modified_date = datetime.now()
    process_version.is_active = False
    process_version.last_modified_date = datetime.now()

    # process_versions_ids = process_definition.versions
    # for process_version_id in process_versions_ids:
    #     process_version = Process_Version.get_for_update(lambda pv: pv.process_version_id == process_version_id)
    #     if process_version.is_active == True and not (process_version.process_version_id == version_id):
    #         process_version.is_active = False
    #         process_version.last_modified_date = datetime.now()
            
    return {
        "process_definition": process_definition.to_dict(),
        "process_version": process_version.to_dict()
    }    

@db_session(sql_debug=True)
def delete_process_version():
    #RULES: cannot delete if the version is the only one left
    #Check if the version is active in some process, if it is deactivate the process - frontend needs to know
    pass

class Process_Instance(DB.Entity):
    process_instance_id = PrimaryKey(int, auto=True)
    process_instance_key = Required(str)
    created = Required(datetime, precision=6)
    last_modified_date = Required(datetime, precision=6)
    process_instance_status = Required(str) #CHECK CONSTRAINT (FINISHED, ERROR, STARTED, SUSPENDED)
    task_ids = Optional(IntArray, nullable=True)
    process_instance_variables = Optional(Json, nullable=True)
    process_version_id = Required(Process_Version) #FK

class Task(DB.Entity):
    task_id = PrimaryKey(int, auto=True)
    task_name = Required(str)
    task_type = Required(str)
    created = Required(datetime, precision=6)
    last_modified_date = Required(datetime, precision=6)
    task_variables = Optional(Json, nullable=True)
    process_instance_id = Required(int) #FK






@db_session
def get_services():
    services = select(s for s in Services)[:]
    services_list = list(services)
    return services_list

@db_session
def add_services(name, type, url):
    Services(name=name, type=type, url=url)
    return f'Service with the {name} name was saved.'

@db_session
def update_services(id, name, type, url):
    service_to_update = Services[id]
    service_name = service_to_update.name
    service_to_update.set(name=name, type=type, url=url)
    return f'Service with the {service_name} name was updated.'

@db_session
def delete_services(id, name):
    service_to_delete = Services[id] 
    service_to_delete.delete()
    return f'Service with the {name} name was deleted.'

@db_session
def add_event(model_name, instance_id, activity_id, timestamp, pending, activity_variables):
    Event(
        model_name=model_name,
        instance_id=instance_id,
        activity_id=activity_id,
        timestamp=timestamp,
        pending=pending,
        activity_variables=activity_variables,
    )

@db_session
def add_running_instance(instance_id):
    RunningInstance(instance_id=instance_id, running=True)

@db_session
def finish_running_instance(instance):
    finished_instance = RunningInstance.get(instance_id=instance)
    finished_instance.running = False

@db_session
def get_running_instances_log():
    log = []
    running_instances = RunningInstance.select(lambda ri: ri.running == True)[:]
    for instance in running_instances:
        instance_dict = {}
        instance_dict[instance.instance_id] = {}
        events = Event.select(lambda e: e.instance_id == instance.instance_id).order_by(
            Event.timestamp
        )[:]
        events_list = []
        for event in events:
            model_path = event.model_name
            event_dict = {}
            event_dict["activity_id"] = event.activity_id
            event_dict["pending"] = event.pending
            event_dict["activity_variables"] = event.activity_variables
            events_list.append(event_dict)

        instance_dict[instance.instance_id]["model_path"] = model_path
        instance_dict[instance.instance_id]["events"] = events_list
        log.append(instance_dict)

    return log
