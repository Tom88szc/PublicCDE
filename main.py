import re

class Validate:
    def __init__(self, transaction, response):
        """
        Constructor for the Validate class
        :param transaction: Dictionary representing a transaction
        :param response: Dictionary representing a response
        """
        self.transaction = transaction
        self.response = response

    def validate_placeholder(self, placeholder, value, trans_value=None):
        """
        Validates if the value meets the placeholder requirements.
        :param placeholder: Placeholder to validate against
        :param value: Value to be checked
        :param trans_value: Transaction value for {ECHO}, {EQUAL}, and {ISEXIST} validation
        :return: True if the value meets the placeholder requirements, False otherwise
        """
        alnum_match = re.match(r'\{AN:(\d+)-(\d+)\}', placeholder)
        num_match = re.match(r'\{N:(\d+)-(\d+)\}', placeholder)
        fixed_alnum_match = re.match(r'\{AN:(\d+)\}', placeholder)
        fixed_num_match = re.match(r'\{N:(\d+)\}', placeholder)
        echo_match = re.match(r'\{ECHO\}', placeholder)
        equal_match = re.match(r'\{EQUAL\}', placeholder)
        isexist_match = re.match(r'\{ISEXIST\}', placeholder)

        if alnum_match:
            min_length = int(alnum_match.group(1))
            max_length = int(alnum_match.group(2))
            return min_length <= len(value) <= max_length and value.isalnum()

        if num_match:
            min_length = int(num_match.group(1))
            max_length = int(num_match.group(2))
            return min_length <= len(value) <= max_length and value.isdigit()

        if fixed_alnum_match:
            length = int(fixed_alnum_match.group(1))
            return len(value) == length and value.isalnum()

        if fixed_num_match:
            length = int(fixed_num_match.group(1))
            return len(value) == length and value.isdigit()

        if echo_match:
            return value == trans_value

        if equal_match:
            return value == trans_value

        if isexist_match:
            return trans_value is not None

        return False

    def compare_value(self, trans_value, resp_value):
        """
        Compares the transaction value with the response value considering placeholders.
        :param trans_value: Transaction value
        :param resp_value: Response value
        :return: True if the values match, False otherwise
        """
        if re.match(r'\{AN:\d+(-\d+)?\}', resp_value) or re.match(r'\{N:\d+(-\d+)?\}', resp_value) or re.match(r'\{ECHO\}', resp_value) or re.match(r'\{EQUAL\}', resp_value) or re.match(r'\{ISEXIST\}', resp_value):
            return self.validate_placeholder(resp_value, trans_value, trans_value)
        return trans_value == resp_value

    def compare_transactions(self):
        """
        Compares the transaction with the response and returns a list of differences.
        :return: List of differences
        """
        differences = []
        all_keys = self.response.keys()  # Only check keys in the response
        for key in all_keys:
            trans_value = self.transaction.get(key)
            resp_value = self.response.get(key)
            if trans_value is None and not re.match(r'\{ISEXIST\}', resp_value):
                differences.append(f"Error: Field {key} is required in transaction.")
            elif not self.compare_value(trans_value, resp_value):
                if re.match(r'\{ECHO\}', resp_value) or re.match(r'\{EQUAL\}', resp_value):
                    differences.append(f"Error: Field {key} value is different. Expected: {trans_value}, Actual: {resp_value}")
                elif re.match(r'\{ISEXIST\}', resp_value):
                    differences.append(f"Error: Field {key} does not exist in transaction.")
                else:
                    differences.append(f"Key: {key}, Expected: {trans_value}, Actual: {resp_value}")
        return differences

    def display_differences(self):
        """
        Displays the differences between the transaction and the response along with a summary.
        """
        differences = self.compare_transactions()
        if differences:
            print(f"Transaction - \033[91mFailed\033[0m")  # Red color for failed
            for difference in differences:
                print(difference)
        else:
            print(f"Transaction - \033[92mPassed\033[0m")  # Green color for passed

        # Save report to file
        with open("report.txt", "w") as file:
            if differences:
                file.write("Transaction - Failed\n")
                for difference in differences:
                    file.write(difference + "\n")
            else:
                file.write("Transaction - Passed\n")


# Example usage with transactions and responses
transactions = {
}

responses = {
}

validator = Validate(transactions, responses)
validator.display_differences()
