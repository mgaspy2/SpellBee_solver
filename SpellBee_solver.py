# SpellBee.com solver

import csv
from tqdm import tqdm
import time

def binary_search(word, file_path='AllWords.txt'):
    with open(file_path, 'r') as file:
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
            raise ValueError("Minimum word length cannot be greater than maximum word length.")

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
                    
    def dfs(self):
        start_time = time.time()
        total_nodes = self.count_nodes(self.root)
        with tqdm(total=total_nodes, desc="DFS Progress") as pbar:
            self._dfs_recursive(self.root, '', 0, pbar)
        end_time = time.time()
        self.dfs_duration = int((end_time - start_time) / 60)

        print("\nFound Words:\n")
        for word, level, index in self.found_words:
            print(f"Word: {word}, Level: {level}, Index: {index+1}")

    def _dfs_recursive(self, node, word_memory, level, pbar):
        if node is None:
            return

        if level > 0:
            word_memory += node.data

        if len(word_memory) >= 3 and word_memory[-1] == word_memory[-2] == word_memory[-3]:
            return
        elif self.required_letter in word_memory and self.min_length <= level <= self.max_length:
            index = binary_search(word_memory)
            if index != -1:
                self.found_words.append((word_memory, level, index))

        pbar.update(1)
        
        for child in node.children:
            self._dfs_recursive(child, word_memory, level + 1, pbar)

    @staticmethod
    def count_nodes(node):
        if node is None:
            return 0
        count = 1
        for child in node.children:
            count += Words.count_nodes(child)
        return count
 
    def save_to_csv(self, file_path=None):
        if file_path is None:
            file_name = f"{''.join(self.letters)}-{self.required_letter}-{self.min_length}-{self.max_length}-{self.dfs_duration}min.csv"
            file_path = file_name
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['Word', 'Level', 'Index']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for word, level, index in self.found_words:
                writer.writerow({'Word': word, 'Level': level, 'Index': index})

        print(f"\nCSV file saved as: {file_path}\n")

if __name__ == "__main__":
    from letters import letters, letter
    
    # Input letters, required letter, minimum word length, and maximum word length
    
    # input_letters = letters[0]
    # required_letter = letter[0]
    input_letters = ['d', 'o', 'r', 's', 'e', 't', 'y']  # 7 letters is recommended
    required_letter = 'y'  # Letter that must be included in the word
    min_word_length = 4  # Minimum word length, default is 4
    max_word_length = 7  # Maximum word length, 5 takes about 1 minute (19608 nodes), 6 takes about 7 minutes (137257 nodes), 7 takes about 50 minutes (960800 nodes) (tested on AMD Ryzen 7 5800H, before optimization on line 91)

    word_tree = Words(input_letters, required_letter, min_word_length, max_word_length)
    word_tree.build_tree()
    # word_tree.display_tree(word_tree.root)
    word_tree.dfs()
    word_tree.save_to_csv()
