import re

class Validate:
    def __init__(self, transactions, responses):
        """
        Constructor for the Validate class
        :param transactions: List of dictionaries representing transactions
        :param responses: List of dictionaries representing responses
        """
        self.transactions = transactions
        self.responses = responses

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
        Compares transactions with responses and returns a list of differences.
        :return: List of differences
        """
        differences = []
        for i, (trans, resp) in enumerate(zip(self.transactions, self.responses)):
            trans_diff = {}
            all_keys = resp.keys()  # Only check keys in responses
            for key in all_keys:
                trans_value = trans.get(key)
                resp_value = resp.get(key)
                if trans_value is None and not re.match(r'\{ISEXIST\}', resp_value):
                    trans_diff[key] = f"Error: Field {key} is required in transaction."
                elif not self.compare_value(trans_value, resp_value):
                    if re.match(r'\{ECHO\}', resp_value) or re.match(r'\{EQUAL\}', resp_value):
                        trans_diff[key] = f"Error: Field {key} value is different. Expected: {trans_value}, Actual: {resp_value}"
                    elif re.match(r'\{ISEXIST\}', resp_value):
                        trans_diff[key] = f"Error: Field {key} does not exist in transaction."
                    else:
                        trans_diff[key] = {'expected': trans_value, 'actual': resp_value}
            if trans_diff:
                differences.append({'transaction_index': i, 'differences': trans_diff})
        return differences

    def display_differences(self):
        """
        Displays the differences between transactions and responses along with a summary.
        """
        differences = self.compare_transactions()
        total_transactions = len(self.transactions)
        failed_transactions = len(differences)
        passed_transactions = total_transactions - failed_transactions

        report_lines = []

        for i in range(total_transactions):
            if any(diff['transaction_index'] == i for diff in differences):
                report_lines.append(f"Transaction index: {i}")
                for diff in differences:
                    if diff['transaction_index'] == i:
                        for key, value in diff['differences'].items():
                            if isinstance(value, str) and value.startswith("Error"):
                                report_lines.append(value)
                            else:
                                report_lines.append(f"Key: {key}, Expected: {value['expected']}, Actual: {value['actual']}")
                report_lines.append(f"Transaction index: {i} - \033[91mFailed\033[0m")  # Red color for failed
            else:
                report_lines.append(f"Transaction index: {i} - \033[92mPassed\033[0m")  # Green color for passed

        report_lines.append(f"\033[94m\nTotal transactions: {total_transactions}\033[0m")
        report_lines.append(f"\033[92mPassed: {passed_transactions}\033[0m")
        report_lines.append(f"\033[91mFailed: {failed_transactions}\033[0m")

        # Save report to file
        with open("raport.txt", "w") as file:
            for line in report_lines:
                file.write(re.sub(r'\033\[\d+m', '', line) + "\n")  # Remove color codes for the file

        # Display the report in color
        for line in report_lines:
            print(line)


# Usage example
transactions = [
    {'DE001': '0100', 'DE002': '407132120069790', 'DE003': '170000',
     'DE004': '000000000000', 'DE006': '000000000000', 'DE007': '{TIME}',
     'DE011': '061336', 'DE012': '061336', 'DE013': '0628', 'DE015': '0402',
     'DE018': '6011', 'DE022': '020', 'DE024': '600000', 'DE025': '00',
     'DE031': '006911079075', 'DE032': '0628', 'DE037': '407132120069790',
     'DE039': '000', 'DE041': 'MCB0817RJ', 'DE042': '601107', 'DE043': 'FIRST DATA',
     'DE048': 'C6A051010123065ffA72-05de-48ec-9517-4bef861c090a',
     'DE049': '985', 'DE051': '985', 'DE060': '230B0000000010610090210',
     'DE063': 'MCD0817RJ'},
    {'DE001': '0100', 'DE002': '407132120069790', 'DE003': '170000',
     'DE004': '000000000000', 'DE006': '000000000000', 'DE007': '{TIME}',
     'DE011': '061336', 'DE012': '061336', 'DE013': '0628', 'DE015': '0402',
     'DE018': '6011', 'DE022': '020', 'DE024': '600000', 'DE025': '00',
     'DE031': '006911079075', 'DE032': '0628', 'DE037': '407132120069790',
     'DE039': '000', 'DE041': 'MCB0817RJ', 'DE042': '601107', 'DE043': 'FIRST DATA',
     'DE048': 'C6A051010123065ffA72-05de-48ec-9517-4bef861c090a',
     'DE049': '985', 'DE051': '985', 'DE060': '230B0000000010610090210',
     'DE063': 'MCD0817RJ'},
    {'DE001': '0100', 'DE002': '407132120069790', 'DE003': '170000',
     'DE004': '000000000000', 'DE006': '000000000000', 'DE007': '{TIME}',
     'DE011': '061336', 'DE012': '061336', 'DE013': '0628', 'DE015': '0402',
     'DE018': '6011', 'DE022': '020', 'DE024': '600000', 'DE025': '00',
     'DE031': '006911079075', 'DE032': '0628', 'DE037': '407132120069790',
     'DE039': '000', 'DE041': 'MCB0817RJ', 'DE042': '601107', 'DE043': 'FIRST DATA',
     'DE048': 'C6A051010123065ffA72-05de-48ec-9517-4bef861c090a',
     'DE049': '985', 'DE051': '985', 'DE060': '230B0000000010610090210',
     'DE063': 'MCD0817RJ'}
]

responses = [
    {'DE001': '0100', 'DE002': '407132120069790', 'DE003': '170000',
     'DE004': '000000000000', 'DE006': '000000000000', 'DE007': '{TIME}',
     'DE011': '061336', 'DE012': '061336', 'DE013': '0628', 'DE015': '0402',
     'DE018': '6011', 'DE022': '020', 'DE024': '600000', 'DE025': '00',
     'DE031': '006911079075', 'DE032': '0628', 'DE037': '407132120069790',
     'DE039': '000', 'DE041': 'MCB0817RJ', 'DE042': '601107', 'DE043': 'FIRST DATA',
     'DE048': 'C6A051010123065ffA72-05de-48ec-9517-4bef861c090a',
     'DE049': '985', 'DE051': '985', 'DE060': '230B0000000010610090210',
     'DE063': 'MCD0817RJ'},
    {'DE001': '0100', 'DE002': '407132120069790', 'DE003': '170000',
     'DE004': '000000000000', 'DE006': '000000000000', 'DE007': '{TIME}',
     'DE011': '061336', 'DE012': '061336', 'DE013': '0628', 'DE015': '0402',
     'DE018': '6011', 'DE022': '020', 'DE024': '600000', 'DE025': '00',
     'DE031': '006911079075', 'DE032': '0628', 'DE037': '407132120069790',
     'DE039': '000', 'DE041': 'MCB0817RJ', 'DE042': '601107', 'DE043': 'FIRST DATA',
     'DE048': 'C6A051010123065ffA72-05de-48ec-9517-4bef861c090a',
     'DE049': '985', 'DE051': '985', 'DE060': '230B0000000010610090210',
     'DE063': 'MCD0817RJ'},
    {'DE001': '0110', 'DE002': '{ECHO}', 'DE003': '{EQUAL}', 'DE008': '{ISEXIST}', 'DE005': '0000'}
]

validator = Validate(transactions, responses)
validator.display_differences()
