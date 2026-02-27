#This homework focuses on lists and loops. I believe these are the most important concepts in Python.

#You may work together, but you must type your own code.
#You should only use LLMs if you get stuck. If you choose to consult an LLM, then ask the machine follow-up questions about its solution.

#Problem 1: The diamond of stars. 

#Important: You MUST rename this file as loops_hw.py for the autograder.

def diamond_of_stars(n:int)->None:
    '''Input: n is a nonnegative integer.
    Outputs: None
    SideEffect: prints a diamond of stars whose longest row contains n stars.
    For example, when n=3, we see this output: 
  *
 * *
* * *
 * *
  *
  Notes: Use spaces to align the stars. There should be a newline after the last star in each row.
    '''
    for i in range(1, n+1):
        spaces = " " * (n-i)
        stars = " ".join(["*"] * i)
        print(spaces+stars)

    for i in range(n-1, 0, -1):
        spaces = " " * (n-i)
        stars = " ".join(["*"] * i)
        print(spaces+stars)
    pass

#Problem 2: The weird sequence of numbers.

def weird_sequence(n:int)->list[bool]:
    '''input: n is a natural number.
    Outputs: A list of numbers continuing the pattern: 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300, ... and so forth.
    The list should NOT include 10^n, but end just before, at 9*10^(n-1)
    Specifically, I mean OEIS-A037124, available here: https://oeis.org/A037124
    For example, when n=2, the output is [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90]'''
    '''
    Hint: One solution is to use a doubly nested loop, appending the numbers one-by-one. 
    The exponent operator in python is expressed using **. For example, 100==10**2
    '''
    out=[]
    for e in range(0, n):
        for i in range(1, 10):
            out.append(i*(10**e))
    return out
    pass
#Problem 3: Count the number of repeated occurences of letters.

def count_double_letters(input_string: str) -> int:
    lastChar = ""
    count = 0

    for i in range(len(input_string)):
        if input_string[i] == lastChar:
            count += 1
        lastChar = input_string[i]

    return count