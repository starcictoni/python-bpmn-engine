
from http.client import HTTPException
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
import xml.dom.minidom

db_connector.setup_db()

# else:
#     raise aiohttp.HttpProcessingError(
#         code=resp.status, message=resp.reason,
#         headers=resp.headers)

class ProcessDefinition:
    def __init__(self):
        pass

    def get_process_definitions(self, request):
        try: 
            response = db_connector.get_process_definitions()
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

    def get_process_definition(self, request):
        try:
            definition_id = request.match_info.get('id')
            if not definition_id or (not utils.is_valid_type_id(definition_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.get_process_definition(definition_id)
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

    #TODO - REDO
    async def activate_process_definition(self, request):
        try:
            payload = await request.json()
            process_definition_id = payload.get('process_definition_id')
            process_version_id = payload.get('process_version_id')
            if not process_definition_id or (not utils.is_valid_type_id(process_definition_id)) or (
                not utils.is_valid_optional_id(process_version_id)):
                raise aiohttp.web.HTTPBadRequest()
                
            response = db_connector.activate_process_definition(process_definition_id, process_version_id)
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
    #TODO - REDO
    async def deactivate_process_definition(self, request):
        try:
            payload = await request.json()
            process_definition_id = payload.get('process_definition_id')
            if not process_definition_id or (not utils.is_valid_type_id(process_definition_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.deactivate_process_definition(process_definition_id)
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
    #TODO - REDO
    async def change_process_definition_info(self, request):
        try:
            payload = await request.json()
            process_definition_id = payload.get('process_definition_id')
            process_definition_name = payload.get('process_definition_name')
            process_filename = payload.get('file_name')
            if not process_definition_id:
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.change_process_definition_info(process_definition_id, process_definition_name, process_filename)
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
            process_definition_id = payload.get('process_definition_id')
            if not process_definition_id or (not utils.is_valid_type_id(process_definition_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.delete_process_definition(process_definition_id)
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

    def get_process_versions(self, request):
        try:
            process_definition_id = request.rel_url.query['process_definition_id']
            if not process_definition_id or (not utils.is_valid_type_id(process_definition_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.get_process_versions(process_definition_id)
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
            process_definition_id = payload.get('process_definition_id')
            process_version_id = payload.get('process_version_id')
            if not process_definition_id or (not utils.is_valid_type_id(process_definition_id)) or (
                not utils.is_valid_optional_id(process_version_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.activate_process_version(process_definition_id, process_version_id)
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
            process_definition_id = payload.get('process_definition_id')
            process_version_id = payload.get('process_version_id')
            if not process_definition_id or (not utils.is_valid_type_id(process_definition_id)) or (
                not utils.is_valid_optional_id(process_version_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.deactivate_process_version(process_definition_id, process_version_id)
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
            process_version_id = payload.get('process_version_id')
            process_version_name = payload.get('process_version_name')
            process_filename = payload.get('filename')
            if not process_version_id:
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.change_process_version_info(process_version_id, process_version_name, process_filename)
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
            process_version_id = payload.get('process_version_id')
            if not process_version_id or (not utils.is_valid_type_id(process_version_id)):
                raise aiohttp.web.HTTPBadRequest()
            response = db_connector.delete_process_version(process_version_id)
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

    async def fetch(self, session, address):
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
                statuses.append(web_service.fetch(session, address))
            elif isinstance(services, list):
                for service in services:
                    ids.append(service.get('id'))
                    address = service.get('address')
                    statuses.append(web_service.fetch(session, address))
            resolved_statuses = await asyncio.gather(*statuses, return_exceptions=True)
        return dict(zip(ids, resolved_statuses))
            
# @routes.get("/service/status")
# async def get_service_status(request):
#     services = db_connector.get_services()
#     services_hp, service_names = [], []
#     async with aiohttp.ClientSession() as session:
#         for service in services:
#             service_names.append(service.name)
#             services_hp.append(fetch(session, service.url))
#         service_statuses = await asyncio.gather(*services_hp, return_exceptions=True)
#         print(service_statuses)
#     return aiohttp.web.json_response(dict(zip(service_names, service_statuses)))



    def get_service_meta(self, request):
        pass



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    process_definition = ProcessDefinition()
    process_version = ProcessVersion()
    web_service = WebService()
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
            web.get('/web-service/meta', web_service.get_service_meta),
            web.get('/web-service/status', web_service.get_service_status),
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
