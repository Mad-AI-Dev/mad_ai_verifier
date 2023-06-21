import json
from models.gpt_tools import count_tokens

class VerificationProcessor:
    def __init__(self):
        self.criteria_string = None
        with open('templates/prompt_template.txt', 'r') as file:
            self.prompt_template = file.read()
        with open('templates/prompt_template_result.txt', 'r') as file:
            self.prompt_postfix_template = file.read()

    def include_criteria(self, criteria_string):
        with open('templates/prompt_template_criteria.txt', 'r') as file:
            criteria_tremplate = file.read()
            criteria_tremplate = criteria_tremplate.replace("{{CRITERIA}}", criteria_string)  # Incorporate criteria string into prompt string
            self.criteria_string = criteria_tremplate


    def initialize_verification_process(self, solutions, verification_option, CONTEXTSIZE, criteria_string = None):
        prompt_array = []
        ## prompt_string = self.generate_prompt_string()
        ## prompt_array.append(prompt_string)
        
        if criteria_string != None:
            self.include_criteria(criteria_string)

        if verification_option == 'simple':
            self.simple_verification_process(solutions, prompt_array, CONTEXTSIZE)
        elif verification_option == 'perspective':
            self.perspective_verification_process(solutions, prompt_array, CONTEXTSIZE)
        elif verification_option == 'perspective_ai':
            self.perspective_verification_ai_process(solutions, prompt_array, CONTEXTSIZE)
        else:
            print("Invalid verification option.")
        
        return prompt_array

    def generate_prompt_string(self):
        prompt_string = self.prompt_template  # Incorporate prompt template into prompt string
        if self.criteria_string != None:
            prompt_string += self.criteria_string  # Incorporate criteria string into prompt string
        return prompt_string

    def append_solution_to_prompt(self, prompt_string, solution, CONTEXTSIZE, prompt_array):
        temp_prompt_string = prompt_string + solution['prefix'] + solution['content'] + self.prompt_postfix_template
        token_size = count_tokens(temp_prompt_string)

        if token_size < CONTEXTSIZE:
            prompt_string += f"\n## {solution['prefix']}:\n\n{solution['content']}\n"
        else:
            prompt_string += self.prompt_postfix_template
            prompt_array.append(prompt_string)
            prompt_string = self.generate_prompt_string() + f"\n## {solution['prefix']}:\n\n{solution['content']}\n"

        return prompt_string

    def simple_verification_process(self, solutions, prompt_array, CONTEXTSIZE):
        ## prompt_string = prompt_array[0]
        prompt_string = self.generate_prompt_string()

        for solution in solutions:
            prompt_string = self.append_solution_to_prompt(prompt_string, solution, CONTEXTSIZE, prompt_array)

        prompt_string += self.prompt_postfix_template
        prompt_array.append(prompt_string)

    def perspective_verification_process(self, solutions, prompt_array, CONTEXTSIZE):
        ## prompt_string = prompt_array[0]
        prompt_string = self.generate_prompt_string()

        for solution in solutions:
            prompt_string = self.append_solution_to_prompt(prompt_string, solution, CONTEXTSIZE, prompt_array)
            perspective_aspect = input("Enter the perspective aspect for the solution: ")
            prompt_string += perspective_aspect

            token_size = count_tokens(prompt_string)
            if token_size >= CONTEXTSIZE:
                prompt_array.append(prompt_string)
                prompt_string = self.generate_prompt_string()

        prompt_array.append(prompt_string)

    def perspective_verification_ai_process(self, solutions, prompt_array, CONTEXTSIZE):
        ## prompt_string = prompt_array[0]
        prompt_string = self.generate_prompt_string()
        ai_feedback = ""

        for solution in solutions:
            prompt_string = self.append_solution_to_prompt(prompt_string, solution, CONTEXTSIZE, prompt_array)
            perspective_aspect = input("Enter the perspective aspect for the solution: ")
            prompt_string += perspective_aspect

            token_size = count_tokens(prompt_string)
            if token_size >= CONTEXTSIZE:
                prompt_array.append(prompt_string)
                prompt_string = self.generate_prompt_string()

            # Send prompt_string to AI model for verification and receive AI-generated feedback
            ai_feedback += "AI Feedback for solution: " + solution['content'] + "\n"

        prompt_array.append(prompt_string)

        # Save verification feedback, including AI-generated feedback, as a .md file
        with open('verification_feedback.md', 'w') as file:
            file.write(ai_feedback)
