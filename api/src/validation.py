from jsonschema import Draft7Validator, draft7_format_checker

from .data import get_extra_functions, get_packages, get_services


standard_pattern = r"^([A-Za-z0-9\u00C0-\u00FF][A-Za-z0-9\u00C0-\u00FF\'\-\.\,\#]+([\ A-Za-z0-9\u00C0-\u00FF][A-Za-z0-9\u00C0-\u00FF\'\-\.\,\#]+)*)?$"
standard_pattern_no_number = r"^[A-Za-z\u00C0-\u00FF][A-Za-z\u00C0-\u00FF\'\-\.\,\#]+([\ A-Za-z\u00C0-\u00FF][A-Za-z\u00C0-\u00FF\'\-\.\,\#]+)*$"
domain_regex = r"^[a-zA-Z0-9\-\.]*$"
date_regex = r"^\d{4}-\d{2}-\d{2}$"


base_schema = Draft7Validator(
    {
        "type": "object",
        "properties": {
            "mode": {"enum": ["offer", "order"]},
            "package": {"type": "string", "enum": list(get_packages().keys())},
            "running_time": {
                "type": ["string", "integer"],
                "enum": ["unlimited"] + list(range(1, 13)),
            },
            "domain": {"type": "string", "pattern": domain_regex},
            "extra_functions": {
                "type": "object",
                "properties": {
                    function_key: {"type": "boolean"}
                    for function_key, function in get_extra_functions().items()
                    if not function.get("hidden")
                },
                "required": list(
                    key
                    for key, function in get_extra_functions().items()
                    if not function.get("hidden")
                ),
            },
            "event_name": {
                "type": "string",
                "pattern": standard_pattern,
                "minLength": 1,
            },
            "event_location": {
                "type": "string",
                "pattern": standard_pattern,
                "minLength": 1,
            },
            "event_from": {"type": "string", "pattern": date_regex},
            "event_to": {"type": "string", "pattern": date_regex},
            "expected_users": {"type": "integer", "min": 0},
            "contact_person": {
                "type": "object",
                "properties": {
                    "organisation": {
                        "type": "string",
                        "pattern": standard_pattern,
                        "minLength": 1,
                    },
                    "name": {
                        "type": "string",
                        "pattern": standard_pattern_no_number,
                        "minLength": 1,
                    },
                    "email": {"type": "string", "format": "email"},
                    "phone": {
                        "type": "string",
                        "pattern": r"^(0|\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42"
                        + r"\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|"
                        + r"4[987654310]|3[9643210]|2[70]|7|1))[\d\-/ ]{1,20}$",
                    },
                },
                "required": ["name", "email", "phone"],
            },
            "services": {
                "type": "object",
                "properties": {
                    service: {"type": "boolean"} for service in get_services().keys()
                },
                "required": list(get_services().keys()),
            },
            "billing_address": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "pattern": standard_pattern},
                    "extra": {"type": "string"},
                    "street": {"type": "string", "pattern": standard_pattern},
                    "zip": {"type": "string", "pattern": standard_pattern},
                    "city": {"type": "string", "pattern": standard_pattern},
                    "country": {"type": "string", "pattern": standard_pattern},
                },
            },
            "comment": {"type": "string"},
        },
        "required": [
            "mode",
            "package",
            "running_time",
            "extra_functions",
            "event_name",
            "event_location",
            "event_from",
            "event_to",
            "expected_users",
            "contact_person",
            "services",
        ],
    },
    format_checker=draft7_format_checker,
)
order_schema = {
    "type": "object",
    "properties": {
        "domain": {"type": "string", "minLength": 1},
        "tax_id": {"type": "string"},
        "billing_address": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "street": {"type": "string", "minLength": 1},
                "zip": {"type": "string", "minLength": 1},
                "city": {"type": "string", "minLength": 1},
                "country": {"type": "string", "minLength": 1},
            },
            "required": ["name", "street", "zip", "city", "country"],
        },
        "hosting_start": {"type": "string", "pattern": date_regex},
    },
    "required": ["domain", "billing_address", "hosting_start"],
}

mail_schema = Draft7Validator(
    {
        "type": "object",
        "properties": {"mail_address": {"type": "string", "format": "email"}},
        "required": ["mail_address"],
    },
    format_checker=draft7_format_checker,
)
