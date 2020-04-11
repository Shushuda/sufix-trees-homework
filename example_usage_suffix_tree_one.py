#!/usr/bin/env python3

import suffix_tree_one

# zbior Z zlozony z k lancuchow
# k to jeden string w zbiorze (typ set), elementow zbioru jest k
# w tym przykladzie k == 5
Z = {"iksde", "de iks", "iks de", "de", "iks", "ksde"}
print("Zbior lancuchow:")
print(Z)

amount, substrings = suffix_tree_one.count_substrings_in_strings(Z)

msg = "Lancuchow bedacych podlancuchem innego lancucha zbioru Z jest: "
print(msg + str(amount))
print("Znalezione podlancuchy:")
print(substrings)
