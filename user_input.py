import json
import os
import sys

class UserInputHandler:
    def __init__(self):
        pass

    def get_user_input_interactive(self):
        """
        This function interacts with the user to collect all the necessary inputs for the project.
        Inputs are collected via command line prompts.
        """
        print("Welcome to the Application.")
        task_description = input("Please provide a project description: ")
        folder_path = input("Please specify the folder path with solution text files: ")
        while not os.path.isdir(folder_path):
            print(f"No folder found at {folder_path}")
            folder_path = input("Please specify a valid folder path: ")

        verification_option = input("Please select the desired verification option (simple, perspective, ai-supported): ")
        while verification_option not in ['simple', 'perspective', 'ai-supported']:
            print(f"{verification_option} is not a valid option.")
            verification_option = input("Please select a valid verification option (simple, perspective, ai-supported): ")
        
        CONTEXTSIZE = input("Please specify the desired CONTEXTSIZE value: ")
        while not CONTEXTSIZE.isdigit() or int(CONTEXTSIZE) <= 0:
            print(f"{CONTEXTSIZE} is not a valid value for CONTEXTSIZE.")
            CONTEXTSIZE = input("Please specify a valid CONTEXTSIZE value: ")
        CONTEXTSIZE = int(CONTEXTSIZE)
        
        return task_description, folder_path, verification_option, CONTEXTSIZE

    def get_user_input_json(self, json_path):
        """
        This function reads the user inputs from a JSON file.
        Inputs are read and validated from the provided JSON file.
        """
        print("Reading user input from JSON file.")
        with open(json_path, "r") as json_file:
            user_data = json.load(json_file)

        task_description = user_data.get("task_description", "")
        folder_path = user_data.get("folder_path", "")
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"No folder found at {folder_path}")

        verification_option = user_data.get("verification_option", "")
        if verification_option not in ['simple', 'perspective', 'ai-supported']:
            raise ValueError(f"{verification_option} is not a valid verification option.")

        use_perspectives = user_data.get("use_perspectives", "")
        if use_perspectives not in [True, False]:
            raise ValueError(f"{use_perspectives} is not a valid perspective usage option.")

        CONTEXTSIZE = user_data.get("CONTEXTSIZE", "")
        if not str(CONTEXTSIZE).isdigit() or int(CONTEXTSIZE) <= 0:
            raise ValueError(f"{CONTEXTSIZE} is not a valid CONTEXTSIZE value.")
        CONTEXTSIZE = int(CONTEXTSIZE)

        criteria = user_data.get("criteria")
        if not criteria:
            criteria = None
        elif not isinstance(criteria, dict):
            raise ValueError("Criteria should be provided as a dictionary.")

        perspectives = user_data.get("perspectives")
        if not perspectives:
            perspectives = None
        elif not isinstance(perspectives, list):
            raise ValueError("Perspectives should be provided as a list.")


        return task_description, folder_path, verification_option, CONTEXTSIZE, criteria, perspectives, use_perspectives
