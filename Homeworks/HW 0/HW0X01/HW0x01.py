#import modules 
import random  

#define main function 
def main():

    #always start at state 0 
    state = 0
    
    #run a continuous loop 
    while(True):

        #s0 start the game 
        if state == 0:
            
            #variables only to be initiated on the first round
            wins = 0 
            losses = 0
            rows = 12
            cols = 4

            #print starting messages 
            welcome = "Welcome to the game of Mastermind!"
            start_msg = "You will be the codebreaker. Try to break the secret code\nby entering 4-digit codes using the numbers 0-5. Your\nguesses will be marked with a (+) symbol for each correct value\nin the correct location and a (-) for each correct value \nn an incorrect location."
            start_promt = "Press enter to begin"
            print(welcome+"\n"+"\n"+start_msg+"\n")

            # Get user input
            user_input = input(start_promt)

            if user_input == "":
                state = 1
            else:
                continue 
       
        #s1 initialize variables 
        elif state == 1:
           
           #initialize variables 
            guess_num = 0
            game_won = ""
            code = []
            current_guess = []
            guesses = [[" " for _ in range(cols)] for _ in range(rows)]
            results = ["b" for _ in range(rows)]
            
            #always go to state 2 
            state = 2

                
        #s2 generate random code 
        elif state == 2: 
            
            for n in range(4):
                
                code.append(random.randint(0,5))

            state = 3
            
        #s3 print the grid 
        elif state == 3:
             
            #define grid strings 
            line = "+−−−+−−−+−−−+−−−+"
            left_blank = "| "    #print one of these 
            right_blank = "| "   #print four of these 
            header = "Code to break: "
            
            #first print the first lines
            print("\n")
            print(header, end="")
            for n in code:
                print(n, end="")
            print("\n") 
            print("wins: ", wins)
            print("losses: ", losses)

            #now print grid
            
            m = 0 #use variable to keep track of loop number 
            for row in guesses:
                
                print(line)
                print(left_blank,end="")
                
                for col in row:

                    print(col,right_blank,end="")
                    
                if results[m] != "b":  # Check if results[m] is not "b"
                    print(results[m])
                else:
                    print("")
                
                m = m + 1
                    
            print(line)
            
            #check if the game is over 
            if game_won == "True":
                print("You Win!")
                state = 6
            elif game_won == "False":
                print("You Loose!")
                state = 6
            else:
                state = 4
            
        #s4 process input 
        elif state == 4:
            
            # Get user input
            code_guess = input("Enter a guess: ")
            current_guess = []
            error = False
            
            #check if guess is a valid entry
            for char in code_guess:
                
                if len(code_guess) != 4:
                    print("Invalid Entry")
                    error = True 
                    break
                elif char.isdigit() == False:
                    print("Invalid Entry")
                    error = True
                    break
                elif int(char) > 5:
                    print("Invalid Entry")
                    error = True
                    break
                else:
                    current_guess.append(char)
            
            #if the guess is valid then store it in the guesses array 
            #i will be storing things in the array bottoms up
            if error == False:        
                guess_num = guess_num + 1
                guesses[rows-guess_num] = current_guess
                state = 5
            
            if error == True:
                state = 4
                
        #s5 check the guess to see what matches
        elif state == 5:
            
            #first check if there is a digit in the right place
            temp_result = ""
            code_copy = []
            guess_copy = []
            for n in range(len(code)):
                if int(current_guess[n]) == code[n]:
                    temp_result += "+"
                    code_copy.append("x")
                    guess_copy.append("y")
                else:
                    code_copy.append(str(code[n]))
                    guess_copy.append(current_guess[n])
                    
            #now check if its the right number in the wrong place
            code_set = set(code_copy)
            for num in guess_copy:
                if num in code_set:
                    temp_result += "-"

            results[rows-guess_num] = temp_result
            
            if temp_result == "++++":
                game_won = "True"
                wins = wins + 1
            elif guess_num == 12:
                game_won = "False"
                losses = losses + 1
            
            #always go back to the printing stage 
            state = 3
        
        #s6 play again? 
        elif state == 6:
            again_input = input("Play again? Enter (y) for yes: ")
            if again_input == "y":
                state = 1
            else:
                state = 0
            

main()

    

