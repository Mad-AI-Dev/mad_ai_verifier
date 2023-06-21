import os
import openai
from typing import List
from models.openai.api_simple import get_response

# Depending on the GPT-4 model available, update the list below
GPT_MODEL_NAMES = {
    'small': 'gpt-4.5-turbo',
    'medium': 'gpt-4.5-turbo',
    'large': 'gpt-4.5-turbo'
}

def fill_gaps_with_underscore(string):
    # Split the string by spaces
    words = string.split()

    # Create a new list to store the modified words
    modified_words = []

    # Iterate over each word
    for word in words:
        # If the word has gaps (multiple consecutive underscores), replace them with a single underscore
        modified_word = word.replace('_', ' ')
        modified_word = modified_word.replace(' ', '_')

        # Add the modified word to the list
        modified_words.append(modified_word)

    # Join the modified words back into a string with spaces
    filled_string = ' '.join(modified_words)

    return filled_string


class GPTModel:
    def __init__(self):
        # You might want to load model-related configurations here
        # For instance, the API key for OpenAI
        self.load_configuration()

    def load_configuration(self):
        # Load your OpenAI API key
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def select_model(self, CONTEXTSIZE: int):
        """
        Selects the appropriate GPT model based on the CONTEXTSIZE
        """
        if CONTEXTSIZE < 5000:
            self.model_name = GPT_MODEL_NAMES['small']
        elif CONTEXTSIZE < 10000:
            self.model_name = GPT_MODEL_NAMES['medium']
        else:
            self.model_name = GPT_MODEL_NAMES['large']

    def verify(self, perspective, prompts: List[str]) -> str:
        """
        Sends the prompt array to the GPT model for verification and receives verification feedback
        """
        responses = []
        
        i = 0
        role = "You are a " + perspective
        role_name = fill_gaps_with_underscore(perspective)
        for prompt in prompts:
            i += 1
            # Call the GPT-4 model for each prompt and get the response
            ## print(f"{role} is working on: {prompt}")
            print(f"{perspective} is working on: prompt {i} of {len(prompts)}")
            response = get_response(prompt, role)

            # Save verification results as a .md file
            file_name = "prompt_" + str(i) + "_" + role_name + ".md"
            with open("output/" + file_name, "w") as f:
                f.write(prompt)


            responses.append(response)

        return "\n".join(responses)

    def verify_criteria(self, perspective, prompt) -> str:
        """
        Sends the prompt array to the GPT model for verification and receives verification feedback
        """
        
        role = "You are a " + perspective
        role_name = fill_gaps_with_underscore(perspective)

        print(f"{perspective} is working on criteria")
        response = get_response(prompt, role)

        # Save verification results as a .md file
        file_name = "criteria"  + "_" + role_name + ".md"
        with open("output/" + file_name, "w") as f:
            f.write(prompt)

        # Save verification results as a .md file
        file_name = "criteria_response"  + "_" + role_name + ".md"
        with open("output/" + file_name, "w") as f:
            f.write(response)

        return response

    def verify_perspectives(self, perspective, prompt) -> str:
        """
        Sends the prompt array to the GPT model for verification and receives verification feedback
        """
        
        role = "You are a " + perspective
        role_name = fill_gaps_with_underscore(perspective)

        print(f"{perspective} is being hired.")
        response = get_response(prompt, role)

        # Save verification results as a .md file
        file_name = "perspective"  + "_" + role_name + ".md"
        with open("output/" + file_name, "w") as f:
            f.write(prompt)

        # Save verification results as a .md file
        file_name = "perspective_response"  + "_" + role_name + ".md"
        with open("output/" + file_name, "w") as f:
            f.write(response)

        return response