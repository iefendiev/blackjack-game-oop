import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                newCard=Card(suit,rank)
                self.deck.append(newCard)

    def __str__(self):
        for card in self.deck:
            print(card)
        return " "

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        while len(self.deck)>0:
            card = self.deck.pop(0)
            return card
        return None

class Hand:
    def __init__(self):
        self.cards = []  
        self.value = 0   
        self.aces = 0    # an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces+=1
            
    def adjust_for_ace(self):
        while self.value>21 and self.aces:
            self.value-=10
            
            self.aces-=1
        
class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total+=self.bet
    
    def lose_bet(self):
        self.total-=self.bet


def take_bet(chips):
    
    try:
        # chips.bet yazman lazım input olarak 
        
        chips.bet=int(input("Please mark us your bet \n"))
        
    except:
        print("This is not an integer \n")
        take_bet(chips)
        
    if chips.bet>chips.total:
        print(f"You don't have that much credit. Total credit: {chips.total} \n")
        take_bet(chips)


def hit(deck,hand):
    
    hand.add_card(deck.deal())
    
    #ADD CARD METODU CARD INPUTU ALIYOR. DEAL METODU BİR KART VERİYOR
    
    hand.adjust_for_ace()

"""
mesela hit(deck,hand) şöyle de olabilirdi

singleCard=deck.deal()
hand.add_card(singleCard)
hand.adjust_for_ace()
"""

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    
    while True:
        
        HS=input("Do you want to hit or stand \n")
        if HS[0].lower()=="h":
            
            #bunu yazarken aldığı argümanları da girmemiz lazım fonksiyonun
            hit(deck,hand)
            
            
        elif HS[0].lower()=="s":
            print("Player stands")
            playing=False
            
        else:
            print("Please enter a valid decisition : hit ~ stand")
            hit_or_stand(deck,hand)
            
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)
    
# ending conditions 
def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")


#gamethrough 

while True:
    playing=True
    # Print an opening statement
    print("Welcome to Black Jack \n")
    
    # Create & shuffle the deck, deal two cards to each player
    deck=Deck()
    deck.shuffle()
    
    players_hand=Hand()
    dealers_hand=Hand()
    
    players_hand.add_card(deck.deal())
    players_hand.add_card(deck.deal())
    
    dealers_hand.add_card(deck.deal())
    dealers_hand.add_card(deck.deal())
    
        
    # Set up the Player's chips
    playersChips=Chips()
    
    # Prompt the Player for their bet
    take_bet(playersChips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(players_hand,dealers_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,players_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(players_hand,dealers_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if players_hand.value>21:
            player_busts(players_hand,dealers_hand,playersChips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if players_hand.value<=21:
        
        while dealers_hand.value<17:
            hit(deck,dealers_hand)        
            
        # Show all cards
        
        show_all(players_hand,dealers_hand)
        
        # Run different winning scenarios
        if players_hand.value > dealers_hand.value and players_hand.value<=21:
            player_wins(players_hand,dealers_hand,playersChips)
            
        elif  players_hand.value < dealers_hand.value and dealers_hand.value<=21:
            dealer_wins(players_hand,dealers_hand,playersChips)
            
        elif players_hand.value > 21:
            player_busts(players_hand,dealers_hand,playersChips)
            
            
        elif dealers_hand.value > 21:
            
            dealers_busts(players_hand,dealers_hand,playersChips)
            
        elif dealers_hand.value == players_hand.value:
            push(players_hand,dealers_hand)
            
        else:
            print("An Error Occured in Winning Conditions")
    
    # Inform Player of their chips total 
    print(f"Players chips: {playersChips.total} \n")
    print(f"Card Values: {players_hand.value} \n")
    
    # Ask to play again
    playAgain=input("Do you want to play again? \n")
    if playAgain[0].lower()=="y":
        playing=True
        continue

    elif playAgain[0].lower()=="n":
        playing=False
        print("Thanks for playing \n")

        break








