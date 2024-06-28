def get_all_exception_to_realtime_validation_bnet(self, scenario):
    """
    Return a dictionary with SCENARIO_00X and TESTCASE_00X as keys
    and BNET_VALID_FIELDS as values.
    """

    file_path = os.path.join(AppConfig.load_scenarios_path + '\\' + scenario, 'scenario.yaml')
    data = read_yaml_file(file_path)
    scenario_dict = {}

    for sc_index, testcases in data.items():
        scenario_dict[sc_index] = {}
        for testcase_key, testcase_value in testcases.items():
            if str(testcase_key).startswith('TESTCASE_'):
                scenario_dict[sc_index][testcase_key] = testcase_value['BNET_VALID_FIELDS']

    print(scenario_dict)
    return scenario_dict


def get_all_data_fields(self):
    """
    Return a dictionary with SCENARIO_00X and TESTCASE_00X as keys
    and DATA as values.
    """

    file_path = os.path.join(self.work_dir, 'data.yaml')
    data = read_yaml_file(file_path)
    scenario_dict = {}

    for sc_index, testcases in data.items():
        scenario_dict[sc_index] = {}
        for testcase_key, testcase_value in testcases.items():
            if str(testcase_key).startswith('TESTCASE_'):
                scenario_dict[sc_index][testcase_key] = testcase_value['DATA']

    print(scenario_dict)
    return scenario_dict
