# SpellBee.com solver (can be used for other word games as well - game dictionary required for search [Answers.txt - SpellBee dictionary, 39k words])
# Tested with minimal word length of 4 on:
# AMD Ryzen 7 5800H
# 8 cores, 16 threads at 3.2GHz

import csv
import time


class WordFinder:
    def __init__(
        self, letters, required_letter, min_length, max_length, file_path="Answers.txt"
    ):
        self.letters = sorted(letters)
        self.required_letter = required_letter
        self.min_length = min_length
        self.max_length = max_length
        self.words = self.load_words(file_path)
        self.search_duration = 0  # Initialize search duration attribute
        self.boundaries = self.find_boundaries(self.letters)
        self.found_words = []

    def load_words(self, file_path):
        with open(file_path, "r") as file:
            words = file.readlines()

        return words

    def find_boundaries(self, letters):
        start_time = time.time()
        boundaries = []

        for letter in letters:
            low = self.binary_search(letter)
            high = self.binary_search(letter, high_boundary=True)
            boundaries.append((low, high))

        end_time = time.time()
        self.search_duration += end_time - start_time

        return boundaries

    def find_words(self):
        found_words = []

        start_time = time.time()

        for low, high in self.boundaries:
            for index in range(low, high + 1):
                word = self.words[index].strip()
                if (
                    self.required_letter in word
                    and all(letter in self.letters for letter in word)
                    and self.min_length <= len(word) <= self.max_length
                ):
                    found_words.append((word, index))

        end_time = time.time()
        self.search_duration += end_time - start_time

    def binary_search(self, letter, high_boundary=False):
        low = 0
        high = len(self.words) - 1
        result = -1

        start_time = time.time()

        while low <= high:
            mid = (low + high) // 2
            word = self.words[mid].strip()
            if word[0] < letter:
                low = mid + 1
            elif word[0] > letter:
                high = mid - 1
            else:
                result = mid
                if high_boundary:
                    low = mid + 1
                else:
                    high = mid - 1

        end_time = time.time()
        self.search_duration += end_time - start_time

        return result

    def find_words(self):
        start_time = time.time()

        for low, high in self.boundaries:
            for index in range(low, high + 1):
                word = self.words[index].strip()
                if (
                    self.required_letter in word
                    and all(letter in self.letters for letter in word)
                    and self.min_length <= len(word) <= self.max_length
                ):
                    self.found_words.append((word, index))

        end_time = time.time()
        self.search_duration += end_time - start_time

    def display_words(self, show=False):
        if self.found_words:
            if show:
                print(f"\nFound {len(self.found_words)} words:\n")
                for word, index in self.found_words:
                    print(f"Word: {word}, Index: {index+1}")
            else:
                print(f"\nFound {len(self.found_words)} words.")
        else:
            print(
                f"\nNo word contains '{self.required_letter}' or meets the length criteria."
            )

        if self.search_duration > 1:
            print(f"\nDictionary search duration: {self.search_duration:.2f} seconds")
        elif self.search_duration > 0.001:
            print(
                f"\nDictionary search duration: {self.search_duration*1000:.2f} milliseconds"
            )
        else:
            print(
                f"\nDictionary search duration: {self.search_duration*1000000:.2f} microseconds"
            )

    def save_to_csv(self, file_path=None):
        if file_path is None:
            duration = self.search_duration
            if duration > 60:
                duration = f"{duration/60:.2f}min"
            elif duration > 1:
                duration = f"{duration:.2f}sec"
            elif duration > 0.001:
                duration = f"{duration*1000:.2f}ms"
            else:
                duration = f"{duration*1000000:.2f}µs"

            file_name = f"{''.join(self.letters)}-{self.required_letter}-dictionary-{self.min_length}-{self.max_length}-{duration}.csv"
            file_path = file_name

        with open(file_path, "w", newline="") as csvfile:
            fieldnames = ["Word", "Index"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for word, index in self.found_words:
                writer.writerow({"Word": word, "Index": index})

        print(f"\nCSV file saved as: {file_path}\n")


if __name__ == "__main__":
    # from letters import letters, letter
    # input_letters = letters[0]
    # required_letter = letter[0]

    # Input letters, required letter, minimum word length, and maximum word length
    input_letters = ["d", "o", "r", "s", "e", "t", "y"]  # 7 letters is default
    required_letter = "y"  # Letter that must be included in the word
    min_word_length = 4  # Minimum word length, default is 4
    max_word_length = 5  # Maximum word length

    words = WordFinder(input_letters, required_letter, min_word_length, max_word_length)
    words.find_words()
    words.display_words(True)
    words.save_to_csv()
