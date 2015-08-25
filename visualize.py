#!/usr/bin/env python3

import argparse
import random
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import copy
import json
import os
import sys

from resultReader import ResultReader

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

def getTestCaseResultRatioLists(testCaseResultLists):
    testCaseResultListsToReturn = []
    numberOfCase = len(testCaseResultLists[0])

    for testCaseResultList in testCaseResultLists:
        ratio = []
        for i in range(0, numberOfCase):
            ratio.append(testCaseResultList[i] / testCaseResultLists[0][i])
        testCaseResultListsToReturn.append(ratio.copy())

    return testCaseResultListsToReturn

def cli(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='N', type=str, nargs='+',
                        help='an file for the visualization')
    args = parser.parse_args()

    result_reader = ResultReader(args.files[0])

    width = 0.3
    fig, ax = plt.subplots()

    fig.subplots_adjust(left=0.2)

    # Get needed propertiese from resultDict
    browserNameList = result_reader.getBrowserNames()
    caseNameList = result_reader.getTestCaseNameList()
    caseValueLists = result_reader.getTestCaseValueLists()
    numberOfCase = len(caseNameList)
    ind = np.arange(numberOfCase)  # the x locations for the groups
    resultRatiosList = getTestCaseResultRatioLists(caseValueLists)

    print(browserNameList)
    print(caseNameList)
    print(caseValueLists)

    # Set up bar colors
    barColorList = []
    for i in range(0, len(browserNameList)):
        barColorList.append("#" + "%.6x" % random.randrange(0, 256 ** 3))

    # Draw bars
    resultRectsList = []
    for index in range(0, len(resultRatiosList)):
        ratios = resultRatiosList[index]
        color = barColorList[index]
        rects = ax.barh(ind + width * (index + 1), ratios, width, color=color)
        resultRectsList.append(rects)

    # Draw legends
    legendPatches = []
    for index in range(0, len(browserNameList)):
        color = barColorList[index]
        browser = browserNameList[index]
        name_patch = mpatches.Patch(color=color, label=browser)
        legendPatches.append(name_patch)

    plt.legend(handles=legendPatches)

    # Add value on top of bars
    for browserIndex in range(0, len(resultRatiosList)):
        ratio = resultRatiosList[browserIndex]
        rects = resultRectsList[browserIndex]

        for benchmarkIndex in range(0, numberOfCase):
            rect = rects[benchmarkIndex]
            valueStr = "%.3f" % ratio[benchmarkIndex]
            fontSize = rect.get_height() * 40
            xloc = rect.get_width() * 0.95
            yloc = rect.get_y() + rect.get_height() / 2.0

            ax.text(xloc, yloc, valueStr, horizontalalignment="right",
                    verticalalignment='center', color="white", weight='bold',
                    size=fontSize)

    # add some text for labels, title and axes ticks
    ax.set_title('Performance benchmark result')
    ax.set_xlabel('Score ratio')
    ax.set_yticks(ind + width * (len(resultRatiosList) + 1) / 2.0)
    ax.set_yticklabels(caseNameList)

    plt.show()

if __name__ == "__main__":
    exit(cli(sys.argv[1:]))
