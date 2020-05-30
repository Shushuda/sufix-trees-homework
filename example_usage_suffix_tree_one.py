#!/usr/bin/env python3

import suffix_tree_my_imp

# zbior Z zlozony z k lancuchow
# k to jeden string w zbiorze (typ set), elementow zbioru jest k
# w tym przykladzie k == 5
Z = {"iksde", "de iks", "iks de", "de", "iks", "ksde"}
text = "#".join(Z) + "$"

print("String jako calosc:", text)
print("String jako zbior:", Z)

print("-------------------")
print("Generowanie drzewa z tekstu jako calosc:")
tree_1 = suffix_tree_my_imp.GenSuffixTree(text)
tree_1.build_suffix_tree()
substring_count_1, substrings_1 = tree_1.count_substrings_in_strings()
print(f"Lancuchow bedacych podlancuchem innego lancucha zbioru Z "
      f"jest: {substring_count_1}")
print(f"Znalezione podlancuchy: {substrings_1}")

print("-------------------")
print("Generowanie drzewa z tekstu jako zbior:")
tree2 = suffix_tree_my_imp.GenSuffixTree(Z, joined_string=False)
tree2.build_suffix_tree()
substring_count_2, substrings_2 = tree2.count_substrings_in_strings()
print(f"Lancuchow bedacych podlancuchem innego lancucha zbioru Z "
      f"jest: {substring_count_2}")
print(f"Znalezione podlancuchy: {substrings_2}")
