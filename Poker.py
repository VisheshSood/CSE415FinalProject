from Card import  *

POT_SIZE = 0
PLAYER_BALANCE = 100
BOT_BALANCE = 100

WHOSE_TURN = 0

def intro():
    print('Welcome to Poker. The cards are being dealt!\n')

def askStand():
    return input('What would you like to do? (S)tand, (F)old, (R)aise: \n').upper()

def askCall():
    return input('What would you like to do? (C)all, (F)old, (R)aise: \n').upper()

def printPlayerDetails(playerHand, otherHand):
    print('Pot Size: ' + str(POT_SIZE))

    print('Your Hand: ' + str(playerHand).strip() + ', Balance: ' + str(PLAYER_BALANCE))
    print('Bot Hand: Blank Blank, Balance: ' + str(BOT_BALANCE))

def callBot():



def game():
    global POT_SIZE
    global PLAYER_BALANCE
    global BOT_BALANCE
    deck = Deck()
    deck.shuffle()

    playerHand = Hand()
    botHand = Hand()

    deck.move_cards(playerHand, 2)
    deck.move_cards(botHand, 2)

    printPlayerDetails(playerHand, None)
    print('Your Turn!\n')
    choice = askStand()
    if (choice == 'R'):
        value = int(input('You have chosen to raise. How much would you like to raise?\n'))
        while (value > PLAYER_BALANCE):
            value = int(input('You do not have that much, lower your bet. How much would you like to raise?\n'))

        POT_SIZE += value
        PLAYER_BALANCE -= value
        print('You have raised by ' + str(value))
    if (choice == 'S'):
        print('You have chosen to stand. \n')


    printPlayerDetails(playerHand, None)
    print('Bot\'s Turn!\n')
    callBot()

intro()
game()