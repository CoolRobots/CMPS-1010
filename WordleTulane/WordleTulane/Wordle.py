#Tulane University, CMPS 1100, Fall 2025
#
#STUDENTS MUST FILL IN BELOW
#
#Student name: Jackson Bethune
#Student email address: Jbethune1@Tulane.edu

import random
from WordleWordlist import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_ROWS, N_COLS
from WordleGraphics import CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR
def enter_action(guessedword):
    if guessedword.casefold() in FIVE_LETTER_WORDS:
        index=0
        row=gw.get_current_row()
        blacklistLets=[]
        for let in guessedword.casefold():
            if let in solution:
                if let == solution[index]:
                    gw.set_square_color(row, index, CORRECT_COLOR)
                    gw.set_key_color(let.upper(), CORRECT_COLOR)
                else:
                    if let in blacklistLets:
                        gw.set_square_color(row, index, MISSING_COLOR)
                    else:
                        gw.set_square_color(row, index, PRESENT_COLOR)
                        if  gw.get_key_color(let.upper())!= CORRECT_COLOR:
                            gw.set_key_color(let.upper(), PRESENT_COLOR)

                        if solution.count(let)==1:
                            blacklistLets.append(let)
            else:
                gw.set_square_color(row, index, MISSING_COLOR)
                if gw.get_key_color(let.upper())!= PRESENT_COLOR and gw.get_key_color(let.upper())!= CORRECT_COLOR:
                    gw.set_key_color(let.upper(), MISSING_COLOR)
            index+=1

        ## Go to next step
        if(guessedword.casefold()==solution):
             gw.show_message("You Win!!!!")
        elif(gw.get_current_row==5):
            gw.show_message("You lose :C")
        else:
            gw.set_current_row(gw.get_current_row()+1)
    else:
        gw.show_message("Not in word list")
    

# Below: chose a random word from the wordlist
solution=random.choice(FIVE_LETTER_WORDS)

# Students: do not change anything below here
gw = WordleGWindow()
gw.add_enter_listener(enter_action)
