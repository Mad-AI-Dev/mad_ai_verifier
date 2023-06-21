import json

def generate_string_from_json(json_obj):
    def process_value(value):
        if isinstance(value, dict):
            return generate_string_from_json(value)
        elif isinstance(value, list):
            if value:
                element = process_value(value[0])
                return f"[{element}]"
            else:
                return "[]"
        else:
            return value.__name__

    string_representation = "{"
    for key, value in json_obj.items():
        processed_value = process_value(value)
        string_representation += f'"{key}": {processed_value}, '
    string_representation = string_representation.rstrip(", ")
    string_representation += "}"
    return string_representation

# Example usage
expected_structure = {
    "nlp_task": str,
    "task_description": str,
    "nested_array": [str],
    "nested_object": {
        "property1": int,
        "property2": float
    }
}

def convert_json_to_python_object(json_dict):
    # Define a dictionary to store the converted Python object structure
    python_object = {}

    # Iterate over each key-value pair in the JSON dictionary
    for key, value in json_dict.items():
        # If the value is a string, convert it to the corresponding Python type
        if value == "str":
            python_object[key] = str
        # If the value is a list, convert it to a list of strings
        elif value == "[str]":
            python_object[key] = [str]
        # If the value is a nested object, recursively convert it
        elif isinstance(value, dict):
            python_object[key] = convert_json_to_python_object(value)
        # If the value is an integer, convert it to the int type
        elif value == "int":
            python_object[key] = int
        # If the value is a float, convert it to the float type
        elif value == "float":
            python_object[key] = float
        # If the value is a boolean, convert it to the bool type
        elif value == "bool":
            python_object[key] = bool
        # If the value is a null/None, convert it to the None type
        elif value == "null":
            python_object[key] = None
        # If the value is a list, convert it to the list type
        elif value == "list":
            python_object[key] = list
        # If the value is a tuple, convert it to the tuple type
        elif value == "tuple":
            python_object[key] = tuple
        # If the value is a dictionary, convert it to the dict type
        elif value == "dict":
            python_object[key] = dict
        # If the value is a set, convert it to the set type
        elif value == "set":
            python_object[key] = set
        # If the value is a frozenset, convert it to the frozenset type
        elif value == "frozenset":
            python_object[key] = frozenset
        # If the value is a complex number, convert it to the complex type
        elif value == "complex":
            python_object[key] = complex
        # If the value is a bytes object, convert it to the bytes type
        elif value == "bytes":
            python_object[key] = bytes
        # If the value is a bytearray object, convert it to the bytearray type
        elif value == "bytearray":
            python_object[key] = bytearray

    return python_object


# Example usage:
obj = {
    "step_number": int,
    "step_description": str,
    "name": str,
    "description": str,
    "tasks": [
        {
            "task_name": str,
            "task_type": str,
            "tree_of_thought": bool,
            "quality_check": bool,
            "input_values": [str],
            "output_values": [str],
            "prompt": str,
            "expected_structure": {
                "functionalities": [str]
            },
            "replacements": dict
        }
    ]
}

def convert_python_object_to_json(obj):
    # Helper function to convert Python types to serializable types
    def convert_type(value):
        if isinstance(value, type):
            return value.__name__
        return value

    # Recursively convert the object to JSON-compatible types
    def convert(obj):
        if isinstance(obj, dict):
            return {key: convert(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert(value) for value in obj]
        else:
            return convert_type(obj)

    # Convert the object to JSON representation
    json_representation = json.dumps(convert(obj), indent=4)
    return json_representation


def extract_json_from_message(message):
    start_token = "{"
    end_token = "}"

    # Find the start and end indices of the JSON object within the message
    start_index = message.find(start_token)
    end_index = message.rfind(end_token)

    if start_index == -1 or end_index == -1:
        return "JSON object not found in the message"

    # Extract the JSON object from the message
    json_string = message[start_index:end_index + len(end_token)]

    # Parse the JSON string into a Python object
    json_data = json.loads(json_string)

    return json_data


def extract_json_string_from_message(message):
    start_token = "{"
    end_token = "}"

    # Find the start and end indices of the JSON object within the message
    start_index = message.find(start_token)
    end_index = message.rfind(end_token)

    if start_index == -1 or end_index == -1:
        return "JSON object not found in the message"

    # Extract the JSON object from the message
    json_string = message[start_index:end_index + len(end_token)]

    return json_string
