
from ast import Param
from concurrent.futures import process
from ensurepip import version
from enum import auto
from fileinput import filename
from multiprocessing.dummy import Process
from optparse import Option
from tkinter.tix import INTEGER
from venv import create
from aiohttp import payload
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


class ProcessDefinition(DB.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    filename = Required(str)
    xml = Required(str)
    is_active = Required(bool)
    created = Required(datetime, precision=6)
    last_modified_date = Required(datetime, precision=6)
    number_of_versions = Required(int)
    active_version_id = Optional(int, nullable=True)
    active_version_number = Optional(int, nullable=True)
    active_version_name = Optional(str, nullable=True)
    versions = Optional(IntArray, nullable=True)
    process_version = Set(lambda: ProcessVersion)

class ProcessVersion(DB.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    number = Required(int)
    filename = Required(str)
    xml = Required(str)
    is_active = Required(bool)
    created = Required(datetime, precision=6)
    last_modified_date = Required(datetime, precision=6)
    definition = Required(ProcessDefinition) #FK

@db_session(sql_debug=True)
def delete_process_definition(definition_id):
    definition = ProcessDefinition.get(lambda pd: pd.id == definition_id)
    versions_ids = definition.versions
    for version_id in versions_ids:
        process_version = ProcessVersion.get(lambda pv: pv.id == version_id)
        process_version.delete()
    definition.delete()
    return {
        "process_definition": definition_id
    }

@db_session(sql_debug=True)
def activate_process_definition(definition_id, version_id):
    process_definition = ProcessDefinition.get_for_update(lambda pd: pd.id == definition_id)
    if not version_id:
        version_id = process_definition.versions[-1]
    process_version = ProcessVersion.get_for_update(lambda pv: pv.id == version_id)
    process_definition.is_active = True
    process_definition.last_modified_date = datetime.now()
    process_definition.active_version_id = process_version.id
    process_definition.active_version_name = process_version.name
    process_definition.active_version_number = process_version.number
    
    process_version.is_active = True
    process_version.last_modified_date = process_definition.last_modified_date

    return process_definition.to_dict()

@db_session(sql_debug=True)
def deactivate_process_definition(definition_id):
    process_definition = ProcessDefinition.get_for_update(lambda pd: pd.id == definition_id)
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
            process_version = ProcessVersion.get_for_update(lambda pv: pv.id == version_id)
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
    process_definitions = select(pd for pd in ProcessDefinition)[:].to_list()
    if not process_definitions:
        return []
    transformed_process_definitions = [process.to_dict() for process in process_definitions]
    return transformed_process_definitions

@db_session(sql_debug=True)
def get_process_definition(definition_id):
    process_definition = ProcessDefinition.get(lambda pd: pd.id == definition_id)
    return {} if process_definition is None else process_definition.to_dict()

@db_session(sql_debug=True)
def add_process_definition(payload):
    process_definition = ProcessDefinition(
        name = payload.get('name'),
        filename = payload.get('filename'),
        created = datetime.now(),
        last_modified_date = datetime.now(),
        xml = payload.get('xml'),
        is_active = payload.get('is_active'),
        active_version_id = None,
        active_version_name = None,
        active_version_number = None,
        versions = None,
        number_of_versions = 1,
    )
    process_definition.flush()

    process_version = ProcessVersion(
        name = payload.get('name') + ' v1',
        number = 1,
        filename = payload.get('filename'),
        created = process_definition.created,
        last_modified_date = process_definition.created,
        xml = payload.get('xml'),
        is_active = payload.get('is_active'),
        definition = process_definition
    )
    process_version.flush()

    if payload.get('is_active'):
        process_definition.active_version_id = process_version.id
        process_definition.active_version_name = process_version.name
        process_definition.active_version_number = process_version.number
        process_definition.process_version = process_version
    process_definition.versions = [process_version.id]

    return process_definition.to_dict()

@db_session(sql_debug=True)
def change_process_definition_info(definition_id, definition_name, definition_filename):
    definition = ProcessDefinition.get_for_update(lambda pd: pd.id == definition_id)
    definition.name = definition_name
    definition.filename = definition_filename
    definition.last_modified_date = datetime.now()
    
    return definition.to_dict()

@db_session(sql_debug=True)
def add_process_version(payload):
    id = payload.get('id')
    process_definition = ProcessDefinition.get(lambda pd: pd.id == id)
    last_process_version = process_definition.number_of_versions
    process_version = ProcessVersion(
        name = payload.get('name'),
        number = last_process_version + 1,
        filename = payload.get('filename'),
        created = datetime.now(),
        last_modified_date = datetime.now(),
        xml = payload.get('xml'),
        is_active = payload.get('is_active'),
        definition = process_definition
    )
    process_version.flush()
    if payload.get('is_active'):
        process_definition.is_active = True
        process_definition.active_version_name = process_version.name
        process_definition.active_version_number = process_version.number

    process_definition.versions.append(process_version.id)
    process_definition.number_of_versions += 1
    process_definition.last_modified_date = process_version.last_modified_date

    return process_definition.to_dict()

@db_session(sql_debug=True)
def get_process_versions(version_id):
    process_versions = select(process for process in ProcessVersion if process.definition.id == version_id)[:]
    if not process_versions:
        return []
    transformed_process_versions = [process.to_dict() for process in process_versions]
    return transformed_process_versions

@db_session(sql_debug=True)
def activate_process_version(definition_id, version_id):
    process_definition = ProcessDefinition.get_for_update(lambda pd: pd.id == definition_id)
    if not process_definition:
        return None

    process_versions_ids = process_definition.versions
    process_versions = []
    for process_version_id in process_versions_ids:
        version = ProcessVersion.get_for_update(lambda pv: pv.id == process_version_id)
        if version.id != version_id and version.is_active == True:
            version.is_active = False
            version.last_modified_date = datetime.now()
        elif version.id == version_id:
            process_definition.is_active = True
            process_definition.active_version_id = version.id
            process_definition.active_version_name = version.name
            process_definition.active_version_number = version.number
            process_definition.last_modified_date = datetime.now()
            version.is_active = True
            version.last_modified_date = datetime.now()
        process_versions.append(version.to_dict())

    return {
        "process_definition": process_definition.to_dict(),
        "process_version": process_versions
    }

@db_session(sql_debug=True)
def deactivate_process_version(definition_id, version_id):
    process_definition = ProcessDefinition.get_for_update(lambda pd: pd.id == definition_id)
    if not process_definition:
        return None
    process_version = ProcessVersion.get_for_update(lambda pv: pv.id == version_id)
    if not process_version:
        return None

    process_definition.is_active = False
    process_definition.active_version_id = None
    process_definition.active_version_name = None
    process_definition.active_version_number = None
    process_definition.last_modified_date = datetime.now()
    process_version.is_active = False
    process_version.last_modified_date = datetime.now()

    return {
        "process_definition": process_definition.to_dict(),
        "process_version": process_version.to_dict()
    }    

@db_session(sql_debug=True)
def change_process_version_info(version_id, version_name, version_filename):
    version = ProcessVersion.get_for_update(lambda pv: pv.id == version_id)
    definition = None
    if version.is_active == True:
        definition = version.process_definition
        definition = ProcessDefinition.get_for_update(lambda pd: pd.id == definition.id)
        definition.active_version_name = version_name
        definition.last_modified_date = datetime.now()
        definition = definition.to_dict()

    version.name = version_name
    version.filename = version_filename
    version.last_modified_date = datetime.now()
    
    return {
        "process_definition": definition,
        "process_version": version.to_dict()
    }

@db_session(sql_debug=True)
def get_process_version(version_id):
    version = ProcessVersion.get(lambda pv: pv.id == version_id)
    return {} if version is None else version.to_dict()

@db_session(sql_debug=True)
def delete_process_version(version_id):
    version = ProcessVersion.get(lambda pv: pv.id == version_id)
    definition = ProcessDefinition.get(lambda pd: pd.id == version.definition.id)
    definition_id = definition.id
    if definition.number_of_versions == 1:
        version.delete()
        definition.delete()
        return {
            "process_definition": definition_id,
            "process_version": version_id
        }
    elif version.is_active:
        definition.is_active = False
        definition.number_of_versions -= 1
        definition.versions.remove(version_id)
        definition.active_version_id = None
        definition.active_version_name = None
        definition.active_version_number = None
        definition.last_modified_date = datetime.now()
        version.delete()
        return {
            "process_definition": definition.to_dict(),
            "process_version": version_id
        }
    else:
        definition.number_of_versions -= 1
        definition.versions.remove(version_id)
        definition.last_modified_date = datetime.now()
        version.delete()
    
    return {
        "process_definition": None,
        "process_version": version_id
    }

class Web_Service(DB.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    address = Required(str)
    is_active = Required(bool)
    created = Required(datetime, precision=6)
    last_modified_date = Required(datetime, precision=6)

@db_session
def get_service(id):
    service = Web_Service.get(lambda s: s.id == id)
    if not service:
        return {}
    return service.to_dict()

@db_session
def get_services():
    services = select(service for service in Web_Service)[:]
    if not services:
        return []
    services = [service.to_dict() for service in services]
    return services

@db_session
def delete_service(id):
    service = Web_Service.get(lambda s: s.id == id)
    if not service:
        return {}
    service.delete()
    return { "id": id}

@db_session
def add_service(payload):
    service = Web_Service(
        name = payload.get('name'),
        address = payload.get('address'),
        is_active = payload.get('is_active'),
        created = datetime.now(),
        last_modified_date = datetime.now()
    )
    service.flush()
    return service.to_dict()

@db_session
def change_status(id):
    service = Web_Service.get_for_update(lambda s: s.id == id)
    if not service:
        return {}
    service.is_active = not service.is_active
    return service.to_dict()

@db_session
def update_service(data):
    service = Web_Service.get_for_update(lambda s: s.id == data.get('id'))
    if not service:
        return {}
    service.name = data.get('name')
    service.address = data.get('address')
    service.last_modified_date = datetime.now()
    return service.to_dict()

