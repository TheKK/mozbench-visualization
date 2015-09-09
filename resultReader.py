import json

class ResultReader(object):
    def __init__(self, filePath):
        self._json_root = {}

        with open(filePath) as fp:
            self._json_root = json.load(fp)

    def get_os_name(self):
        return self._json_root["platform"]

    def get_browser_names(self):
        browser_names_to_return = []

        for browser_name in self._json_root["browsers"]:
            browser_names_to_return.append(browser_name)

        return browser_names_to_return

    def get_test_case_name_list(self):
        test_case_names_to_return = []

        for browser_name in self._json_root["browsers"]:
            browser = self._json_root["browsers"][browser_name]

            for benchmark_name in browser["benchmarks"]:
                benchmark = browser["benchmarks"][benchmark_name]
                result_name = benchmark["result_name"]

                for single_case in benchmark["results"][0]:
                    test_case_names_to_return.append(single_case[result_name])
                break
            break

        return test_case_names_to_return

    def get_test_case_value_lists(self):
        test_case_value_lists = []

        for browser_name in self._json_root["browsers"]:
            browser = self._json_root["browsers"][browser_name]
            test_case_value_list = []

            for benchmark_name in browser["benchmarks"]:
                benchmark = browser["benchmarks"][benchmark_name]
                result_value_name = benchmark["result_value_name"]
                num_of_run = len(benchmark["results"])
                result_list = [0] * len(benchmark["results"][0])

                for result in benchmark["results"]:
                    num_of_case = len(result)

                    # Record results (might more than one)
                    for case_index in range(0, num_of_case):
                        single_case = result[case_index]
                        result_list[case_index] += single_case[result_value_name]

                # Get averange value
                for i in range(0, len(result_list)):
                    result_list[i] /= float(num_of_run)

                # Add results form this benchmark
                test_case_value_list += result_list

            test_case_value_lists.append(test_case_value_list)

        return test_case_value_lists
