#!/usr/bin/env python3

from typing import Set, List, Union

import suffix_tree


def count_substrings_in_strings(string_set: Union[Set[str], List[str]]) -> \
        Union[int, set]:
    # in case someone calls with a list arg
    string_set = set(string_set)
    # helper var
    set_checker = string_set

    substring_amount = 0
    found_substrings = set()
    for element in string_set:
        tree = suffix_tree.SuffixTree(element)

        for string in set_checker - {element}:
            if tree.find_substring(string) != -1:
                substring_amount += 1
                # print for debugging purposes
                print(string + " in " + element)
                found_substrings.add(string)
        set_checker = set_checker - found_substrings

    # returns the amount of strings in the set that are also substrings of
    # at least one other string in the set
    return substring_amount, found_substrings
