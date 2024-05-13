# SpellBee.com solver (can be used for other word games as well - suitable dictionary required for validation [AllWords.txt - 60k words, Answers.txt - 39k words])
# Tested with minimal word length of 4 on:
# AMD Ryzen 7 5800H
# 8 cores, 16 threads at 3.2GHz

import csv
import multiprocessing
from functools import partial
from tqdm import tqdm


def binary_search(word, file_path="Answers.txt"):
    with open(file_path, "r") as file:
        lines = file.readlines()
        low = 0
        high = len(lines) - 1

        while low <= high:
            mid = (low + high) // 2
            current_word = lines[mid].strip()

            if current_word == word:
                return mid
            elif current_word < word:
                low = mid + 1
            else:
                high = mid - 1

        return -1


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []


class Words:
    def __init__(self, letters, required_letter, min_length, max_length):
        self.root = None
        self.letters = sorted(letters)
        self.required_letter = required_letter
        self.min_length = min_length
        self.max_length = max_length
        self.found_words = []
        self.dfs_duration = 0

        if self.min_length > self.max_length:
            raise ValueError(
                "Minimum word length cannot be greater than maximum word length."
            )

    @staticmethod
    def count_nodes(node):
        if node is None:
            return 0
        count = 1
        for child in node.children:
            count += Words.count_nodes(child)
        return count

    def build_tree(self):
        self.root = TreeNode("root")
        self._build_tree_recursive(self.root, 0)

    def _build_tree_recursive(self, node, depth):
        if depth >= self.max_length:
            return

        for letter in self.letters:
            node.children.append(TreeNode(letter))

        for child in node.children:
            self._build_tree_recursive(child, depth + 1)

    def display_tree(self, node, level=0):
        if node is not None:
            if level == 0:
                for child in node.children:
                    self.display_tree(child, level + 1)
            elif node.data == self.letters[-1]:
                print("  " * level + "└─" + node.data)
                for child in node.children:
                    self.display_tree(child, level + 1)
            else:
                print("  " * level + "├─" + node.data)
                for child in node.children:
                    self.display_tree(child, level + 1)

    def save_to_csv(self, file_path=None):
        if file_path is None:
            duration = self.dfs_duration
            if duration > 60:
                duration = f"{duration/60:.2f}min"
            elif duration > 1:
                duration = f"{duration:.2f}sec"
            elif duration > 0.001:
                duration = f"{duration*1000:.2f}ms"
            else:
                duration = f"{duration*1000000:.2f}µs"

            file_name = f"{''.join(self.letters)}-{self.required_letter}-tree-{self.min_length}-{self.max_length}-{duration}.csv"
            file_path = file_name

        with open(file_path, "w", newline="") as csvfile:
            fieldnames = ["Word", "Level", "Index"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for word, level, index in self.found_words:
                writer.writerow({"Word": word, "Level": level, "Index": index})

        print(f"\nCSV file saved as: {file_path}\n")

    def dfs(self, show=False):
        nodes_count = self.count_nodes(self.root)

        with tqdm(total=nodes_count, desc="DFS Progress") as pbar:
            self._dfs_recursive(self.root, "", 0, pbar)

        self.dfs_duration = pbar.format_dict["elapsed"]

        if show:
            print(f"\nFound {len(self.found_words)} words:\n")
            for word, level, index in self.found_words:
                print(f"Word: {word}, Level: {level}, Index: {index+1}")
        else:
            print(f"\nFound {len(self.found_words)} words")

        if self.dfs_duration > 60:
            print(f"\nDFS Duration: {self.dfs_duration/60:.2f} minutes")
        elif self.dfs_duration > 1:
            print(f"\nDFS Duration: {self.dfs_duration:.2f} seconds")
        elif self.dfs_duration > 0.001:
            print(f"\nDFS Duration: {self.dfs_duration*1000:.2f} milliseconds")
        else:
            print(f"\nDFS Duration: {self.dfs_duration*1000000:.2f} microseconds")

    def _dfs_recursive(self, node, word_memory, level, pbar=None):
        if node is None:
            return

        if level > 0:
            word_memory += node.data

        if (
            level >= 3 and word_memory[-1] == word_memory[-2] == word_memory[-3]
        ):  # 1st optimization: if there are 3 consecutive same letters in the word then skip the word - ToDO: add more optimizations if possible
            if pbar is not None:
                pbar.update(self.count_nodes(node))
            return
        elif (
            self.required_letter in word_memory
            and self.min_length <= level <= self.max_length
        ):
            index = binary_search(word_memory)
            if index != -1:
                self.found_words.append((word_memory, level, index))

        if pbar is not None:
            pbar.update(1)

        for child in node.children:
            self._dfs_recursive(child, word_memory, level + 1, pbar)

    def dfs_parallel(self, show=False):
        processes_num = len(self.root.children)
        cores_num = multiprocessing.cpu_count()
        if processes_num > cores_num:
            processes_num = cores_num

        pool = multiprocessing.Pool(processes_num)

        partial_dfs_recursive = partial(
            _dfs_recursive_parallel,
            word_memory="",
            level=1,
            required_letter=self.required_letter,
            min_length=self.min_length,
            max_length=self.max_length,
        )

        with tqdm(
            total=processes_num, desc="Parallel DFS Progress"
        ) as pbar:  # progress bar updates after each process is completed - ToDO: update progress bar after each node is completed
            results = []
            for result in pool.imap(partial_dfs_recursive, self.root.children):
                results.append(result)
                pbar.update(1)

        self.dfs_duration = pbar.format_dict["elapsed"]

        for found_words in results:
            self.found_words.extend(found_words)

        pool.close()
        pool.join()

        if show:
            print(f"\nFound {len(self.found_words)} words:\n")
            for word, level, index in self.found_words:
                print(f"Word: {word}, Level: {level}, Index: {index+1}")
        else:
            print(f"\nFound {len(self.found_words)} words")

        if self.dfs_duration > 60:
            print(f"\nParallel DFS Duration: {self.dfs_duration/60:.2f} minutes")
        elif self.dfs_duration > 1:
            print(f"\nParallel DFS Duration: {self.dfs_duration:.2f} seconds")
        elif self.dfs_duration > 0.001:
            print(f"\nParallel DFS Duration: {self.dfs_duration*1000:.2f} milliseconds")
        else:
            print(
                f"\nParallel DFS Duration: {self.dfs_duration*1000000:.2f} microseconds"
            )


def _dfs_recursive_parallel(
    node, word_memory, level, required_letter, min_length, max_length
):
    memory_tree = Words([], required_letter, min_length, max_length)
    memory_tree._dfs_recursive(node, word_memory, level)

    return memory_tree.found_words


if __name__ == "__main__":
    # from letters import letters, letter
    # input_letters = letters[0]
    # required_letter = letter[0]

    # Input letters, required letter, minimum word length, and maximum word length
    input_letters = ["d", "o", "r", "s", "e", "t", "y"]  # 7 letters is default
    required_letter = "y"  # Letter that must be included in the word
    min_word_length = 4  # Minimum word length, default is 4
    max_word_length = 5  # Maximum word length

    word_tree = Words(input_letters, required_letter, min_word_length, max_word_length)
    word_tree.build_tree()
    # word_tree.display_tree(word_tree.root)
    # word_tree.dfs()  # Maximum word length: 5 - 27 seconds (19608 nodes), 6 - 4 minutes (137257 nodes), 7 - 29 minutes (960800 nodes)
    word_tree.dfs_parallel()  # Maximum word length: 5 - 13 seconds (19608 nodes), 6 - 2 minutes (137257 nodes), 7 - 20 minutes (960800 nodes) [parallelization on 7 cores - each letter is a separate process]
    word_tree.save_to_csv()

    # Times before optimization

    # optimization: if level >= 3 and word_memory[-1] == word_memory[-2] == word_memory[-3] and dictionary change to Answers.txt (dictionary change is only SpellBee optimization)
    # dfs() - max_word_length: 5 takes - 1 minute, 6 - 7 minutes, 7 - 50 minutes
