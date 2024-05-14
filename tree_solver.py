import time
import csv


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


class TreeNode:
    def __init__(self, letter, word=""):
        self.letter = letter
        self.word = word
        self.word += self.letter
        self.children = []

    def __str__(self):
        return self.word

    def add_child(self, node):
        self.children.append(node)

    def delete_child(self, node):
        self.children.remove(node)

    def delete_children(self):
        self.children = []

    def build_tree(self, letters, length, word="", depth=0):
        if depth >= length:
            return 0

        if depth > 0:
            word = self.word
            # print(depth, word)

        count = 0
        for letter in letters:
            self.children.append(TreeNode(letter, word))
            count += 1

        for child in self.children:
            count += child.build_tree(letters, length, word, depth + 1)

        return count

    # def dfs(self, node):
    #     if node is None:
    #         return

    #     for child in node.children:
    #         self.dfs(child)


class WordsTree:
    def __init__(
        self, letters, required_letter, min_length, max_length, dictionary_path
    ):
        start = time.time()

        self.letters = sorted(letters)
        self.required_letter = required_letter
        self.min_length = min_length
        self.max_length = max_length

        tree_start = time.time()
        self.root = TreeNode("root")
        self.node_count = self.root.build_tree(self.letters, max_length)
        tree_end = time.time()
        self.tree_build_duration = tree_end - tree_start

        self.dictionary = self.load_dictionary(dictionary_path)
        self.prefixes = self.get_prefixes()

        dfs_start = time.time()
        self.found_words = []
        self.dfs(self.root)
        dfs_end = time.time()
        self.dfs_duration = dfs_end - dfs_start

        end = time.time()
        self.duration = end - start

    def load_dictionary(self, file_path):
        with open(file_path, "r") as file:
            dictionary = file.readlines()

        return dictionary

    def get_prefixes(self, prefix_length=2):
        prefixes = set()

        for word in self.dictionary:
            if len(word) >= prefix_length:
                prefix = word[:prefix_length]
                prefixes.add(prefix)

        return prefixes

    def dfs(self, node, prev_found=False, depth=0):
        if node is None:
            return

        if depth > 0:
            pass

        if depth == 2:
            if not any(node.word.startswith(prefix) for prefix in self.prefixes):
                return

        if depth >= 3 and node.word[-1] == node.word[-2] == node.word[-3]:
            return

        if (
            self.required_letter in node.word
            and self.min_length <= len(node.word) <= self.max_length
        ):
            index, match = binary_search(node.word, self.dictionary, prev_found)
            if prev_found:
                prev_found = False
                if index == -1:
                    return
                elif match:
                    self.found_words.append((node.word, depth, index))
                    prev_found = True
            elif match and index != -1:
                self.found_words.append((node.word, depth, index))
                prev_found = True

        for child in node.children:
            self.dfs(child, prev_found, depth + 1)

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

    def display_branch(self, node, level=0):
        if node is not None:
            if level == 0:
                print(node.letter)
                for child in node.children:
                    self.display_branch(child, level + 1)
            elif node.letter == self.letters[-1]:
                print("  " * level + "└─" + node.letter + "  " + node.word)
                for child in node.children:
                    self.display_branch(child, level + 1)
            else:
                print("  " * level + "├─" + node.letter + "  " + node.word)
                for child in node.children:
                    self.display_branch(child, level + 1)

    def display_tree(self, decimals=2, words=False, tree=False):
        print("\nTree solver results:")
        print("\nLetters:", self.letters)
        print("Required letter:", self.required_letter)
        print("Minimum word length:", self.min_length)
        print("Maximum word length:", self.max_length)
        print("\nFound", len(self.prefixes), "prefixes")
        print("\nCreated tree with", self.node_count - 1, "nodes")

        if words:
            print(f"\nFound {len(self.found_words)} words:\n")
            for word, level, index in self.found_words:
                print(f"Word: {word}, Level: {level}, Index: {index+1}")
        else:
            print(f"\nFound {len(self.found_words)} words")

        print(
            f"\nTree build completed in: {self.format_time(self.tree_build_duration, decimals)}"
        )
        print(f"DFS completed in: {self.format_time(self.dfs_duration, decimals)}")
        print(
            f"Class initialization completed in: {self.format_time(self.duration, decimals)}\n"
        )

        if tree:
            print("\nTree structure:\n")
            self.display_branch(self.root)

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

    wordsTree = WordsTree(input_letters, required_letter, min_word_length, max_word_length, "Answers.txt")
    wordsTree.display_tree(2, tree=False)
    # wordsTree.save_to_csv()

    # Binary search test
    # with open("Answers.txt", "r") as file:
    #         dictionary = file.readlines()
    # print(binary_search("eyeso", dictionary, True))
