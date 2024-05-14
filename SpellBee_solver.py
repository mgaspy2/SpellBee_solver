# SpellBee.com solver (can be used for other word games as well - suitable dictionary required for validation [AllWords.txt - 60k words, Answers.txt - 39k words])

from tree_solver import WordsTree
from dictionary_solver import WordsDictionary


class SpellBeeSolver:
    def __init__(
        self, letters, required_letter, min_length, max_length, dictionary_path="Answers.txt",
    ):
        self.letters = letters
        self.required_letter = required_letter
        self.min_length = min_length
        self.max_length = max_length
        self.dictionary_path = dictionary_path

    def solve(self, method="tree"):
        if method == "tree":
            solver = WordsTree(
                self.letters,
                self.required_letter,
                self.min_length,
                self.max_length,
                self.dictionary_path,
            )
            solver.display_tree(2, True)
        elif method == "dictionary":
            solver = WordsDictionary(
                self.letters,
                self.required_letter,
                self.min_length,
                self.max_length,
                self.dictionary_path,
            )
            solver.display_dictionary(2, True)
        else:
            raise ValueError("Invalid method. Choose 'tree' or 'dictionary'.")

        return solver

    def save_to_csv(self, method="tree", file_name="results.csv"):
        solver = self.solve(method)
        solver.save_to_csv(file_name)


if __name__ == "__main__":
    # Input letters, required letter, minimum word length, and maximum word length
    input_letters = ["a", "p", "t", "i", "y", "l", "c"]  # 7 letters is default
    required_letter = "c"  # Letter that must be included in the word
    min_word_length = 4  # Minimum word length, default is 4
    max_word_length = 5  # Maximum word length

    spellbee = SpellBeeSolver(
        input_letters, required_letter, min_word_length, max_word_length
    )
    spellbee.solve("tree")
