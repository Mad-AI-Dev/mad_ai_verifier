import json
from api_simple import get_response
from json_utils import extract_json_from_message, extract_json_string_from_message


def get_verified_response(prompt, agent, expected_structure):
    retry_count = 6
    data = None
    
    for _ in range(retry_count):
        response_raw = get_response(prompt, agent)

        print()        
        print("RESPONSE: ", response_raw)
        print()        

        # Check if expected_structure matches at the beginning
        for key, value_type in expected_structure.items():
            if key == "component_code":
                component_code = response_raw
                data = {
                    "component_code": component_code
                }
                return data

        # Extract data from JSON response
        try:
            response_json = extract_json_string_from_message(response_raw)
            data = json.loads(response_json)
            if isinstance(data, dict) and validate_json_structure(data, expected_structure):
                break
        except json.JSONDecodeError:
            print("Invalid response format. Data extraction failed.")
    
    if data is None:
        print(f"Failed to extract data after {retry_count} retries.")
        return
    
    # Additional verification logic
    if not validate_data(data):
        print("Invalid data. Additional verification failed.")
        return
    
    return data





def validate_json_structure_noarray(json_data, expected_structure):
    for key, value_type in expected_structure.items():
        print (key, value_type)
        if key not in json_data or not isinstance(json_data[key], value_type):
            return False
    return True

def validate_json_structure(json_data, expected_structure):
    for key, value_type in expected_structure.items():
        print ('key, value_type', key, value_type)
        
        
        if key not in json_data:
            print ('key not in json_data')
            
            return False
        if isinstance(value_type, list):
            print ('value_type is list')
            if not isinstance(json_data[key], list):
                print ('json_data[key] is not list')
                return False
            # Validate each item in the array
            for item in json_data[key]:
                print ('item', item)
                if not isinstance(item, value_type[0]):
                    print ('item is not value_type[0]')
                    return False
        else:
            print ('value_type is not list')
            if not isinstance(json_data[key], value_type):
                print ('json_data[key] is not value_type')
                return False
    return True


def validate_data(data):
    # Add your specific validation logic here
    return True

def validate_subtasks(subtasks):
    for subtask in subtasks:
        if not isinstance(subtask, dict):
            return False
        expected_keys = ["id", "name", "description", "status"]
        for key in expected_keys:
            if key not in subtask or not isinstance(subtask[key], str):
                return False
    return True