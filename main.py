messages = {
    1: {'TESTCASE_0001': {'DE001': '0110', 'DE002': '4071321206096790', 'DE003': '170000', 'DE004': '00000000'}},
    2: {'TESTCASE_0001': {'DE001': '0110', 'DE002': '4071321206096790', 'DE003': '170000', 'DE004': '00000000'}}
}

rt_validation = {
    'SCENARIO_001': {'TESTCASE_0001': {'DE001': '0110', 'DE049': '985'}, 'TESTCASE_0002': {'DE001': '0110', 'DE049': '985'}},
    'SCENARIO_002': {'TESTCASE_0001': {'DE001': '0110', 'DE049': '985'}}
}


class TLVParser:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def parse(self):
        result = []
        while self.index < len(self.data):
            tag = self._parse_tag()
            length = self._parse_length()
            value = self._parse_value(length)
            result.append({'Tag': tag, 'Length': length, 'Value': value})
        return result

    def _parse_tag(self):
        tag = self.data[self.index:self.index + 2]
        self.index += 2
        return tag

    def _parse_length(self):
        length_hex = self.data[self.index:self.index + 2]
        length = int(length_hex, 16)
        self.index += 2
        return length

    def _parse_value(self, length):
        value = self.data[self.index:self.index + (length * 2)]
        self.index += length * 2
        return value


# Przykład użycia
tlv_data = "010300DEADBEEF02010503012345"
parser = TLVParser(tlv_data)
parsed_data = parser.parse()
for entry in parsed_data:
    print(entry)

# Przekształcanie kluczy w messages na stringi i dopasowywanie formatu do rt_validation
messages_converted = {f'SCENARIO_{str(key).zfill(3)}': value for key, value in messages.items()}

def get_scenario_testcase(scenario, testcase):
    message_data = messages_converted.get(scenario, {}).get(testcase)
    rt_validation_data = rt_validation.get(scenario, {}).get(testcase)

    if message_data and rt_validation_data:
        return {
            'messages': message_data,
            'rt_validation': rt_validation_data
        }
    elif message_data:
        return {
            'messages': message_data,
            'rt_validation': None
        }
    elif rt_validation_data:
        return {
            'messages': None,
            'rt_validation': rt_validation_data
        }
    else:
        return None

# Przykład użycia funkcji
scenario = 'SCENARIO_001'
testcase = 'TESTCASE_0001'
result = get_scenario_testcase(scenario, testcase)

if result:
    print(f'Data for {scenario} {testcase}:')
    print('Messages:', result['messages'])
    print('RT Validation:', result['rt_validation'])
else:
    print(f'No data found for {scenario} {testcase}')
