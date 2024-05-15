# SpellBee.com solver (can be used for other word games as well - suitable dictionary required for validation [AllWords.txt - 60k words, Answers.txt - 39k words])

from tree_solver import WordsTree
from dictionary_solver import WordsDictionary


class SpellBeeSolver:
    def __init__(
        self,
        letters,
        required_letter,
        min_length,
        max_length,
        dictionary_path="Answers.txt",
    ):
        self.letters = letters
        self.required_letter = required_letter
        self.min_length = min_length
        self.max_length = max_length
        self.dictionary_path = dictionary_path

    def solve(self, method="vs", save=False):
        print("\n         Letters:", self.letters)
        print(" Required letter:", self.required_letter)
        print("Min. word length:", self.min_length)
        print("Max. word length:", self.max_length)

        if method == "tree":
            solver = WordsTree(
                self.letters,
                self.required_letter,
                self.min_length,
                self.max_length,
                self.dictionary_path,
            )
            solver.display_tree(2, True)
            if save:
                solver.save_to_csv("results.csv")
        elif method == "dictionary":
            solver = WordsDictionary(
                self.letters,
                self.required_letter,
                self.min_length,
                self.max_length,
                self.dictionary_path,
            )
            solver.display_dictionary(2, True)
            if save:
                solver.save_to_csv("results.csv")
        elif method == "vs":
            tree = WordsTree(
                self.letters,
                self.required_letter,
                self.min_length,
                self.max_length,
                self.dictionary_path,
            )
            dictionary = WordsDictionary(
                self.letters,
                self.required_letter,
                self.min_length,
                self.max_length,
                self.dictionary_path,
            )
            print("")
            print(
                "Tree       | Found words: "
                + str(len(tree.found_words))
                + " | Search: "
                + tree.format_time(tree.search_duration)
                + " | Tree build: "
                + tree.format_time(tree.dfs_duration)
                + " | Nodes: "
                + str(tree.nodes_count)
            )
            print(
                "Dictionary | Found words: "
                + str(len(dictionary.found_words))
                + " | Search: "
                + dictionary.format_time(dictionary.search_duration)
                + "\n"
            )
            if save:
                tree.save_to_csv("tree_results.csv")
                dictionary.save_to_csv("dictionary_results.csv")
        else:
            raise ValueError("Invalid method. Choose 'tree', 'dictionary' or 'vs'!")

    def save_to_csv(self, method="tree", file_name="results.csv"):
        solver = self.solve(method)
        solver.save_to_csv(file_name)


if __name__ == "__main__":
    # Input letters, required letter, minimum word length, and maximum word length
    input_letters = ["a", "p", "t", "i", "y", "l", "c"]  # 7 letters is default
    required_letter = "c"  # Letter that must be included in the word
    min_word_length = 4  # Minimum word length, default is 4
    max_word_length = 7  # Maximum word length

    spellbee = SpellBeeSolver(
        input_letters, required_letter, min_word_length, max_word_length
    )
    spellbee.solve()
