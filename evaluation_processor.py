class EvaluationProcessor:
    def __init__(self):
        self.criteria = {}

    def generate_criteria_prompt(self, task_description):
        """
        Verify the criteria. If criteria is None, generate criteria with the help of an NLP system.
        Otherwise, return the criteria.

        Args:
            criteria: The evaluation criteria.

        Returns:
            The verified criteria.
        """
        with open('templates/critera_creation_prompt.txt', 'r') as file:
            criteria_prompt = file.read()
            criteria_prompt = criteria_prompt.replace("{{PROMPT}}", task_description)  # Incorporate criteria string into prompt string

        return criteria_prompt

    def add_criterion(self, criterion_name, weight):
        """
        Add a criterion with its corresponding weight.

        Args:
            criterion_name (str): Name of the criterion.
            weight (float): Weight assigned to the criterion.
        """
        self.criteria[criterion_name] = weight

    def add_multiple_criteria(self, criteria_dict):
        """
        Add multiple criteria with their corresponding weights.

        Args:
            criteria_dict (dict): Dictionary containing criteria as keys and weights as values.
        """
        self.criteria.update(criteria_dict)

    def get_criteria(self):
        """
        Retrieve the defined evaluation criteria.

        Returns:
            dict: Dictionary of evaluation criteria with their weights.
        """
        return self.criteria

    def get_criteria_string(self):
        """
        Print all criteria to a string and return it.

        Returns:
            str: String representation of all criteria.
        """
        criteria_string = "Weighted Criteria:\n"
        for criterion, weight in self.criteria.items():
            criteria_string += f"{criterion}: {weight}\n"
        return criteria_string
