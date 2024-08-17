import time
import secrets

feeling_brave = True

ghost = r'''

            .--,
           /  (
          /    \
         /      \\ 
        /  0  0  \
((()   |    ()    |   ()))
\\  ()  (  .____.  )  ()  /
 |` \\_/ \\  `""`  / \\_/ `|
 |       `.'--'.`       |
  \\        `""`        /
   \\                  /
    `.              .'    ,
     |`             |  _.'|
     |              `-'  /
     \\                 .'
      `.____________.-'

'''


game_over= '''


  ▄████  ▄▄▄       ███▄ ▄███▓▓█████     ▒█████   ██▒   █▓▓█████  ██▀███  
 ██▒ ▀█▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀    ▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒
▒██░▄▄▄░▒██  ▀█▄  ▓██    ▓██░▒███      ▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒
░▓█  ██▓░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄    ▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  
░▒▓███▀▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒   ░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒
 ░▒   ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░   ░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░
  ░   ░   ▒   ▒▒ ░░  ░      ░ ░ ░  ░     ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░
░ ░   ░   ░   ▒   ░      ░      ░      ░ ░ ░ ▒       ░░     ░     ░░   ░ 
      ░       ░  ░       ░      ░  ░       ░ ░        ░     ░  ░   ░     
                                                     ░                   


'''

count = 0 

while feeling_brave:

    print('You are walking down a corridor...')
    time.sleep(1)
    print('You hear noises behind a door')
    time.sleep(1.5)
    user_input = int(input('Enter a door if you dare....'))

    ghost_num = secrets.SystemRandom().randint(1,3)

    if ghost_num == user_input:
        print(ghost)
        time.sleep(2)
        print(game_over)
        feeling_brave = False

    else:
        print('YOu made it to the next level >:)')

    count += 1 

print(f'You made to level {count}')


#%%
