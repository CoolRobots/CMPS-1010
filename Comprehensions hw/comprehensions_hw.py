#This file contains the first homework assignment, about lists, strings, and comprehensions.
#You must rename this file as comprehensions_hw.py for the tests and autograder.

def problem_1()->str:
    '''Problem 1: Goal: Capitalize the zeroth letter of each word.
        Step 1: Use the split function to create a list of the words in the initial string.
        Step 2: Use a list comprehension, string addition, and the .captalize() function to capitalize the zeroth letter of each word.
        Step 3: Use the join function to recombine the words into a string.'''
    initial_string:str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    #TODO: follow the steps to complete this function. Your final answer should be stored in the variable string_with_each_word_captalized.
    split_words = initial_string.split()
    capped_words = []
    for word in split_words:
       capped_words.append(word.capitalize())
    string_with_each_word_captalized = " ".join(capped_words)

    return(string_with_each_word_captalized)
def problem_2()->str:
    '''
    Problem 2: Goal: Get every-other letter of the last sentence
        Step 1: Use the split function to get a list of sentences.
        Step 2: Use list slicing to get the last sentence. (keep in mind there will be an empty sentence at the end of the list from Step 1, due to the last period.)
        Step 3: Remove the space at the beginning of the last sentence (so the 0th character is a letter.)
        Step 4: Use string slicing to get the even-indexed characters of the last sentence
    '''
    initial_string : str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    split_sentences = initial_string.split(".")
    last_sentence = split_sentences[-2]
    last_sentence_no_space = last_sentence[1:]
    even_letters_of_last_sentence=last_sentence_no_space[::2]
    return even_letters_of_last_sentence
def problem_3()->dict:
    '''
    Problem 3: Goal: Create a dictionary whose keys are the characters of the sentence. The values are the number of occurences of the character in the initial_string.
        Step 1: Use a dictionary comprehension to create a dictionary whose values are the characters in initial_string.
            Step 1.5 Use the len function and a list comprehension to determine the number of times each character occurs.
        Note: Capital letters should be considered different from their lowercase counterparts.
        Note: a 1-line solution is intended.
    '''
    initial_string : str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    #TODO: follow the steps to complete this function. Your final answer should be stored in the variable dict_of_letter_frequencies.
    dict = {}
    for char in initial_string:
        dict.update({char:dict.get(char,0)+1})
    return dict