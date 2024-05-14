import csv
import time


def binary_search(letter, lines, high_boundary=False):
    low = 0
    high = len(lines) - 1
    result = -1

    while low <= high:
        mid = (low + high) // 2
        current_word = lines[mid].strip()

        if current_word[0] < letter:
            low = mid + 1
        elif current_word[0] > letter:
            high = mid - 1
        else:
            result = mid
            if high_boundary:
                low = mid + 1
            else:
                high = mid - 1

    return result


class WordsDictionary:
    def __init__(
        self, letters, required_letter, min_length, max_length, dictionary_path
    ):
        start = time.time()

        self.letters = sorted(letters)
        self.required_letter = required_letter
        self.min_length = min_length
        self.max_length = max_length

        self.dictionary = self.load_dictionary(dictionary_path)
        self.boundaries = self.find_boundaries(self.letters)

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

    def find_boundaries(self, letters):
        boundaries = []

        for letter in letters:
            low = binary_search(letter, self.dictionary)
            high = binary_search(letter, self.dictionary, high_boundary=True)
            boundaries.append((low, high))

        return boundaries

    def find_words(self):
        for low, high in self.boundaries:
            for index in range(low, high + 1):
                word = self.dictionary[index].strip()
                if (
                    self.required_letter in word
                    and all(letter in self.letters for letter in word)
                    and self.min_length <= len(word) <= self.max_length
                ):
                    self.found_words.append((word, index))

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

    def display_dictionary(self, decimals=2, words=False):
        print("\nDictionary solver results:")

        if words:
            print(f"\nFound {len(self.found_words)} words:\n")
            for word, index in self.found_words:
                print(f"Word: {word}, Index: {index+1}")
        else:
            print(f"\nFound {len(self.found_words)} words")

        print(
            f"\nSearch completed in: {self.format_time(self.search_duration, decimals)}"
        )
        print(
            f"Class initialization completed in: {self.format_time(self.duration, decimals)}\n"
        )

    def save_to_csv(self, file_path=None):
        if file_path is None:
            file_name = f"dictionary-{''.join(self.letters)}-{self.required_letter}-{self.min_length}-{self.max_length}-{self.format_time(self.search_duration)}.csv"
            file_path = file_name

        with open(file_path, "w", newline="") as csvfile:
            fieldnames = ["Word", "Index"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for word, index in self.found_words:
                writer.writerow({"Word": word, "Index": index})

        print(f"CSV file saved as: {file_path}\n")


if __name__ == "__main__":
    input_letters = ["a", "p", "t", "i", "y", "l", "c"]
    required_letter = "c"
    min_word_length = 4
    max_word_length = 6

    words = WordsDictionary(
        input_letters, required_letter, min_word_length, max_word_length, "Answers.txt"
    )
    words.display_dictionary(2, words=False)
    # words.save_to_csv()
