import os
import json

class SolutionLoader:
    def __init__(self):
        self.data = {}
        
    def load_solutions(self, folder_path):
        """
        This function reads all the text files in the specified folder and stores their contents in a list of dictionaries.
        Each dictionary represents a solution, with the file name as the 'name' key and its contents as the 'content' key.

        :param folder_path: The path to the folder containing the solution files.
        :return: List of dictionaries representing the solutions.
        """
        solutions = []  # Create an empty list to store the solutions

        try:
            files = os.listdir(folder_path)
            for file_name in files:
                if file_name.endswith('.txt'):
                    with open(os.path.join(folder_path, file_name), 'r') as f:
                        content = f.read()
                        solution = {'name': file_name, 'prefix': "Solution " + file_name, 'description': file_name, 'content': content}
                        solutions.append(solution)
        except Exception as e:
            print(f"An error occurred while loading solutions: {e}")
            return []

        return solutions



    def save_to_json(self, path="data/solutions.json"):
        """
        This function saves the solutions data to a json file.

        :param path: The path where to save the solutions.json file.
        :return: None
        """
        try:
            with open(path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"An error occurred while saving solutions to a JSON file: {e}")
        
    def load_from_json(self, path="data/solutions.json"):
        """
        This function loads the solutions data from a json file.

        :param path: The path where to load the solutions.json file from.
        :return: Dictionary with the file name as the key and its contents as the value.
        """
        try:
            with open(path, 'r') as f:
                self.data = json.load(f)
        except Exception as e:
            print(f"An error occurred while loading solutions from a JSON file: {e}")
            return {}

        return self.data
