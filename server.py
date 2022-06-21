from http.client import responses
import json
from logging import debug
from pickle import FALSE
from tkinter.tix import Tree
import traceback
from turtle import width
from typing import OrderedDict
from webbrowser import get
import aiohttp
import os
from aiohttp import ClientConnectionError, ClientSession, web
from uuid import uuid4
import asyncio
from utils.functions import *
from requests import session
from bpmn_model import BpmnModel, UserFormMessage, get_model_for_instance
import aiohttp_cors
import db_connector
from functools import reduce

# Setup database
db_connector.setup_db()
routes = web.RouteTableDef()
session = aiohttp.ClientSession()

# uuid4 = lambda: 2  # hardcoded for easy testing

models = {}
for file in os.listdir("models"):
    if file.endswith(".bpmn"):
        m = BpmnModel(file)
        models[file] = m

async def fetch(session, url):
    try:
        async with session.get(url + '/status') as response:
            print(response)
            status = True if response.status == 200 else False
    except ClientConnectionError as e:
        #print(str(e))
        status = False
    except aiohttp.InvalidURL as e:
        #InvalidURL is not JSON serializable
        status = False
    return status        


async def run_as_server(app):
    app["bpmn_models"] = models
    log = db_connector.get_running_instances_log()
    for l in log:
        for key, data in l.items():
            if data["model_path"] in app["bpmn_models"]:
                instance = await app["bpmn_models"][data["model_path"]].create_instance(
                    key, {}
                )
                instance = await instance.run_from_log(data["events"])
                asyncio.create_task(instance.run())

#TODO - refactor, too long
@routes.post("/service")
async def add_services(request):
    payload = await request.json()
    new_data = payload['new']
    old_data = payload['old']
    insert_list = []
    delete_list = []
    update_list = []

    #base cases
    if not new_data and not old_data:
        return web.json_response({"status": 400, "message": ["No data was sent."]})
    if not new_data and old_data:
        delete_list.extend(old_data)
    if new_data and not old_data:
        insert_list.extend(new_data)

    #ids_lst = [x for x in new_data if x.get('id') is None] #obsolete?
    update_list = [item for item in new_data if item.get('changed') is True]

    #strip excess properties so new_data can be comapared with old_data
    for item in new_data:
        item.pop('changed', None)
        item.pop('color', None)
        item.pop('disabled', None)

    new = json.dumps(new_data, sort_keys=True)
    old = json.dumps(old_data, sort_keys=True)  
    if new == old:
        return web.json_response({"status": 400, "message": ["Nothing to do."]})

    if not insert_list:
        insert_list = [new_item for new_item in new_data if not find(new_item, old_data) and not find(new_item, insert_list)]
    if not delete_list:
        delete_list = [old_item for old_item in old_data if not find(old_item, new_data) and not find(old_item, delete_list)]

    feedback_messages = []

    for insert_item in insert_list:
        msg = db_connector.add_services(insert_item['name'], insert_item['type'], insert_item['url'])
        feedback_messages.append(msg)
    for update_item in update_list:
        msg = db_connector.update_services(update_item['id'], update_item['name'], update_item['type'], update_item['url'])
        feedback_messages.append(msg)
    for delete_item in delete_list:
        msg = db_connector.delete_services(delete_item['id'], delete_item['name'])
        feedback_messages.append(msg)
    return web.json_response({"status": 200, "message": feedback_messages})

@routes.get("/service")
async def get_services(request):
    services = db_connector.get_services()
    result = [service.to_dict() for service in services]
    return web.json_response(result)

@routes.get("/service/meta/{url}")
async def get_service_route(request):
    url = request.match_info.get('url')
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url + '/meta') as response:
                routes = await response.json()
                print(routes)
        except ClientConnectionError as e:
            routes = []
            print(e)
        except aiohttp.InvalidURL as e:
            routes = []
            print(e)
    return web.json_response(routes)

@routes.get("/service/status")
async def get_service_status(request):
    services = db_connector.get_services()
    services_hp, service_names = [], []
    async with aiohttp.ClientSession() as session:
        for service in services:
            service_names.append(service.name)
            services_hp.append(fetch(session, service.url))
        service_statuses = await asyncio.gather(*services_hp, return_exceptions=True)
        print(service_statuses)
    return web.json_response(dict(zip(service_names, service_statuses)))

@routes.get("/model")
async def get_models(request):
    data = [m.to_json() for m in models.values()]
    return web.json_response({
            "status": "ok", 
            "results": data
        })

@routes.get("/model/{model_name}")
async def get_model(request):
    model_name = request.match_info.get("model_name")
    return web.FileResponse(
        path=os.path.join("models", app["bpmn_models"][model_name].model_path)
    )

@routes.post("/model/{model_name}/instance")
async def handle_new_instance(request):
    _id = str(uuid4())
    model = request.match_info.get("model_name")
    instance = await app["bpmn_models"][model].create_instance(_id, {})
    asyncio.create_task(instance.run())
    return web.json_response({"id": _id})


@routes.post("/instance/{instance_id}/task/{task_id}/form")
async def handle_form(request):
    post = await request.json()
    instance_id = request.match_info.get("instance_id")
    task_id = request.match_info.get("task_id")
    m = get_model_for_instance(instance_id)
    m.instances[instance_id].in_queue.put_nowait(UserFormMessage(task_id, post))

    return web.json_response({"status": "OK"})


@routes.get("/instance")
async def search_instance(request):
    params = request.rel_url.query
    queries = []
    try:
        strip_lower = lambda x: x.strip().lower()
        check_colon = lambda x: x if ":" in x else f":{x}"

        queries = list(
            tuple(
                map(
                    strip_lower,
                    check_colon(q).split(":"),
                )
            )
            for q in params["q"].split(",")
        )
    except:
        return web.json_response({"error": "invalid_query"}, status=400)

    result_ids = []
    for (att, value) in queries:
        ids = []
        for m in models.values():
            for _id, instance in m.instances.items():
                search_atts = []
                if not att:
                    search_atts = list(instance.variables.keys())
                else:
                    for key in instance.variables.keys():
                        if not att or att in key.lower():
                            search_atts.append(key)
                search_atts = filter(
                    lambda x: isinstance(instance.variables[x], str), search_atts
                )

                for search_att in search_atts:
                    if search_att and value in instance.variables[search_att].lower():
                        # data.append(instance.to_json())
                        ids.append(_id)
        result_ids.append(set(ids))

    ids = reduce(lambda a, x: a.intersection(x), result_ids[:-1], result_ids[0])

    data = []
    for _id in ids:
        data.append(get_model_for_instance(_id).instances[_id].to_json())

    return web.json_response({"status": "ok", "results": data})


@routes.get("/instance/{instance_id}/task/{task_id}")
async def handle_task_info(request):
    instance_id = request.match_info.get("instance_id")
    task_id = request.match_info.get("task_id")
    m = get_model_for_instance(instance_id)
    if not m:
        raise aiohttp.web.HTTPNotFound
    instance = m.instances[instance_id]
    task = instance.model.elements[task_id]

    return web.json_response(task.get_info())


@routes.get("/instance/{instance_id}")
async def handle_instance_info(request):
    instance_id = request.match_info.get("instance_id")
    m = get_model_for_instance(instance_id)
    if not m:
        raise aiohttp.web.HTTPNotFound
    instance = m.instances[instance_id].to_json()

    return web.json_response(instance)


app = None


def run():
    global app
    app = web.Application()
    app.on_startup.append(run_as_server)
    app.add_routes(routes)

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*",
            )
        },
    )

    for route in list(app.router.routes()):
        cors.add(route)

    return app


async def serve():
    return run()


if __name__ == "__main__":
    app = run()
    web.run_app(app, port=9000)
