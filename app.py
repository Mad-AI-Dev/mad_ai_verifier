import json
import os
import sys
import dotenv
from user_input import UserInputHandler
from solution_loader import SolutionLoader
from verification_processor import VerificationProcessor
from evaluation_processor import EvaluationProcessor
from perspectives_generator import PerspectiveGenerator
from perspective_object import PerspectiveObject
from models.gpt_model import GPTModel
from models.openai.api_simple import get_response
from assistants.assistant import Assistant
from models.openai.json_utils import extract_json_string_from_message

class App:
    def __init__(self):
        self.user_input_handler = UserInputHandler()
        self.solution_loader = SolutionLoader()
        self.verification_processor = VerificationProcessor()
        self.gpt_model = GPTModel()
        self.assistant = Assistant()
    
    def start_application(self):
        # Identify start mode based on the arguments provided.
        if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
            self.json_input_mode(sys.argv[1])
        else:
            self.user_interactive_mode()

    def user_interactive_mode(self):
        # Receive and handle user input interactively
        task_description, folder_path, verification_option, CONTEXTSIZE = self.user_input_handler.get_user_input_interactive()
        self.execute_verification(task_description, folder_path, verification_option, CONTEXTSIZE)

    def json_input_mode(self, json_path):
        # Handle user input from JSON file
        task_description, folder_path, verification_option, CONTEXTSIZE, criteria, perspectives, use_perspectives = self.user_input_handler.get_user_input_json(json_path)

        self.execute_verification(task_description, folder_path, verification_option, CONTEXTSIZE, criteria, perspectives, use_perspectives)

    # Process a single perspective
    def process_perspective(self, task_description, folder_path, verification_option, CONTEXTSIZE, criteria, perspective):
        # Select appropriate GPT model based on the CONTEXTSIZE
        self.gpt_model.select_model(CONTEXTSIZE)

        # Create an instance of EvaluationProcessor
        evaluation_processor = EvaluationProcessor()

        # Add multiple criteria to the evaluation processor
        if criteria is None:
            # Call a function to generate criteria using an NLP system
            criteria_prompt = evaluation_processor.generate_criteria_prompt(task_description)
            verified_criteria = self.gpt_model.verify_criteria(perspective, criteria_prompt)
            verified_criteria_json_string = extract_json_string_from_message(verified_criteria)
            criteria = json.loads(verified_criteria_json_string)

        evaluation_processor.add_multiple_criteria(criteria)
        criteria_string = evaluation_processor.get_criteria_string()

        # Load solutions
        solutions = self.solution_loader.load_solutions(folder_path)

        # Initialize verification process based on the selected option
        prompts = self.verification_processor.initialize_verification_process(solutions, verification_option, CONTEXTSIZE, criteria_string)

        # Obtain verification feedback from the model for the current perspective
        perspective_feedback = self.gpt_model.verify(perspective, prompts)

        # Save verification results for the current perspective as a .md file
        perspective_filename = f"output/verification_results_{perspective}.md"
        with open(perspective_filename, "w") as f:
            f.write(perspective_feedback)


    def generate_perspectives(self, task_description):
        # Create an instance of EvaluationProcessor
        perspectives_generator = PerspectiveGenerator()

        # Call a function to generate perspectives using an NLP system
        main_perspective = "Project Manager"
        perspectives_prompt = perspectives_generator.generate_perspectives_prompt(task_description)
        verified_perspectives = self.gpt_model.verify_perspectives(main_perspective, perspectives_prompt)
        verified_perspectives_json_string = extract_json_string_from_message(verified_perspectives)
        verified_perspective_json = json.loads(verified_perspectives_json_string)
        
        return verified_perspective_json

    def execute_verification(self, task_description, folder_path, verification_option, CONTEXTSIZE, criteria=None, perspectives=None, use_perspectives=True):

        # Process each perspective in the perspectives array
        if use_perspectives and perspectives is not None:
            for perspective in perspectives:
                self.process_perspective(task_description, folder_path, verification_option, CONTEXTSIZE, criteria, perspective)
        elif use_perspectives and perspectives is None:
            generated_perspectives = self.generate_perspectives(task_description)
            for perspective in generated_perspectives:
                self.process_perspective(task_description, folder_path, verification_option, CONTEXTSIZE, criteria, perspective)
        else:
            self.process_perspective(task_description, folder_path, verification_option, CONTEXTSIZE, criteria, None)  # Process without a specific perspective

        # Provide feedback to the user
        print("Verification process is completed. Check the output folder for the results.")


if __name__ == "__main__":
    app = App()
    dotenv.load_dotenv()
    app.start_application()
