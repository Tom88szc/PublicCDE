import os
import yaml

class ScenarioProcessor:
    def __init__(self, work_dir):
        self.work_dir = work_dir

    def generate_testcase(self, card_profiles, data, card_ord, testcase_name):
        # Placeholder implementation for generating test cases
        pass

    def process_testcase(self, scenarios, card_profiles):
        scenario_data = {}
        for sc_index, scenario in enumerate(scenarios, start=1):
            tc_ids = []
            scenario_data[sc_index] = {}

            for testcase_key, testcase_value in scenario.items():
                if str(testcase_key).startswith('TESTCASE_'):
                    tc_ids.append(testcase_key)
                    data = scenario[testcase_key]['DATA']
                    scenario_data[sc_index][testcase_key] = {"DATA": data}
                    testcase_name = scenario[testcase_key]['NAME']
                    testcase_description = scenario[testcase_key]['DESCRIPTION']
                    card_ord = scenario[testcase_key]['CARD_ORD']
                    repeat = scenario[testcase_key]['REPEAT']
                    self.generate_testcase(card_profiles, data, card_ord, testcase_name)

                    # Conditional
                    if 'FULL_REVERSAL' not in scenario[testcase_key].keys():
                        continue
                    else:
                        full_reversal = scenario[testcase_key]['FULL_REVERSAL']
                        if 'PARTIAL_REVERSAL' not in scenario[testcase_key].keys():
                            continue
                        else:
                            partial_reversal = scenario[testcase_key]['PARTIAL_REVERSAL']
        self.save_data(scenario_data)

    def save_data(self, scenario_data):
        file_path = os.path.join(self.work_dir, 'data.yaml')
        with open(file_path, 'a') as f:
            yaml.dump(scenario_data, f, default_flow_style=False, allow_unicode=True)

# Example usage
scenarios = [
    {
        "SCENARIO_DESCRIPTION": "Description for scenario 1",
        "CONFIG_SCENARIO": "Config for scenario 1",
        "TESTCASE_0001": {
            "NAME": "Test Case 1",
            "DESCRIPTION": "Description for Test Case 1",
            "CARD_ORD": "Card Order 1",
            "REPEAT": "Repeat 1",
            "DATA": "Data for Test Case 1"
        },
        "TESTCASE_0002": {
            "NAME": "Test Case 2",
            "DESCRIPTION": "Description for Test Case 2",
            "CARD_ORD": "Card Order 2",
            "REPEAT": "Repeat 2",
            "DATA": "Data for Test Case 2"
        }
    },
    {
        "SCENARIO_DESCRIPTION": "Description for scenario 2",
        "CONFIG_SCENARIO": "Config for scenario 2",
        "TESTCASE_0001": {
            "NAME": "Test Case 3",
            "DESCRIPTION": "Description for Test Case 3",
            "CARD_ORD": "Card Order 3",
            "REPEAT": "Repeat 3",
            "DATA": "Data for Test Case 3"
        }
    }
]

processor = ScenarioProcessor(work_dir='.')
processor.process_testcase(scenarios, card_profiles={})
