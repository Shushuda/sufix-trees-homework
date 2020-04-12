#!/usr/bin/env python3

from typing import Set, List, Union, Tuple

import suffix_tree


def count_substrings_in_strings(string_set: Union[Set[str], List[str]]) -> \
        Tuple[int, Set[str]]:

    substring_amount = 0
    found_substrings = set()

    for string in string_set:
        # I don't see any other way than to remove the string that we
        # currently search for from the joined string used for tree
        # construction.
        # Otherwise, the used library will always return the first
        # occurrence of the substring without any number of said
        # occurrences, which results in the program thinking that
        # there are as many substrings as there are strings in the
        # joined string, which is obviously false
        joined_string = '|'.join(string_set - {string})
        tree = suffix_tree.SuffixTree(joined_string)
        if tree.has_substring(string):
            substring_amount += 1
            # print for debugging purposes
            print(string + " in " + joined_string)
            found_substrings.add(string)

    # returns the amount of strings in the set that are also substrings of
    # at least one other string in the set + set of found substrings
    return substring_amount, found_substrings
