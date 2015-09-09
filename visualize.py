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

def get_test_case_result_ratio_lists(test_case_result_lists):
    test_case_result_listsToReturn = []
    number_of_case = len(test_case_result_lists[0])

    for test_case_result_list in test_case_result_lists:
        ratio = []
        for i in range(0, number_of_case):
            # Since python 2.X behave like C, we cast value to float for safe
            ratio.append(test_case_result_list[i] /
                         float(test_case_result_lists[0][i]))
        test_case_result_listsToReturn.append(copy.copy(ratio))

    return test_case_result_listsToReturn

def cli(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='N', type=str, nargs='+',
                        help='an file for the visualization')
    args = parser.parse_args()

    result_readers = []

    # Create ResultReader from input files
    for file_name in args.files:
        result_readers.append(ResultReader(file_name))

    result_reader = result_readers[0]

    # TODO: Make this flexiable
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.2)

    # Get needed propertiese from resultDict
    browser_name_list = []
    case_name_list = []
    case_value_lists = []

    for result_reader in result_readers:
        # Use platform + browser as id
        browser_names = result_reader.get_browser_names()
        os_name = result_reader.get_os_name()

        for browser_name in browser_names:
            browser_name_list.append(os_name + "_" + browser_name);

        # Retrieve test case names
        if (case_name_list == []):
            case_name_list = result_reader.get_test_case_name_list()
        else:
            ya_case_name_list = result_reader.get_test_case_name_list()
            try:
                # Make sure each file has the same test cases
                for name in ya_case_name_list:
                    case_name_list.index(name)
            except ValueError as e:
                print("Error: the files you input has different test cases")
                print("Test case: %s" % name) # Not sure if this would work

        # Retrieve test case value, since case name have no error, this would be
        # fine as well
        case_value_lists.extend(result_reader.get_test_case_value_lists())

    # browser_name_list = result_reader.get_browser_names()
    # case_name_list = result_reader.get_test_case_name_list()
    # case_value_lists = result_reader.get_test_case_value_lists()
    number_of_case = len(case_name_list)
    result_ratios_list = get_test_case_result_ratio_lists(case_value_lists)

    ind = np.arange(number_of_case)  # the x locations for the groups

    # Set up bar colors
    bar_color_list = []
    browser_num = len(browser_name_list)
    color_gape = int(100 / browser_num)
    for i in range(0, browser_num):
        bar_color_list.append("#" + "%x%x%x" % (
            100 + i * color_gape,
            100 + i * color_gape,
            180
            )
        )

    # Set bar width
    width = 0.5 / number_of_case;

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
            font_size = rect.get_height() * 80
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
