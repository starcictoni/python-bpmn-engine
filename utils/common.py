import uuid

class SafeDict(dict):
    def __missing__(self, key):
        return "${" + key + "}"

def parse_expression(expression, process_variables):
    if (key := expression.replace("${", "").replace("}", "")) in process_variables:
        return process_variables[key]

    return expression.replace("${", "{").format_map(SafeDict(process_variables))

def is_valid_type_id(value):
    value = safe_cast_to_int(value)
    return True if isinstance(value, int) else False

def is_valid_optional_id(value):
    value = safe_cast_to_optional_int(value)
    return True if (value is None) or (isinstance(value, int)) else False

def safe_cast_to_int(value):
    try:
        value = int(value)
    except ValueError:
        return None
    else:
        return value

def safe_cast_to_optional_int(value):
    try:
        value = int(value)
    except ValueError:
        return value
    except TypeError:
        return value
    else:
        return value

def is_valid_uuid(value):
    try: 
        uuid.UUID(value)
        return True
    except ValueError:
        return False

def convert_to_list(response):
    temp = []
    temp.append(response)
    return temp

def add_status_to_response(response, health):
    if isinstance(response, dict):
        for key in health:
            if key == response.get('id'):
                response.update({
                    "status": health[key]
                })
    elif isinstance(response, list):
        for key, val in health.items():
            for service in response:
                if key == service.get('id'):
                    service.update({
                        "status": val
                    })
    return response

if __name__ == "__main__":
    test = "___${a[nice]}___"
    print(parse_expression(test, {"a": {"nice": ["OK"]}}))
