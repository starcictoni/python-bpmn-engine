
from http.client import HTTPException
from symbol import parameters
from aiohttp import web
from uuid import uuid4, UUID
from datetime import datetime
import aiohttp
from pkg_resources import empty_provider
from pony.orm import *
import xml.etree.ElementTree as ET
import utils.common as utils
import env, os, asyncio, json
import db_connector
import logging
import traceback
import aiohttp_cors
from functools import reduce
from bpmn_model import BpmnModel, UserFormMessage, get_model_for_instance

db_connector.setup_db()


class ProcessDefinition:
    def __init__(self):
        pass

    def get_process_definitions(self, request):
        try: 
            response = db_connector.get_process_definitions()
            if not response:
                return web.json_response(status=400, data=[])
            data = json.dumps(response, sort_keys=True, default=str)
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data=[])
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data=[])
        else:
            return web.json_response(status=200, data=data)

    def get_process_definition(self, request):
        try:
            definition_id = request.match_info.get('id')
            if not definition_id or (not utils.is_valid_type_id(definition_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.get_process_definition(definition_id)
            if not response:
                return web.json_response(status=400, data={})
            data = json.dumps(response, sort_keys=True, default=str)
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)
    
    async def add_process_definition(self, request):
        try:
            payload = await request.json()
            if not payload:
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.add_process_definition(payload)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=201, data=data)

    async def activate_process_definition(self, request):
        try:
            payload = await request.json()
            definition_id = payload.get('definition_id')
            version_id = payload.get('version_id')
            if not definition_id or (not utils.is_valid_type_id(definition_id)) or (
                not utils.is_valid_optional_id(version_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.activate_process_definition(definition_id, version_id)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def deactivate_process_definition(self, request):
        try:
            payload = await request.json()
            id = payload.get('id')
            if not id or (not utils.is_valid_type_id(id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.deactivate_process_definition(id)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def change_process_definition_info(self, request):
        try:
            payload = await request.json()
            id = payload.get('id')
            name = payload.get('name')
            filename = payload.get('filename')
            if not id:
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.change_process_definition_info(id, name, filename)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def delete_process_definition(self, request):
        try:
            payload = await request.json()
            id = payload.get('id')
            if not id or (not utils.is_valid_type_id(id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.delete_process_definition(id)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

class ProcessVersion:
    def __init__(self):
        pass

    def get_process_version(self, request):
        try:
            version_id = request.match_info.get('id')
            if not version_id or (not utils.is_valid_type_id(version_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.get_process_version(version_id)
            if not response:
                return web.json_response(status=200, data={})
            data = json.dumps(response, sort_keys=True, default=str)
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    def get_process_versions(self, request):
        try:
            definition_id = request.rel_url.query['id']
            if not definition_id or (not utils.is_valid_type_id(definition_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.get_process_versions(definition_id)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def add_process_version(self, request):
        try:
            payload = await request.json()
            response = db_connector.add_process_version(payload)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=201, data=data)

    async def activate_process_version(self, request):
        try:
            payload = await request.json()
            definition_id = payload.get('definition_id')
            version_id = payload.get('version_id')
            if not definition_id or (not utils.is_valid_type_id(definition_id)) or (
                not utils.is_valid_optional_id(version_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.activate_process_version(definition_id, version_id)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def deactivate_process_version(self, request):
        try:
            payload = await request.json()
            definition_id = payload.get('definition_id')
            version_id = payload.get('version_id')
            if not definition_id or (not utils.is_valid_type_id(definition_id)) or (
                not utils.is_valid_optional_id(version_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.deactivate_process_version(definition_id, version_id)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def change_process_version_info(self, request):
        try:
            payload = await request.json()
            id = payload.get('id')
            name = payload.get('name')
            filename = payload.get('filename')
            if not id:
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.change_process_version_info(id, name, filename)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def delete_process_version(self, request):
        try:
            payload = await request.json()
            id = payload.get('id')
            if not id or (not utils.is_valid_type_id(id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.delete_process_version(id)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

class WebService:
    def __init__(self):
        pass

    async def get_service(self, request):
        try:
            service_id = request.match_info.get('id')
            if not service_id or (not utils.is_valid_type_id(service_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.get_service(service_id)
            if not response:
                raise aiohttp.web.HTTPServerError()
            health = await WebService().get_service_status(response)
            combined = utils.add_status_to_response(response, health)
            data = json.dumps(combined, sort_keys=True, default=str)
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def delete_service(self, request):
        try:
            payload = await request.json()
            service_id = payload.get('id')
            if not service_id or (not utils.is_valid_type_id(service_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.delete_service(service_id)
            if not response:
                raise aiohttp.web.HTTPServerError()
            data = json.dumps(response, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def add_service(self, request):
        try:
            payload = await request.json()
            response = db_connector.add_service(payload)
            if not response:
                raise aiohttp.web.HTTPServerError()
            health = await WebService().get_service_status(response)
            combined = utils.add_status_to_response(response, health)
            data = json.dumps(combined, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def update_service(self, request):
        try:
            payload = await request.json()
            service_id = payload.get('id')
            if not service_id or (not utils.is_valid_type_id(service_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.update_service(payload)
            if not response:
                raise aiohttp.web.HTTPServerError()
            health = await WebService().get_service_status(response)
            combined = utils.add_status_to_response(response, health)
            data = json.dumps(combined, sort_keys=True, default=str)
        except json.decoder.JSONDecodeError:
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def change_status(self, request):
        try:
            service_id = request.match_info.get('id')
            if not service_id or (not utils.is_valid_type_id(service_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.change_status(service_id)
            if not response:
                raise aiohttp.web.HTTPServerError()
            health = await WebService().get_service_status(response)
            combined = utils.add_status_to_response(response, health)
            data = json.dumps(combined, sort_keys=True, default=str)
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def get_services(self, request):
        try:
            response = db_connector.get_services()
            if not response:
                raise aiohttp.web.HTTPServerError()
            health = await WebService().get_service_status(response)
            combined = utils.add_status_to_response(response, health)
            data = json.dumps(combined, sort_keys=True, default=str)
        except aiohttp.web.HTTPBadRequest as err:
            traceback.print_stack(err)
            return web.json_response(status=400, data={})
        except aiohttp.web.HTTPServerError as err:
            traceback.print_stack(err)
            return web.json_response(status=500, data={})
        else:
            return web.json_response(status=200, data=data)

    async def fetch_status(self, session, address):
        try:
            async with session.get(address + '/status') as response:
                status = True if response.status == 200 else False
        except aiohttp.ClientConnectionError as err:
            status = False
        except aiohttp.InvalidURL as err:
            status = False
        return status

    async def get_service_status(self, services):
        ids = []
        statuses = []
        resolved_statuses = []
        web_service = WebService()
        async with aiohttp.ClientSession() as session:
            if isinstance(services, dict):
                service = services
                ids.append(service.get('id'))
                address = service.get('address')
                statuses.append(web_service.fetch_status(session, address))
            elif isinstance(services, list):
                for service in services:
                    ids.append(service.get('id'))
                    address = service.get('address')
                    statuses.append(web_service.fetch_status(session, address))
            resolved_statuses = await asyncio.gather(*statuses, return_exceptions=True)
        return dict(zip(ids, resolved_statuses))

    async def fetch_meta(self, address):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(address + '/meta') as response:
                        print(response.status)
                        data = await response.json()
            except aiohttp.ClientConnectionError as err:
                data = []
            except aiohttp.InvalidURL as err:
                data = []
            return data

    async def get_service_meta(self, request):
        try:
            address = request.rel_url.query['address']
            if not address:
                raise aiohttp.web.HTTPBadRequest()
            web_service = WebService()
            response = await web_service.fetch_meta(address)
            data = json.dumps(response, sort_keys=True, default=str)
        except aiohttp.web.HTTPBadRequest as err:
            return web.json_response(status=400, data=[])
        except aiohttp.web.HTTPServerError as err:
            return web.json_response(status=500, data=[])
        else:
            return web.json_response(status=200, data=data)

class Other():
    def __init__(self):
        pass

    async def handle_instance_info(request):
        instance_id = request.match_info.get("instance_id")
        m = get_model_for_instance(instance_id)
        if not m:
            raise aiohttp.aiohttp.web.HTTPNotFound
        instance = m.instances[instance_id].to_json()
        return aiohttp.web.json_response(instance)

    async def handle_task_info(request):
        instance_id = request.match_info.get("instance_id")
        task_id = request.match_info.get("task_id")
        m = get_model_for_instance(instance_id)
        if not m:
            raise aiohttp.aiohttp.web.HTTPNotFound
        instance = m.instances[instance_id]
        task = instance.model.elements[task_id]
        return aiohttp.web.json_response(task.get_info())

    async def search_instance(request):
        params = request.rel_url.query
        queries = []
        try:
            strip_lower = lambda x: x.strip().lower()
            check_colon = lambda x: x if ":" in x else f":{x}"
            queries = list(tuple(map(strip_lower, check_colon(q).split(":")))for q in params["q"].split(","))
        except:
            return aiohttp.web.json_response({"error": "invalid_query"}, status=400)

        result_ids = []
        ## FAKE
        models = {}
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
        return aiohttp.web.json_response({"status": "ok", "results": data})

    async def handle_form(request):
        post = await request.json()
        instance_id = request.match_info.get("instance_id")
        task_id = request.match_info.get("task_id")
        m = get_model_for_instance(instance_id)
        m.instances[instance_id].in_queue.put_nowait(UserFormMessage(task_id, post))
        return aiohttp.web.json_response({"status": "OK"})
    
    async def get_models(request):
        models = {}
        data = [m.to_json() for m in models.values()]
        return aiohttp.web.json_response({
                "status": "ok", 
                "results": data
            })

    async def handle_new_instance(request):
        _id = str(uuid4())
        model = request.match_info.get("model_name")
        instance = await app["bpmn_models"][model].create_instance(_id, {})
        asyncio.create_task(instance.run())
        return aiohttp.web.json_response({"id": _id})

    async def get_model(request):
        model_name = request.match_info.get("model_name")
        return aiohttp.web.FileResponse(
            path=os.path.join("models", app["bpmn_models"][model_name].model_path)
        )

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    process_definition = ProcessDefinition()
    process_version = ProcessVersion()
    web_service = WebService()
    other = Other()
    app.add_routes(
        [
            web.get('/process-definition', process_definition.get_process_definitions),
            web.get('/process-definition/{id}', process_definition.get_process_definition),
            web.post('/process-definition', process_definition.add_process_definition),
            web.patch('/process-definition/active', process_definition.activate_process_definition),
            web.patch('/process-definition/inactive', process_definition.deactivate_process_definition),
            web.patch('/process-definition/info', process_definition.change_process_definition_info),
            web.delete('/process-definition', process_definition.delete_process_definition),
            web.get('/process-version', process_version.get_process_versions),
            web.get('/process-version/{id}', process_version.get_process_version),
            web.post('/process-version', process_version.add_process_version),
            web.patch('/process-version/active', process_version.activate_process_version),
            web.patch('/process-version/inactive', process_version.deactivate_process_version),
            web.patch('/process-version/info', process_version.change_process_version_info),
            web.delete('/process-version', process_version.delete_process_version),
            web.get('/web-service', web_service.get_services),
            web.get('/web-service/{id}', web_service.get_service),
            web.post('/web-service', web_service.add_service),
            web.delete('/web-service', web_service.delete_service),
            web.patch('/web-service', web_service.update_service),
            web.patch('/web-service/{id}', web_service.change_status),
            web.get('/web-service/status', web_service.get_service_status),
            web.get('/service/meta', web_service.get_service_meta),
            #other
            web.get('/model', other.get_models),
            web.post('/model/{model_name}/instance', other.handle_new_instance),
            web.get('/model/{model_name}', other.get_model),
            web.get('/instance', other.search_instance),
            web.get('/instance/{instance_id}', other.handle_instance_info),
            web.get('/instance/{instance_id}/task/{task_id}', other.handle_task_info),
            web.post('/instance/{instance_id}/task/{task_id}/form', other.handle_form),
        ]
    )
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

    web.run_app(app, port=9000)
