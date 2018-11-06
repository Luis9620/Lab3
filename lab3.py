from AVL import Node
from AVL import AVLTree
from RBTree import RedBlackTree

count = 0


def display_menu(words_list, my_words_list):
    global count
    menu = {}
    menu['1'] = "AVL-Tree"
    menu['2'] = "RB-Tree"
    menu['3'] = "Exit"
    while True:
        options = menu.keys()

        for entry in options:
            print(entry, ".- ", menu[entry])
        selection = input("Please Select:")
        if selection == '1':
            print("Loading...Please wait")
            AVL_tree_words = avl_tree(words_list)
            max_anagram(my_words_list, AVL_tree_words)
            while True:
                word = str(input("Enter a word(press 0 to go back to menu):")).lower()
                selection = word
                if selection == '0':
                    break
                if AVL_tree_words.search(word) != True:
                    print("Invalid word. Try again!")
                else:
                    count_anagrams(word, AVL_tree_words)
                    print("Word: " + word + " Anagrams: " + str(count))
                    count = 0
        elif selection == '2':
            print("Loading...Please wait")
            RB_tree_words = red_black_tree(words_list)
            max_anagram(my_words_list, RB_tree_words)
            while True:
                word = input("Enter a word(press 0 to go back to menu):")
                word = str(word).lower()
                selection = word
                if selection == '0':
                    break
                if RB_tree_words.search(word) != True:
                    print("Invalid word. Try again!")
                else:
                    count_anagrams(word, RB_tree_words)
                    print("Word: " + word + " Anagrams: " + str(count))
                    count = 0
        elif selection == '3':
            print("Bye")
            break
        else:
            print("Unknown Option Selected!")

def avl_tree(words_list):
    tree = AVLTree()
    for i in range(len(words_list)):
        tree.insert(Node(words_list[i].lower()))
    return tree


def red_black_tree(words_list):
    tree = RedBlackTree()
    for i in range(len(words_list)):
        tree.insert(words_list[i].lower())
    return tree


def print_anagrams(word,words, prefix=""):
    if len(word) <= 1:
        str = prefix + word
    if str in words:
        print(prefix + word)
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]  # letters before cur
            after = word[i + 1:]  # letters after cur
            if cur not in before:  # Check if permutations of cur have not been generated.
                print_anagrams(before + after, prefix + cur)


def count_anagrams(word, tree, prefix=""):
    global count
    if len(word) <= 1:
        if tree.search(prefix + word) == True:
            count += 1
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]  # letters before cur
            after = word[i + 1:]  # letters after cur
            if cur not in before:  # Check if permutations of cur have not been generated.
                count_anagrams(before + after, tree, prefix + cur)


def max_anagram(words_list, tree):
    max_anagram_number = 0
    max_anagram_word = ""

    global count
    for i in range(len(words_list)):
        count_anagrams(words_list[i], tree)
        if max_anagram_number < count:
            max_anagram_number = count
            max_anagram_word = words_list[i]
        count = 0
    print("Word with most anagrams: " + max_anagram_word + " Anagrams: " + str(max_anagram_number))


def main():
    words_file = open("words.txt", "r")
    words_list = words_file.read().split("\n")
    my_words_file = open("my_words.txt", "r")
    my_words_list = my_words_file.read().split("\n")

    display_menu(words_list, my_words_list)



main()