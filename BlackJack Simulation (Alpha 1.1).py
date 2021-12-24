import random, itertools, os
from time import sleep
from tabulate import tabulate



class SetUp:
    '''Setting up the deck'''
    @classmethod
    def DeckSetUp(self):
        number_of_decks = 1 #number of decks used
        suits = ['hearts', 'diamonds', 'clubs', 'spades'] 
        ranks = ['2','3','4','5','6','7','8','9','10','jack','queen','king','ace']
        deck = number_of_decks*list(itertools.product(suits,ranks)) #card is of form: [suit,rank]
        random.shuffle(deck) #shuffle the deck
        return deck

class Table:

    '''> Displays the cards on the table. 
       > playerhand and dealerhand are card arrays.
       > prints the cards that are on the table.
       > dealerturn is set False when it is the players turn, as it hides the dealers second card.'''
    @classmethod
    def DisplayTable(self, playerhand, dealerhand, dealerturn = False):
        os.system('cls')
        playerhanddisplay = []
        dealerhanddisplay = []
        for card in playerhand:
            playerhanddisplay.append(str(card[1]) + ' of ' + str(card[0]))
        for card in dealerhand:
            dealerhanddisplay.append(str(card[1]) + ' of ' + str(card[0]))
        if dealerturn == False:
            dealerhanddisplay[-1] = 'Unknown'
        print('Player cards: ', *playerhanddisplay, sep = '     ')
        print('')
        print('Dealer cards: ', *dealerhanddisplay, sep = '     ')

    '''> Calculating values
       > hand corresponds to dealerhand or playerhand.
       > dealerturn is set False to not show the value of the dealers cards. When it is dealers turn, it shows the dealers values.
       > self.savedplayerhandvalues acts as a save for playerhandvalues when it is the dealers turn (for display purposes). Idk, maybe need some code cleanup.'''
    @classmethod
    def Values(self, hand, dealerturn = False):
        handvalues = []
        for card in hand:

            if (card[1] == 'jack') or (card[1] == 'queen') or (card[1] == 'king'):
                handvalues.append(10)
            elif card[1] == 'ace':
                handvalues.append(11)
            else:
                handvalues.append(int(card[1]))

            if sum(handvalues) <= 21:
                loss = False
            elif sum(handvalues) > 21:
                loss = True
                for i in range(len(handvalues)):
                    if handvalues[i] == 11:
                        handvalues[i] = 1
                        loss = False
                        break
                    else:
                        pass
        if dealerturn == False:
            self.savedplayerhandvalues = handvalues
        else:
            pass
        if dealerturn == True:
            print('\nDealer card value: ', str(sum(handvalues)))
            print('Player card value: ', str(sum(self.savedplayerhandvalues)))
            print('')
        else:
            print('\nPlayer card value: ', str(sum(handvalues)))
            print('')

        return loss, handvalues
            
class Dealer:
    '''> The dealer gets the card deck
       > deck = array of cards (ref SetUp)'''
    def __init__(self,deck):
        self._deck = deck

    '''> The dealer starts the game
       > The initial arrays of playerhand and dealerhand are created and return in this method.
       > playerloss is a Boolean value which determines if the player has lost. In this case it is trivially True.
       > playerhandvalues is an array of the card values. We initialize this because we wish to check if the player has a Blackjack.'''
    def startDeal(self):
        playerhand = []
        dealerhand = []
        for dummyindex in range(2):
            playerhand.append(self._deck[0])
            self._deck.remove(self._deck[0])
            dealerhand.append(self._deck[0])
            self._deck.remove(self._deck[0])
        Table.DisplayTable(playerhand, dealerhand)
        [playerloss, playerhandvalues] = Table.Values(playerhand)
        return playerhand, dealerhand, playerloss, playerhandvalues
    
    '''> Dealer hits a card
       > it returns an arbitrary hand (playerhand or dealerhand, depending who is playing).'''
    def hit(self, hand):
        hand.append(self._deck[0])
        self._deck.remove(self._deck[0])
        return hand

    '''> Dealer play
       > This method uses a simple logic of playing till the dealer gets a higher hand than the player.'''
    '''> playerhand = array of cards (ref SetUp and Table classes)
       > playerhandvalues = array of card values (ref Table.Values)
       > dealerhand = array of dealer's cards.
       > play = user based Boolean value, when true, the user still choses to hit/pass on cards, when False, the loop ends.'''
    def play(self, playerhandvalues, playerhand, dealerhand):
        Table.DisplayTable(playerhand, dealerhand, dealerturn = True)
        [dealerloss, dealerhandvalues] = Table.Values(dealerhand, dealerturn = True)
        play = True
        sleep(1)
        while (play == True) and (dealerloss == False):
            if sum(playerhandvalues) > sum(dealerhandvalues):
                dealerhand = self.hit(dealerhand)
            else:
                play = False
            Table.DisplayTable(playerhand, dealerhand, dealerturn = True)
            [dealerloss, dealerhandvalues] = Table.Values(dealerhand, dealerturn = True)
            sleep(1)
        
        return dealerloss, dealerhandvalues

class Player:
    '''> Player gameplay Loop'''
    '''> playerhand = array of cards (ref SetUp and Table classes)
       > playerloss = Boolean value which checks if sum(playerhandvalues) does not go over 21
       > playerhandvalues = array of card values (ref Table.Values)
       > play = user based Boolean value, when true, the user still choses to hit/pass on cards, when False, the loop ends.'''
    def play(self, playerhand, playerloss, playerhandvalues):
        play = True
        while (play == True) and (playerloss == False):
            playerinput = input('1 - hit, 2 - pass: ')
            if playerinput == '1':
                playerhand = dealer.hit(playerhand)
            elif playerinput == '2':
                play = False
            Table.DisplayTable(playerhand, dealerhand)
            [playerloss, playerhandvalues] = Table.Values(playerhand)
        return playerloss, playerhandvalues

if __name__ == '__main__':  
    '''> Running the program loop. while true, the program is on.'''
    while True:
        '''> Running one game. 
           > The loop returns playerloss and dealerloss Boolean values
           > The loop also returns playerhandvalues and dealerhandvales which is a list of the final card values at the end of the game.'''
        while True:
            '''> Starting game. 
               > Creates instances of dealer and player.
               > Using .startDeal() method to return player and dealer hands, additionally it returns playerloss (in this case False) and playerhandvalues
               to check if there is a blackjack.'''
            dealer, player = Dealer(SetUp.DeckSetUp()), Player() 
            [playerhand, dealerhand, playerloss, playerhandvalues] = dealer.startDeal()           
            '''> BlackJack check.'''
            if sum(playerhandvalues) == 21:
                print("\nYou have a BlackJack!")
                break
            else:
                pass
            '''> In case blackjack does not happen, then method play() from Player class is called. This is where the user plays the game.
               > .play() returns updates on playerloss and playerhandvalues.'''
            [playerloss, playerhandvalues] = player.play(playerhand, playerloss, playerhandvalues)
            if playerloss == True:
                print("\nYou went over 21!")
                break
            else:
                pass
            '''> Dealer play loop starts if the playerloss is False. The logic for the Dealer.play() is similar to the Player one.'''
            [dealerloss, dealerhandvalues] = dealer.play(playerhandvalues, playerhand, dealerhand)
            if dealerloss == True:
                print("\nDealer went over 21! You win!")
                break
            else:
                print("\nDealer won!")
                break
        '''> User chooses if he wants to play again.'''
        playagain = input('\nDo you wish to play again? (Y/N): ')
        if str(playagain).lower().strip() != 'y':
            break
        else:
            pass

