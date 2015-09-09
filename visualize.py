#!/usr/bin/env python2

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

def get_test_case_result_ratio_lists(test_case_result_lists):
    test_case_result_listsToReturn = []
    number_of_case = len(test_case_result_lists[0])

    for test_case_result_list in test_case_result_lists:
        ratio = []
        for i in range(0, number_of_case):
            ratio.append(test_case_result_list[i] / test_case_result_lists[0][i])
        test_case_result_listsToReturn.append(copy.copy(ratio))

    return test_case_result_listsToReturn

def cli(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='N', type=str, nargs='+',
                        help='an file for the visualization')
    args = parser.parse_args()

    result_reader = ResultReader(args.files[0])

    width = 0.2
    fig, ax = plt.subplots()

    fig.subplots_adjust(left=0.2)

    # Get needed propertiese from resultDict
    browser_name_list = result_reader.get_browser_names()
    case_name_list = result_reader.get_test_case_name_list()
    case_value_lists = result_reader.get_test_case_value_lists()
    number_of_case = len(case_name_list)
    ind = np.arange(number_of_case)  # the x locations for the groups
    result_ratios_list = get_test_case_result_ratio_lists(case_value_lists)

    # Set up bar colors
    bar_color_list = []
    for i in range(0, len(browser_name_list)):
        bar_color_list.append("#" + "%.6x" % random.randrange(0, 256 ** 3))

    # Draw bars
    result_rects_list = []
    for index in range(0, len(result_ratios_list)):
        ratios = result_ratios_list[index]
        color = bar_color_list[index]
        rects = ax.barh(ind + width * index, ratios, width, color=color)
        result_rects_list.append(rects)

    # Draw legends
    legend_patches = []
    for index in range(0, len(browser_name_list)):
        color = bar_color_list[len(browser_name_list) - index - 1]
        browser = browser_name_list[index]
        name_patch = mpatches.Patch(color=color, label=browser)
        legend_patches.append(name_patch)

    plt.legend(handles=legend_patches)

    # Add value on top of bars
    for browser_index in range(0, len(result_ratios_list)):
        ratio = result_ratios_list[browser_index]
        rects = result_rects_list[browser_index]

        for benchmark_index in range(0, number_of_case):
            rect = rects[benchmark_index]
            value_str = "%.3f" % ratio[benchmark_index]
            font_size = rect.get_height() * 40
            xloc = rect.get_width() * 0.95
            yloc = rect.get_y() + rect.get_height() / 2.0

            ax.text(xloc, yloc, value_str, horizontalalignment="right",
                    verticalalignment='center', color="white", weight='bold',
                    size=font_size)

    # add some text for labels, title and axes ticks
    ax.set_title('Performance benchmark result')
    ax.set_xlabel('Score ratio')
    ax.set_yticks(ind + width * len(result_ratios_list) / 2.0)
    ax.set_yticklabels(case_name_list)

    plt.show()

if __name__ == "__main__":
    exit(cli(sys.argv[1:]))
