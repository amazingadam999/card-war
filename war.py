import pygame
import os
import random


cwd = os.getcwd()
pygame.init()
mainfont = pygame.font.SysFont(pygame.font.get_default_font(), 40)


#settings not added yet, but this is where
#they will be read from a file, right now I am
#hard-coding their values

musicplay = True
crashplay = True




width = 1500
height = 844
display = pygame.display.set_mode((width,height))
pygame.display.set_caption("Cards")
clock = pygame.time.Clock()
cardwidth = 150
cardheight = 210

def pfc(x, y, width=cardwidth, height=cardheight):
    #input centre of the where you want the image, and it will return the x and y
    #position to draw it
    #pfc stands for position from centre, and it defaults to the card height and with

    newx = x-(width/2)
    newy = y-(height/2)

    return (newx, newy)


def fullcardname(cardname): #gives the full name of a card, eg 8S returns 8 of Spades
    cardname = cardname.lower()
    if cardname == "joker":
        return "Joker"

    if len(cardname) != 2:
        return "???"

    if cardname[0].isdigit():
        typec = cardname[0] #type of card


    elif cardname[0] == "t":
        typec = 10

    elif cardname[1] == "e":
        typec = 11

    elif cardname[0] == "j":
        typec = "Jack"

    elif cardname[0] == "q":
        typec = "Queen"

    elif cardname[0] == "k":
        typec = "King"

    elif cardname[0] == "a":
        typec = "Ace"

    else:
        return "???"

    if cardname[1] == "s":
        suit = "Spades"

    elif cardname[1] == "c":
        suit = "Clubs"

    elif cardname[1] == "h":
        suit = "Hearts"

    elif cardname[1] == "d":
        suit = "Diamonds"

    else:
        return "???"

    return typec + " of " + suit


def cardrank(cardname): #turns a card into its number to compare values, J = 12, Q = 13, K = 14, A = 15, Joker = 999, used to compare card values
    cardname = cardname.lower()
    if cardname == "joker":
        return 999 # jokers beat every other card, so they get a very high number

    if len(cardname) != 2:
        return -1 # invalid cards are given the lowest value of -1

    if cardname[0].isdigit():
        return int(cardname[0])

    elif cardname[0] == "t":
        return 10

    elif cardname[0] == "e":
        return 11

    elif cardname[0] == "j":
        return 12

    elif cardname[0] == "q":
        return 13

    elif cardname[0] == "k":
        return 14

    elif cardname[0] == "a":
        return 15

    else:
        return -1



pygame.mixer.music.load(cwd+"/sounds/music.ogg")
if musicplay is True:
    pygame.mixer.music.play(-1)
crash = pygame.mixer.Sound(cwd+"/sounds/crash.ogg")
    
                                                             

hidden = pygame.image.load(cwd+"/cards/black.png")
cpuhidden = pygame.image.load(cwd+"/cards/red.png")




white = (255, 255, 255)

run = True
end = False

chose = None
cpuchose = None
cpuchosetime = None
reveal = False
nofileimage = pygame.image.load(cwd+"/cards/nofile.png")

#lists of cards, types, and suits
listoftypes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "T", "E", "J", "Q", "K", "A", "Joker"]
listofsuits = ["S", "C", "H", "D"]
listofcards = []
cardimages = {}
for typeofcard in listoftypes:
    if typeofcard == "Joker":
        # this only loads the image of the joker, it does not add it to the deck
        cardimages["Joker"] = pygame.image.load(cwd+"/cards/joker.png")
        continue

    for suit in listofsuits:
        cardname = typeofcard+suit
        listofcards.append(cardname)
        try:
            cardimages[cardname] = pygame.image.load(cwd+"/cards/"+cardname.lower()+".png")
        except:
            cardimages[cardname] = nofileimage
            print(cardname, " doesn't have an image. Make sure ", cardname, ".png exists in the cards folder.", sep="")

listofcards.append("Joker") #adding joker(s)



cardstoplay = []
cpucardstoplay = []
deck = list(listofcards)
random.shuffle(deck)

if len(deck) % 2 != 0: # determining how many cards each player shoud bhave
    adv = random.randint(0, 1)
    if adv == 0:
        nofcards = int(len(deck)/2) + len(deck) % 2
        cpunofcards = int(len(deck)/2)
    else:
        cpunofcards = int(len(deck)/2) + len(deck) % 2
        nofcards = int(len(deck)/2)

else:
    cpunofcards = int(len(deck)/2)
    nofcards = int(len(deck)/2)


cardstoplay = deck[:nofcards] #giving each player cards
cpucardstoplay = deck[nofcards:nofcards+cpunofcards]


cardsowned = []
cpucardsowned = []
drawcards = []

##cardstoplay[-1] = "Joker"
##
##cpucardstoplay[-1] = "Joker"


drawcards = []

##cardstoplay = ["Joker", "Joker", "Joker", "AS"]
##cpucardstoplay = ["Joker", "Joker", "Joker"]



while run is True:
    display.fill(white)


    if reveal is True:
        pygame.time.wait(2500)

        # updates cardsowned
        if cardrank(cardtoplay) > cardrank(cpucardtoplay):
            for card in drawcards:
                cardsowned.append(card)
            cardsowned.append(cardtoplay)
            cardsowned.append(cpucardtoplay)
            drawcards = []
                
        elif cardrank(cardtoplay) < cardrank(cpucardtoplay):
            for card in drawcards:
                cpucardsowned.append(card)
            cpucardsowned.append(cpucardtoplay)
            cpucardsowned.append(cardtoplay)
            drawcards = []
            
                
        elif cardrank(cardtoplay) == cardrank(cpucardtoplay):
            drawcards.append(cardtoplay)
            drawcards.append(cpucardtoplay)


        del cpucardstoplay[-1]
        del cardstoplay[-1]


        if len(cpucardstoplay) < 1 or len(cardstoplay) < 1:
            if len(cardsowned) < len(cpucardsowned):
                endsurface = mainfont.render('Finish! CPU wins the game!', False, (0, 0, 0))
            elif len(cardsowned) > len(cpucardsowned):
                endsurface = mainfont.render('Finish! You win the game!', False, (0, 0, 0))
            else:
                endsurface = mainfont.render('Finish! The game is a draw!', False, (0, 0, 0))


            display.blit(endsurface, pfc(width*0.2, height*0.5, textsurface.get_width(), textsurface.get_height()))
            end = True
            
        chose = None
        cpuchose = None
        cpuchosetime = None
        reveal = False


        
        


    elif chose is not None and cpuchose is not None and end is False:
        pygame.time.wait(2000)
        if crashplay is True:
            crash.play()
        
        cpucardtoplay = cpucardstoplay[-1]
        cardtoplay = cardstoplay[-1]
        
        if cardrank(cardtoplay) > cardrank(cpucardtoplay):
            textsurface = mainfont.render('You win this round!', False, (0, 0, 0))

        elif cardrank(cardtoplay) < cardrank(cpucardtoplay):
            textsurface = mainfont.render('CPU wins this round!', False, (0, 0, 0))
                
        elif cardrank(cardtoplay) == cardrank(cpucardtoplay):
            textsurface = mainfont.render('It is a draw this round!', False, (0, 0, 0))

        display.blit(textsurface, pfc(width*0.2, height*0.5, textsurface.get_width(), textsurface.get_height()))
        reveal = True
        

    if cpuchosetime is None:
        cpuchosetime = pygame.time.get_ticks() + random.randint(500, 2000)


    if cpuchose is None:
        if pygame.time.get_ticks() >= cpuchosetime:
            if len(cpucardstoplay) >= 3:
                cpuchose = random.randint(0, 2)
            elif len(cpucardstoplay) >= 2:
                cpuchose = random.randint(0, 1)
            elif len(cpucardstoplay) >= 1:
                cpuchose = 0
    
        

        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if chose is None:
                try:
                    if card0 is not None:
                        if card0.collidepoint(mousex, mousey):
                            chose = 0
                    if card1 is not None:
                        if card1.collidepoint(mousex, mousey):
                            chose = 1
                    if card2 is not None:
                        if card2.collidepoint(mousex, mousey):
                            chose = 2
                except NameError:
                    pass


            
                    


    #player's cards

    if chose != 0 and len(cardstoplay) >= 1:
        card0 = display.blit(hidden, pfc(width*0.4, height*0.8))
    else:
        card0 = None
    if chose != 1 and len(cardstoplay) >= 2:
        card1 = display.blit(hidden, pfc(width*0.5, height*0.8))
    else:
        card1 = None
    if chose != 2 and len(cardstoplay) >= 3:
        card2 = display.blit(hidden, pfc(width*0.6, height*0.8))
    else:
        card2 = None

    if len(cardstoplay) > 3:
        display.blit(hidden, pfc(width*0.75, height*0.8))

    #cpu's cards

    if cpuchose != 0 and len(cpucardstoplay) >= 1:
        cpuc0 = display.blit(cpuhidden, pfc(width*0.4, height*0.2))
    if cpuchose != 1 and len(cpucardstoplay) >= 2:
        cpuc1 = display.blit(cpuhidden, pfc(width*0.5, height*0.2))
    if cpuchose != 2 and len(cpucardstoplay) >= 3:
        cpuc2 = display.blit(cpuhidden, pfc(width*0.6, height*0.2))

    if len(cpucardstoplay) > 3:
        display.blit(cpuhidden, pfc(width*0.75, height*0.2))


    if chose is not None and reveal is False:
            display.blit(hidden, pfc(width * 0.4, height * 0.5))

    elif reveal is True:
        display.blit(cardimages[cardtoplay], pfc(width * 0.4, height * 0.5))

            
    if cpuchose is not None and reveal is False:
            display.blit(cpuhidden, pfc(width * 0.6, height * 0.5))

    elif reveal is True:
        display.blit(cardimages[cpucardtoplay], pfc(width * 0.6, height * 0.5))


    if len(cardsowned) >= 1:
        display.blit(cardimages[cardsowned[-1]], pfc(width * 0.2, height * 0.8))

    scoresurface = mainfont.render('Your score: '+str(len(cardsowned)), False, (0, 0, 0))
    display.blit(scoresurface, pfc(width*0.2, height*0.95, scoresurface.get_width(), scoresurface.get_height()))

    scoresurface = mainfont.render("CPU's score: "+str(len(cpucardsowned)), False, (0, 0, 0))
    display.blit(scoresurface, pfc(width*0.2, height*0.05, scoresurface.get_width(), scoresurface.get_height()))

    if len(cpucardsowned) >= 1:
        display.blit(cardimages[cpucardsowned[-1]], pfc(width * 0.2, height * 0.2))

    if len(drawcards) >= 1:
        display.blit(cardimages[drawcards[-1]], pfc(width * 0.5, height * 0.5))
    

        
    pygame.display.update()
    
    if end is True:
        pygame.time.wait(5000)
        run = False
        break


    clock.tick(50)



pygame.quit()
