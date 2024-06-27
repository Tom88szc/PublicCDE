import re


class Validate:
    def __init__(self, transactions, responses):
        """
        Konstruktor klasy Validate
        :param transactions: Lista słowników reprezentujących transakcje
        :param responses: Lista słowników reprezentujących odpowiedzi
        """
        self.transactions = transactions
        self.responses = responses

    def validate_placeholder(self, placeholder, value):
        """
        Weryfikuje, czy wartość spełnia wymagania placeholdera.
        :param placeholder: Placeholder do weryfikacji
        :param value: Wartość do sprawdzenia
        :return: True, jeśli wartość spełnia wymagania placeholdera, False w przeciwnym razie
        """
        alnum_match = re.match(r'\{AN:(\d+)-(\d+)\}', placeholder)
        num_match = re.match(r'\{N:(\d+)-(\d+)\}', placeholder)
        fixed_alnum_match = re.match(r'\{AN:(\d+)\}', placeholder)
        fixed_num_match = re.match(r'\{N:(\d+)\}', placeholder)

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

        return False

    def compare_value(self, trans_value, resp_value):
        """
        Porównuje wartość transakcji z wartością odpowiedzi uwzględniając placeholdery.
        :param trans_value: Wartość transakcji
        :param resp_value: Wartość odpowiedzi
        :return: True, jeśli wartości są zgodne, False w przeciwnym razie
        """
        if re.match(r'\{AN:\d+(-\d+)?\}', resp_value) or re.match(r'\{N:\d+(-\d+)?\}', resp_value):
            return self.validate_placeholder(resp_value, trans_value)
        return trans_value == resp_value

    def compare_transactions(self):
        """
        Porównuje transakcje z odpowiedziami i zwraca listę różnic.
        :return: Lista różnic
        """
        differences = []
        for i, (trans, resp) in enumerate(zip(self.transactions, self.responses)):
            trans_diff = {}
            all_keys = resp.keys()  # Only check keys in responses
            for key in all_keys:
                trans_value = trans.get(key)
                resp_value = resp.get(key)
                if trans_value is None:
                    trans_diff[key] = f"Error: Field {key} is missing in transaction."
                elif not self.compare_value(trans_value, resp_value):
                    trans_diff[key] = {'expected': trans_value, 'actual': resp_value}
            if trans_diff:
                differences.append({'transaction_index': i, 'differences': trans_diff})
        return differences

    def display_differences(self):
        """
        Wyświetla różnice między transakcjami a odpowiedziami oraz podsumowanie.
        """
        differences = self.compare_transactions()
        total_transactions = len(self.transactions)
        failed_transactions = len(differences)
        passed_transactions = total_transactions - failed_transactions

        report_lines = []

        for diff in differences:
            report_lines.append(f"Transaction index: {diff['transaction_index']}")
            for key, value in diff['differences'].items():
                if isinstance(value, str) and value.startswith("Error"):
                    report_lines.append(value)
                else:
                    report_lines.append(f"Key: {key}, Expected: {value['expected']}, Actual: {value['actual']}")

        report_lines.append(f"\nTotal transactions: {total_transactions}")
        report_lines.append(f"Passed: {passed_transactions}")
        report_lines.append(f"Failed: {failed_transactions}")

        with open("raport.txt", "w") as file:
            for line in report_lines:
                file.write(line + "\n")

        # Display the report in color
        for line in report_lines:
            if "Total transactions" in line:
                print(f"\033[94m{line}\033[0m")
            elif "Passed" in line:
                print(f"\033[92m{line}\033[0m")
            elif "Failed" in line:
                print(f"\033[91m{line}\033[0m")
            else:
                print(line)


# Przykład użycia
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
    {'DE001': '0110', 'DE002': '{AN:16}', 'DE003': '{N:1-6}', 'DE004': '{AN:1-5}', 'DE005': '0000'}
]

validator = Validate(transactions, responses)
validator.display_differences()
