from enum import unique
from urllib import response
from pony.orm import *
from datetime import datetime
import env
import os

DB = Database()

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

def setup_db():
    if not os.path.isdir("database"):
        os.mkdir("database")
    if env.DB["provider"] == "postgres":
        DB.bind(**env.DB)
    else:
        DB.bind(provider="sqlite", filename="database/database.sqlite", create_db=True)
    DB.generate_mapping(create_tables=True)
    set_sql_debug(True)


###############
### Services ##
###############

#TODO: add exception handling
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
def add_event(
    model_name, instance_id, activity_id, timestamp, pending, activity_variables
):
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
