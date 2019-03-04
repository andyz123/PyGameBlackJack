import pygame, sys, random
from pygame.locals import *
from time import sleep

# Card object
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return (f'{self.rank}_of_{self.suit}')

# Deck object
class Deck:
    def __init__(self):
        # Adds cards into deck with suits and number on them.
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        s = ''
        for i in range(len(self.deck)):
            s += str(self.deck[i]) + '\n'
        return s

    def shuffle(self):
        random.shuffle(self.deck)

    # Deals a card by removing a card from the Deck.
    def deal(self):
        is_empty = False
        if len(self.deck) == 0:
            is_empty = True
        if is_empty == False:
            return self.deck.pop()

# Hand object
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    # Adds a card to the hand and adjust for aces if value is above 21
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# These are values used to create the cards and color scheme respectively. 
########################################################################################

suits = ('diamonds', 'clubs', 'hearts', 'spades')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 
            'Six': 6, 'Seven': 7, 'Eight': 8, 
            'Nine': 9, 'Ten': 10, 'Jack': 10,
            'Queen': 10, 'King': 10, 'Ace': 11}

# Color in (R,G,B) format
WHITE = (255,255,255)
GREEN = (65,151,0)
BLACK = (0,0,0)
RED = (209, 152, 140)

##########################################################################################

# Used to add text to the game when needed.
def add_text(text, font, surface, x, y, color):
    textobject = font.render(text, 1, color)
    textrect = textobject.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobject, textrect)
    

def game_over():
    # Creates the screen when player goes bankrupt.
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    gameover = pygame.image.load('image/gameoverimage.jpg')
    pygame.display.set_caption('Pygame BlackJack! - GAME OVER!')
    screen.blit(gameover, (0,0))
    add_text('GAME OVER!', pygame.font.SysFont('Calibri',70, bold = True), screen, 700, 200, BLACK)
    add_text('YOU RAN OUT OF CASH!', pygame.font.SysFont('Calibri',70, bold = True), screen, 575, 280, BLACK)
    add_text('THANKS FOR PLAYING!', pygame.font.SysFont('Calibri',70, bold = True), screen, 625, 360, BLACK)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


def play():
    # Creates the first screen the player sees.
    pygame.init()
    gamex, gamey = (1280, 720)
    screen = pygame.display.set_mode((gamex, gamey))
    pygame.display.set_caption('Pygame Blackjack! - Welcome!')
    banner = pygame.image.load('image/banner.png')
    playButton = pygame.image.load('image/play.png')
    playRect = playButton.get_rect()
    playRect.topleft = (850, 300)
    font = pygame.font.SysFont(None, 30)
    screen.fill(RED)
    screen.blit(banner, (50,0))
    screen.blit(playButton, (850, 300))
    # Game instructions.
    add_text('Welcome to Pygame Blackjack! I hope you enjoy your stay.', font, screen, 20, 290, BLACK)
    add_text('Here are some rules and guidelines for you to follow:', font, screen, 20, 330, BLACK)
    add_text(' * At this table, you are only allowed $100 worth of chips.', font, screen, 20, 370, BLACK)
    add_text(' * You can bet in denominations of $5, $10, $20, $50, and $100', font, screen, 20, 410, BLACK)
    add_text(' * A value of over 21 is a bust and the hand with the higher value wins the round.', font, screen, 20, 450, BLACK)
    add_text(' * Beginning the round with a value of 21 triggers Blackjack! You win 2x your bet!', font, screen, 20, 490, BLACK)
    add_text(' * A tie hand is a Push. No money is exchanged.', font, screen, 20, 530, BLACK)
    add_text(' * The actions: split and double down are unavailable.', font, screen, 20, 570, BLACK)
    add_text(' * If you run out of cash, we will politely ask you to leave this table.', font, screen, 20, 610, BLACK)
    add_text(' * Good luck and HAVE FUN!!', font, screen, 20, 650, BLACK)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # If player presses the play button, game begins.
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if playRect.collidepoint(event.pos):
                        player = Hand()
                        dealer = Hand()
                        deck = Deck()
                        take_bet(100, player, dealer, deck)



# Asks player how much they would like to bet.
def take_bet(chips, player, dealer, deck):
    pygame.init()
    # Displays the screen that asks player to pick their betting amounts.
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption('Pygame Blackjack! - Place your bets!')
    image = pygame.image.load('image/betimage.jpg')
    screen.blit(image,(0,0))
    sufficient_funds = False
    if chips < 5:
        game_over()
    betsPlaced = False
    font = pygame.font.SysFont(None,30)
    add_text('Chips: ' + str(chips),font,screen,10,10,BLACK)
    bet5Pos = (200, 250)
    bet5 = pygame.image.load('image/5dollars.png')
    bet5Rect = bet5.get_rect()
    bet5Rect.topleft = (bet5Pos)
    bet10Pos = (500, 250)
    bet10 = pygame.image.load('image/10dollars.png')
    bet10Rect = bet10.get_rect()
    bet10Rect.topleft = (bet10Pos)
    bet20Pos = (800, 250)
    bet20 = pygame.image.load('image/20dollars.png')
    bet20Rect = bet20.get_rect()
    bet20Rect.topleft = (bet20Pos)
    bet50Pos = (350, 400)
    bet50 = pygame.image.load('image/50dollars.png')
    bet50Rect = bet50.get_rect()
    bet50Rect.topleft = (bet50Pos)
    bet100Pos = (650, 400)
    bet100 = pygame.image.load('image/100dollars.png')
    bet100Rect = bet100.get_rect()
    bet100Rect.topleft = (bet100Pos)
    bet = 0
    font1 = pygame.font.SysFont(None, 50)
    add_text('Place your bet', font1, screen, 525, 200, BLACK)
    screen.blit(bet5, bet5Rect)
    screen.blit(bet10, bet10Rect)
    screen.blit(bet20, bet20Rect)
    screen.blit(bet50, bet50Rect)
    screen.blit(bet100, bet100Rect)
    pygame.display.update()
    while betsPlaced == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Checks to see if the player has enough to make that bet.
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if bet5Rect.collidepoint(event.pos):
                        if chips >= 5:
                            bet = 5
                            betsPlaced = True
                    if bet10Rect.collidepoint(event.pos):
                        if chips >= 10:
                            bet = 10
                            betsPlaced = True
                    if bet20Rect.collidepoint(event.pos):
                        if chips >= 20:
                            bet = 20
                            betsPlaced = True
                    if bet50Rect.collidepoint(event.pos):
                        if chips >= 50:
                            bet = 50
                            betsPlaced = True
                    if bet100Rect.collidepoint(event.pos):
                        if chips >= 100:
                            bet = 100
                            betsPlaced = True
    # When player successfully placed a bet, cards are dealt, and game begins.                          
    while betsPlaced is True:
        deck = Deck()
        deck.shuffle()
        player.add_card(deck.deal())
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
        dealer.add_card(deck.deal())
        award = play_hand(bet, chips, player, dealer, deck)
        chips += award
        pygame.display.update()
        take_bet(chips, player, dealer, deck)

def play_hand(bet, chips, player, dealer, deck):
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption('Pygame Blackjack! - PLAY')
    screen.fill(GREEN)
    font = pygame.font.SysFont(None, 30)
    add_text('Money remaining: ' + "$" + str(chips) , font, screen, 10, 10, WHITE)
    add_text('Your bet for this round: ' + "$" + str(bet), font, screen, 10, 30, WHITE)
    add_text('Press "H" to hit' , font, screen, 10, 50, WHITE)
    add_text('Press "S" to stand' , font, screen, 10, 70, WHITE)
    add_text('Player: ', font, screen, 50, 310, WHITE)
    add_text('Dealer: ', font, screen, 400, 10, WHITE)
    pcardx, pcardy = (50, 340)
    # Load the card images into the game.
    for card in player.cards:
        pic = pygame.image.load('Playing Cards/'+ str(card) + '.png')
        screen.blit(pic, (pcardx,pcardy))
        pcardx += 50
    dcardx,dcardy = (500, 10)
    dcard1 = pygame.image.load('Playing Cards/'+ str(dealer.cards[0])+'.png')
    dcard2 = pygame.image.load('Playing Cards/' + str(dealer.cards[1]) + '.png')
    dcardback = pygame.image.load('image/back.png')
    screen.blit(dcardback, (dcardx + 50,dcardy))
    screen.blit(dcard1, (dcardx,dcardy))
    pygame.display.update()
    blackjack = False
    doublePrize = False
    dealerBust = False
    playerBust = False
    # Checks if either the player or dealer has Blackjack.
    if player.value == 21:
        add_text('Blackjack!!! You WIN!!', font, screen, 500, 360, BLACK)
        add_text('Press space to continue', font, screen, 500, 410, BLACK)
        pygame.display.update()
        blackjack = True
        doublePrize = True
    if dealer.value == 21 and player.value != 21:
        add_text('Dealer just got Blackjack. You lose.', font, screen, 500, 360, BLACK)
        add_text('Press space to continue', font, screen, 500, 410, BLACK)
        screen.blit(dcard2, (dcardx + 50, dcardy))
        pygame.display.update()
        blackjack = True
    stand = False
    handDone = False
    playerWins = False
    dealerWins = False
    push = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Game logic to allow to allow button presses on keyboard. 
            if event.type == KEYDOWN:
                if event.key == K_SPACE and doublePrize is True:
                    del player.cards[:]
                    del dealer.cards[:]
                    player.value = 0
                    dealer.value = 0
                    return bet*2 
                if (event.key == K_SPACE and dealer.value == 21 or event.key == K_SPACE 
                    and player.value > 21 or event.key == K_SPACE and dealerWins is True):
                    del player.cards[:]
                    del dealer.cards[:]
                    player.value = 0
                    dealer.value = 0
                    return -bet
                if event.key == K_SPACE and dealer.value > 21 or event.key == K_SPACE and playerWins is True:
                    del player.cards[:]
                    del dealer.cards[:]
                    player.value = 0
                    dealer.value = 0
                    return bet
                if event.key == K_SPACE and push is True:
                    del player.cards[:]
                    del dealer.cards[:]
                    player.value = 0
                    dealer.value = 0
                    return 0
                if event.key == K_h and player.value < 22 and player.value != 21 and stand is False:
                    player.add_card(deck.deal())
                    screen.blit(pygame.image.load('Playing Cards/' + str(player.cards[-1]) + '.png'), (pcardx, pcardy))
                    pcardx+=50
                    pygame.display.update()
        
                    if player.value > 21:
                        add_text('OVER 21! You lose.', font, screen, 500, 360, BLACK)
                        add_text('Press space to continue', font, screen, 500, 410, BLACK)
                        pygame.display.update()
                        playerBust = True
                if event.key == K_s and player.value < 22 and blackjack is False and stand is False:
                    dcardx+=50
                    screen.blit(pygame.image.load('Playing Cards/' + str(dealer.cards[1]) + '.png'), (dcardx, dcardy))
                    pygame.display.update()
                    stand = True
                    # Win conditions
                    while dealer.value < 17 and stand is True and handDone is False:
                        add_text('Dealer is drawing . . .', font, screen, 500, 335, BLACK)
                        sleep(2)
                        dcardx+= 50
                        dealer.add_card(deck.deal())
                        screen.blit(pygame.image.load('Playing Cards/' + str(dealer.cards[-1]) + '.png'), (dcardx, dcardy))
                        pygame.display.update()
                        
                        if dealer.value > 21:
                            add_text('DEALER BUST! YOU WIN!', font, screen, 500, 360, BLACK)
                            add_text('Press space to continue', font, screen, 500, 410, BLACK)
                            pygame.display.update()
                            dealerBust = True
                    if dealer.value >= 17:
                        handDone = True
                    if dealerBust is False and stand is True and playerBust is False and blackjack is False and handDone is True:
                        if dealer.value <= 21 and player.value <= 21:
                            if player.value > dealer.value:
                                add_text('YOU WIN!', font, screen, 500, 360, BLACK)
                                add_text('Press space to continue', font, screen, 500, 410, BLACK)
                                pygame.display.update()
                                playerWins = True
                            if player.value < dealer.value:
                                add_text('Dealer wins.', font, screen, 500, 360, BLACK)
                                add_text('Press space to continue', font, screen, 500, 410, BLACK)
                                pygame.display.update()
                                dealerWins = True
                            if player.value == dealer.value:
                                add_text('Tie!', font, screen, 500, 360, BLACK)
                                add_text('Press space to continue', font, screen, 500, 410, BLACK)
                                pygame.display.update() 
                                push = True
                          
# Executes the game.
if __name__ == '__main__':
    play()