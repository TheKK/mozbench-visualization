#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import copy
import json
import os
import sys

"""
    @return list
    [
     { browserName,
       browserVersion,
       results : [
                  { benchmarkName,
                    reaultValue
                  },
                  ...
                 ]
     },
     ...
    ]
"""

def getBrowserNames(jsonRoot):
    browserNamesToReturn = []

    for browserName in jsonRoot["browsers"]:
        browserNamesToReturn.append(browserName)

    return browserNamesToReturn

def getTestCaseNameList(jsonRoot):
    testCaseNamesToReturn = []

    for browserName in jsonRoot["browsers"]:
        for suite in jsonRoot["browsers"][browserName]["suites"]:
            caseName = suite["result_name"]

            for case in suite["results"][0]:
                testCaseNamesToReturn.append(case[caseName])
        break

    return testCaseNamesToReturn

def getTestCaseValueLists(jsonRoot):
    testCaseValueLists = []

    for browserName in jsonRoot["browsers"]:
        testCaseValueList = []
        for suite in jsonRoot["browsers"][browserName]["suites"]:
            testCaseResultValueName = suite["result_value"]

            # FIXME Only take one results currenttly
            for result in suite["results"]:
                for case in result:
                    testCaseValueList.append(case[testCaseResultValueName])
                break
        testCaseValueLists.append(testCaseValueList)

    return testCaseValueLists

def getTestCaseResultRatioLists(testCaseResultLists):
    testCaseResultListsToReturn = []
    numberOfCase = len(testCaseResultLists[0])

    for testCaseResultList in testCaseResultLists[1:]:
        ratio = []
        for i in range(0, numberOfCase):
            ratio.append(testCaseResultList[i] /
                                               testCaseResultLists[0][i])
        testCaseResultListsToReturn.append(ratio.copy())

    return testCaseResultListsToReturn

def cli(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='N', type=str, nargs='+',
                        help='an file for the visualization')
    args = parser.parse_args()

    jsonResultRoot = []
    with open(args.files[0]) as fp:
            jsonResultRoot = json.load(fp)

    width = 0.3
    fig, ax = plt.subplots()

    # Get neede propertiese from resultDict
    browserNameList = getBrowserNames(jsonResultRoot)
    caseNameList = getTestCaseNameList(jsonResultRoot)
    caseValueLists = getTestCaseValueLists(jsonResultRoot)
    numberOfCase = len(caseNameList)
    ind = np.arange(numberOfCase)  # the x locations for the groups
    ratios = getTestCaseResultRatioLists(caseValueLists)

    # Draw bars
    ax.bar(ind, np.ones(numberOfCase), width, color='#fc9937')
    for ratio in ratios:
        ax.bar(ind+width, ratio, width, color='#318ff9')

    # Draw legends
    legendPatches = []
    name_patch = mpatches.Patch(color='#fc9937', label=browserNameList[0])
    legendPatches.append(name_patch)

    for browser in browserNameList[1:]:
        name_patch = mpatches.Patch(color='#318ff9', label=browser)
        legendPatches.append(name_patch)

    plt.legend(handles=legendPatches)

    # add some text for labels, title and axes ticks
    ax.set_title('Performance benchmark result')
    ax.set_ylabel('Score ratio')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(caseNameList, rotation=80)

    plt.show()

if __name__ == "__main__":
    exit(cli(sys.argv[1:]))
