#!/usr/bin/env python3
"""
My suffix tree implementation written in Python based on a Go implementation
from this site:
https://rosettacode.org/wiki/Ukkonen’s_Suffix_Tree_Construction

I couldn't find a way to traverse the tree comfortably with the previous
implementation and I couldn't find any Python implementation that would create
generalised suffix trees, so I've found one written in Go and rewrote it
to Python. I needed those Node variables that weren't present in the previous
implementation and adding them in would require rewriting the logic of the
tree building (which I just didn't know how to do), so I decided to just find
something else instead of writing the entire implementation by myself.
This one seemed nice and gave me the Node variables I needed and Go is simple
enough to allow almost 1:1 rewriting to Python.
"""
from typing import Tuple, Set


class GenSuffixTree:

    def __init__(self, string, joined_string=True):
        if joined_string:
            text_array = string.replace("$", "").split("#")
        else:
            text_array = string
            string = '#'.join(text_array)

        if string[-1] != "$":
            string += "$"

        # I tried to do the array mapping,
        # but I had no idea what to use it for...

        # array = {}
        # index = 0
        # for item in text_array:
        #     length = len(item)
        #     array.update(
        #         {item:
        #             {'index': index,
        #              'length': length}
        #          }
        #     )
        #     index += length + 1

        self.array = text_array

        self.suffix_tree = self.SuffixTree(string)

    def build_suffix_tree(self):
        self.suffix_tree.build_suffix_tree()

    def find_one_substring(self, substring) -> bool:
        return self.suffix_tree.find_one_substring(substring)

    def find_every_substring(self, substring) -> int:
        return self.suffix_tree.find_every_substring(substring)

    def count_substrings_in_strings(self) -> Tuple[int, Set[str]]:
        return self.suffix_tree.count_substrings_in_strings(self.array)

    class Node:

        def __init__(self):
            self.children = {}
            self.suffix_link = None
            self.start = None
            # simulating pointers (lists in Python are mutable)
            self.end = []
            self.suffix_index = None

    class SuffixTree:

        def __init__(self, string):
            self.text = string
            self.root = None
            self.last_new_node = None
            self.active_node = None
            self.active_edge = -1
            self.active_length = 0
            self.remaining_suffix_count = 0
            self.root_end = None
            self.split_end = None
            self.size = -1
            # simulating pointers (lists in Python are mutable)
            self.leaf_end = [-1]

        def new_node(self, start, end):
            node = GenSuffixTree.Node()
            node.children = {}
            node.suffix_link = self.root
            node.start = start
            node.end = end
            node.suffix_index = -1
            return node

        def edge_length(self, node):
            if node == self.root:
                return 0
            return node.end[0] - node.start + 1

        def walk_down(self, curr_node):
            if self.active_length >= self.edge_length(curr_node):
                self.active_edge += self.edge_length(curr_node)
                self.active_length -= self.edge_length(curr_node)
                self.active_node = curr_node
                return True
            return False

        def extend_suffix_tree(self, pos):
            self.leaf_end[0] = pos
            self.remaining_suffix_count += 1
            self.last_new_node = None

            while self.remaining_suffix_count > 0:
                if self.active_length == 0:
                    self.active_edge = pos

                if self.active_node.children.get(self.text[self.active_edge]) \
                        is None:
                    self.active_node.children[self.text[self.active_edge]] = \
                        self.new_node(pos, self.leaf_end)
                    if self.last_new_node:
                        self.last_new_node.suffix_link = self.active_node
                        self.last_new_node = None
                else:
                    next_n = self.active_node.children.get(
                        self.text[self.active_edge])

                    if self.walk_down(next_n):
                        continue
                    if self.text[next_n.start + self.active_length] \
                            == self.text[pos]:
                        if self.last_new_node and \
                                self.active_node is not self.root:
                            self.last_new_node.suffix_link = self.active_node
                            self.last_new_node = None
                        self.active_length += 1
                        break

                    temp = next_n.start + self.active_length - 1
                    self.split_end = temp
                    split = self.new_node(next_n.start, [self.split_end])
                    self.active_node.children[self.text[self.active_edge]] \
                        = split
                    split.children[self.text[pos]] = self.new_node(
                        pos, self.leaf_end)
                    next_n.start += self.active_length
                    split.children[self.text[next_n.start]] = next_n

                    if self.last_new_node:
                        self.last_new_node.suffix_link = split
                    self.last_new_node = split

                self.remaining_suffix_count -= 1

                if self.active_node == self.root and self.active_length > 0:
                    self.active_length -= 1
                    self.active_edge = pos - self.remaining_suffix_count + 1
                elif self.active_node is not self.root:
                    self.active_node = self.active_node.suffix_link

        def set_suffix_index_by_DFS(self, node, label_height):
            if node is None:
                return
            if node.start is not -1:
                print(self.text[node.start:(node.end[0] + 1)])
            leaf = 1
            for i in node.children.values():
                leaf = 0
                self.set_suffix_index_by_DFS(
                    i,
                    label_height + self.edge_length(i))
            if leaf == 1:
                node.suffix_index = self.size - label_height

        def build_suffix_tree(self):
            self.size = len(self.text)
            temp = -1
            self.root_end = temp
            self.root = self.new_node(-1, self.root_end)
            self.active_node = self.root
            for i in range(0, self.size):
                self.extend_suffix_tree(i)
            label_height = 0
            self.set_suffix_index_by_DFS(self.root, label_height)

        def traverse_for_substring(self, substring, index, start, end):
            text_index = start
            while text_index <= end[0] and index < len(substring):
                if self.text[text_index] is not substring[index]:
                    return -1
                text_index += 1
                index += 1
            if index >= len(substring):
                return 1
            return

        def get_leaf_count(self, node):
            if node.suffix_index > -1:
                return 1
            count = 0
            for i in node.children.values():
                count += self.get_leaf_count(i)
            return count

        def do_traversal(self, node, substring, index, one_substring=False):
            if node is None:
                return -1, 0
            substring_count = 0
            if node.start is not -1:
                found = self.traverse_for_substring(substring, index,
                                                    node.start, node.end)
                if found == 1:
                    if node.suffix_index > -1 or one_substring:
                        substring_count = 1
                    else:
                        substring_count = self.get_leaf_count(node)
                    return substring_count
                elif found is -1:
                    return substring_count

            index = index + self.edge_length(node)
            if index < len(substring):
                if node.children.get(substring[index]):
                    count = self.do_traversal(
                        node.children.get(substring[index]), substring, index,
                        one_substring)
                    return count
                else:
                    return substring_count
            else:
                return substring_count

        def find_one_substring(self, substring):
            substring_count = self.do_traversal(self.root, substring, 0,
                                                one_substring=True)
            if substring_count == 1:
                return True
            else:
                return False

        def find_every_substring(self, substring):
            substring_count = self.do_traversal(self.root, substring, 0)
            return substring_count

        def count_substrings_in_strings(self, array):
            found_substrings = set()
            substring_amount = 0

            for substring in array:
                result = self.find_every_substring(substring)
                if result > 1:
                    substring_amount += 1
                    found_substrings.add(substring)

            # returns the amount of strings in the set that are also substrings
            # of at least one other string in the set + set of found substrings
            return substring_amount, found_substrings
