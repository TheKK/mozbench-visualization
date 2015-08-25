import json

class ResultReader(object):
    def __init__(self, filePath):
        self._json_root = {}

        with open(filePath) as fp:
            self._json_root = json.load(fp)

    def getBrowserNames(self):
        browserNamesToReturn = []

        for browserName in self._json_root["browsers"]:
            browserNamesToReturn.append(browserName)

        return browserNamesToReturn

    def getTestCaseNameList(self):
        testCaseNamesToReturn = []

        for browserName in self._json_root["browsers"]:
            browser = self._json_root["browsers"][browserName]

            for benchmarkName in browser["benchmarks"]:
                benchmark = browser["benchmarks"][benchmarkName]
                resultName = benchmark["resultName"]

                for singleCase in benchmark["results"][0]:
                    testCaseNamesToReturn.append(singleCase[resultName])
                break
            break

        return testCaseNamesToReturn

    def getTestCaseValueLists(self):
        testCaseValueLists = []

        for browserName in self._json_root["browsers"]:
            browser = self._json_root["browsers"][browserName]
            testCaseValueList = []

            for benchmarkName in browser["benchmarks"]:
                benchmark = browser["benchmarks"][benchmarkName]
                resultValueName = benchmark["resultValueName"]
                numOfRun = len(benchmark["results"])
                resultList = [0] * len(benchmark["results"][0])

                for result in benchmark["results"]:
                    numOfCase = len(result)

                    # Record results (might more than one)
                    for caseIndex in range(0, numOfCase):
                        singleCase = result[caseIndex]
                        resultList[caseIndex] += singleCase[resultValueName]

                # Get averange value
                for i in range(0, len(resultList)):
                    resultList[i] /= float(numOfRun)

                # Add results form this benchmark
                testCaseValueList += resultList

            testCaseValueLists.append(testCaseValueList)

        return testCaseValueLists
