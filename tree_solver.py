import time
import csv
from itertools import permutations


def binary_search(word, dictionary, word_base=False):
    low = 0
    high = len(dictionary) - 1
    index = -1

    while low <= high:
        mid = (low + high) // 2
        current_word = dictionary[mid].strip()

        if word_base and current_word.startswith(word):
            if word == current_word:
                return mid, True
            else:
                index = mid
        elif word == current_word:
            return mid, True

        if current_word < word:
            low = mid + 1
        else:
            high = mid - 1

    return index, False


class WordsTree:
    def __init__(
        self, letters, required_letter, min_length, max_length, dictionary_path
    ):
        start = time.time()

        self.letters = sorted(letters)
        self.required_letter = required_letter
        self.min_length = min_length
        self.max_length = max_length

        self.dictionary = self.load_dictionary(dictionary_path)
        prefix_start = time.time()
        self.prefixes, self.prefix_length = self.get_prefixes()
        prefix_end = time.time()
        self.prefix_duration = prefix_end - prefix_start

        dfs_start = time.time()
        self.words = []
        self.nodes_count = self.dfs()
        dfs_end = time.time()
        self.dfs_duration = dfs_end - dfs_start

        search_start = time.time()
        self.found_words = []
        self.find_words()
        search_end = time.time()
        self.search_duration = search_end - search_start

        end = time.time()
        self.duration = end - start

    def load_dictionary(self, file_path):
        with open(file_path, "r") as file:
            dictionary = file.readlines()

        return dictionary

    def get_prefixes(self, prefix_length=2):
        prefixes = set()

        all_prefixes = permutations(self.letters, prefix_length)
        all_prefixes = ["".join(prefix) for prefix in all_prefixes]
        for prefix in all_prefixes:
            index, _ = binary_search(prefix, self.dictionary, word_base=True)
            if index == -1:
                prefixes.add(prefix)

        return prefixes, prefix_length

    def dfs(self, word="", depth=0):
        if depth == self.prefix_length:
            if any(
                word.startswith(prefix) for prefix in self.prefixes
            ):  # Prefix check - unfair in terms of time measurement as it accesses the dictionary before a words are generated, biasing the word generation process.
                return 0

        if depth >= 3 and word[-1] == word[-2] == word[-3]:
            return 0

        if (
            self.required_letter in word
            and self.min_length <= len(word) <= self.max_length
        ):
            self.words.append(word)

        if depth >= self.max_length:
            return 0

        count = 0
        for letter in self.letters:
            count += self.dfs(word + letter, depth + 1)
            count += 1

        return count

    def find_words(self):
        for word in self.words:
            index, match = binary_search(word, self.dictionary)
            if index != -1 and match:
                self.found_words.append((word, len(word), index))

    def format_time(self, duration, decimals=2):
        formatted_time = duration

        if formatted_time > 60:
            formatted_time = f"{formatted_time/60:.{decimals}f}min"
        elif formatted_time > 1:
            formatted_time = f"{formatted_time:.{decimals}f}sec"
        elif formatted_time > 0.001:
            formatted_time = f"{formatted_time*1000:.{decimals}f}ms"
        else:
            formatted_time = f"{formatted_time*1000000:.{decimals}f}us"

        return formatted_time

    def display_tree(self, decimals=2, words=False):
        print("\nTree solver results:")
        print("\nFound", len(self.prefixes), "forbidden prefixes")
        print("\nCreated tree with", self.nodes_count - 1, "nodes")

        if words:
            print(f"\nFound {len(self.found_words)} words:\n")
            for word, level, index in self.found_words:
                print(f"Word: {word}, Level: {level}, Index: {index+1}")
        else:
            print(f"\nFound {len(self.found_words)} words")

        print(f"\n|   Prefixes:   {self.format_time(self.prefix_duration, decimals)}")
        print(f"|  Word tree:   {self.format_time(self.dfs_duration, decimals)}")
        print(f"|     Search:   {self.format_time(self.search_duration, decimals)}")
        print(f"|     Solver:   {self.format_time(self.duration, decimals)}\n")

    def save_to_csv(self, file_path=None):
        if file_path is None:
            file_name = f"tree-{''.join(self.letters)}-{self.required_letter}-{self.min_length}-{self.max_length}-{self.format_time(self.dfs_duration)}.csv"
            file_path = file_name

        with open(file_path, "w", newline="") as csvfile:
            fieldnames = ["Word", "Depth", "Index"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for word, level, index in self.found_words:
                writer.writerow({"Word": word, "Depth": level, "Index": index})

        print(f"CSV file saved as: {file_path}\n")


if __name__ == "__main__":
    input_letters = ["a", "p", "t", "i", "y", "l", "c"]
    required_letter = "c"
    min_word_length = 4
    max_word_length = 6

    wordsTree = WordsTree(
        input_letters, required_letter, min_word_length, max_word_length, "Answers.txt"
    )
    wordsTree.display_tree(2, words=False)
    # wordsTree.save_to_csv()

    # Binary search test

    # for word in wordsTree.words:
    #     index, match = binary_search(word, wordsTree.dictionary)
    #     if match:
    #         print(index)

    # print(binary_search("aacd", wordsTree.words))

    # with open("Answers.txt", "r") as file:
    #         dictionary = file.readlines()
    # print(binary_search("eyeso", dictionary, True))

    # all_prefixes = permutations(input_letters, 2)
    # all_prefixes = [''.join(prefix) for prefix in all_prefixes]
    # for prefix in all_prefixes:
    #     print(prefix, prefix in dictionary)
