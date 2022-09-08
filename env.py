API_KEY = "xxxxxxxxxxxxx"
BASE_ID = "xxxxxxxxxxxxx"
# DS = ""


SYSTEM_VARS = {"_frontend_url": "http://localhost:9001"}
DB = {
    "provider": "postgres",
    "user": "postgres",
    "password": "FILLME",
    "host": "localhost",
    "database": "bpmn_praksa",
}
DS = {
    "airtable": {"type": "http-connector", "url": "http://0.0.0.0:8082"},
    "notification": {"type": "http-connector", "url": "http://0.0.0.0:8081"},
    "pdf": {"type": "http-connector", "url": "http://0.0.0.0:8083"},
}