class PerspectiveGenerator:
    def __init__(self):
        self.perspectives = {}

    def generate_perspectives_prompt(self, task_description):
        """
        Verify the perspectives. If perspectives is None, generate perspectives with the help of an NLP system.
        Otherwise, return the perspectives.

        Args:
            perspectives: The evaluation perspectives.

        Returns:
            The verified perspectives.
        """
        with open('templates/perspectives_creation_prompt.txt', 'r') as file:
            perspectives_prompt = file.read()
            perspectives_prompt = perspectives_prompt.replace("{{PROMPT}}", task_description)  # Incorporate perspectives string into prompt string

        return perspectives_prompt

    def add_perspective(self, perspective_name, weight):
        """
        Add a perspective with its corresponding weight.

        Args:
            perspective_name (str): Name of the perspective.
            weight (float): Weight assigned to the perspective.
        """
        self.perspectives[perspective_name] = weight

    def add_multiple_perspectives(self, perspectives_dict):
        """
        Add multiple perspectives with their corresponding weights.

        Args:
            perspectives_dict (dict): Dictionary containing perspectives as keys and weights as values.
        """
        self.perspectives.update(perspectives_dict)

    def get_perspectives(self):
        """
        Retrieve the defined evaluation perspectives.

        Returns:
            dict: Dictionary of evaluation perspectives with their weights.
        """
        return self.perspectives

    def get_perspectives_string(self):
        """
        Print all perspectives to a string and return it.

        Returns:
            str: String representation of all perspectives.
        """
        perspectives_string = "Perspectives:\n"
        for perspective, weight in self.perspectives.items():
            perspectives_string += f"{perspective}: {weight}\n"
        return perspectives_string
