from tkinter import *
from tkinter import messagebox
import winsound

from classes import *

# SOME STYLES FOR BUTTONS
btn_settings = {
    'font': 'helv12',
    'width': 7,
    'height': 1,

}

btn_grid = {
    'padx': 6,
    'pady': 3
}

# UNMOUNT WIDGETS
rw = [] # THIS ARRAY CONTAINS WIDGETS TO UNMOUNT

def clear_widgets(widgets):
    for widget in widgets:
        widget.grid_remove()

    widgets = []


# MOVE VALIDATION FUNCTIONS

# CHECK WHETHER AN ATTACK MOVE IS VALID
def attack_valid(card, table):
    # IF TABLE IS EMPTY THEN ANY MOVE IS VALID
    if len(table) == 0 and isinstance(card, Card):
        return True
    # IF TABLE IS NOT EMPTY THEN YOU ARE ABLE TO USE ONLY THOSE CARS WHOSE VALUES LIES ON THE TABLE
    if isinstance(card, Card):
        if card.val in [card.val for card in table]:
            return True
        else:
            return False
    # PASS IS VALID ONLY IF TABLE IS NOT EMPTY
    # IF YOU ARE AN ATTACKER YOU CANNOT PASS WITHOUT DOING ANY MOVE,
    # YOU HAVE TO ATTACK AT LEAST ONE TIME
    elif card == 0:
        if len(table) != 0:
            return True
        else:
            return False


# CHECK WHETHER A DEFENSE MOVE IS VALID
def defense_valid(card, table, trump):
    if isinstance(card, Card):
        # IF ATTACKER'S CARD IS ONE OF THE TRUMP SUIT THEN
        # DEFENSE IS VALID ONLY IF DEFENDER'S CARD VALUE IS HIGHER AND OF TRUMP SUIT
        if table[-1].suit == trump.suit:
            if card.val > table[-1].val and card.suit == table[-1].suit:
                return True
            else:
                return False
        # IF ATTACKER'S CARD ISN'T ONE OF THE TRUMP SUIT THEN DEFENSE IS VALID
        # ONLY IF DEFENDER'S CARD VALUE IS HIGHER AND OF THE SAME SUIT
        # OR IF DEFENDER'S CARD IS ONE OF THE TRUMP SUIT
        else:
            if card.val > table[-1].val and card.suit == table[-1].suit or card.suit == trump.suit:
                return True
            else:
                return False
    # PASS IS ALWAYS VALID MOVE FOR DEFENSE
    elif card == 0:
        return True


# PLAYER WITH THE SMALLEST TRUMP GOES FIRST
def goesFirst(player1, computer, trump):
    # GENERATE ARRAYS WITH CARDS OF THE TRUMP SUIT
    playertrumps = [x for x in player1.hand if x.suit == trump.suit]
    comptrumps = [x for x in computer.hand if x.suit == trump.suit]

    # IF TWO PLAYERS HAVE CARDS OF THE TRUMP SUIT
    # THEN ONE WITH THE LEAST TRUMP CARD GOES FIRST

    # IF NONE OF THEM HAVE CARDS OF THE TRUMP SUIT
    # THEN ATTACKER GOES FIRST
    if not playertrumps and comptrumps:
        return 2
    elif not comptrumps and playertrumps:
        return 1
    elif not comptrumps and not playertrumps:
        return 0
    elif playertrumps and comptrumps:
        playertrumps.sort(key=lambda x: x.val)
        comptrumps.sort(key=lambda x: x.val)
        if playertrumps[0].val < comptrumps[0].val:
            return 1
        else:
            return 2


# FUNCTION TO GENERATE CALLBACKS FOR THE BUTTONS
# EVERY BUTTON SETS HAS TO SET VAL TO VAR (WHICH IS A TKINTER VARIABLE)
def callback_generator(val, var):
    return lambda: var.set(val)


def game(root, var):

    root.geometry('1000x600')
    root.configure(background='green')

    # GAME UI

    def UI(attacker, defender, trump, round):

        # UNMOUNT OLD WIDGETS
        clear_widgets(rw)

        global buttons
        buttons = []

        global mode

        # EVERY WIDGET IS 1) CREATING 2) MOUNTING ON GRID 3) APPENDING TO ARRAY OF WIDGETS TO UNMOUNT

        # CREATING LABEL OF THE TRUMP CARD
        w = Label(root, text='TRUMP CARD: \n' + trump.show())
        w.grid(row=2, column=0, padx=6, pady=6)
        rw.append(w)

        # CREATING WIDGET WITH AMOUNT OF CARD IN THE DECK
        w = Label(root, text='CARDS IN THE DECK: \n' +
                  str(len(deck.cards)))
        w.grid(row=3, column=0, padx=6, pady=6)
        rw.append(w)


        # METHOD OF CREATING THE TABLE DEPENDS ON MODE PLAYER HAS CHOSEN

        # TRAINING MODE
        if mode:
            player_is_attacker = isinstance(attacker, Player)

            if player_is_attacker:

                # IF PLAYER IS ATTACKER
                # DEFENDER CARD BUTTONS ARE SHOWN BUT DISABLED (UNCLICKABLE)

                w = Label(root, text=f"{attacker.name}' HAND")
                w.grid(row=0, column=1, **btn_grid)
                rw.append(w)

                values = attacker.showHand(trump)
                i = 1
                j = 1
                for value in values:
                    bt = Button(root, text=value, command=callback_generator(
                        value.split(':')[0], var), **btn_settings, fg='red' if value[-1] == trump.show()[-1] else 'black')
                    bt.grid(row=i, column=j, **btn_grid)
                    buttons.append(bt)
                    rw.append(bt)

                    # IF I % 8 CONTINUE DRAWING BUTTONS ON THE NEXT COLUMN
                    if i % 8 == 0:
                        i = 1
                        j += 1
                    else:
                        i += 1

                w = Label(root, text=f"{defender.name}'S HAND")
                w.grid(row=0, column=83, **btn_grid)
                rw.append(w)

                values = defender.showHand(trump)
                i = 1
                j = 83
                for value in values:
                    bt = Button(root, text=value, command=callback_generator(
                        value.split(':')[0], var), state='disabled', **btn_settings, disabledforeground='#FA6669' if value[-1] == trump.show()[-1] else 'gray')
                    bt.grid(row=i, column=j, **btn_grid)
                    rw.append(bt)

                    # IF I % 8 CONTINUE DRAWING BUTTONS ON THE NEXT COLUMN
                    if i % 8 == 0:
                        i = 1
                        j += 1
                    else:
                        i += 1

            else:

                # IF PLAYER IS DEFENDER
                # ATTACKER CARD BUTTONS ARE SHOWN BUT DISABLED (UNCLICKABLE)

                w = Label(root, text=f"{defender.name}'S HAND")
                w.grid(row=0, column=1, **btn_grid)
                rw.append(w)

                values = defender.showHand(trump)
                i = 1
                j = 1
                for value in values:
                    bt = Button(root, text=value, command=callback_generator(
                        value.split(':')[0], var), **btn_settings, fg='red' if value[-1] == trump.show()[-1] else 'black')
                    bt.grid(row=i, column=j, **btn_grid)
                    buttons.append(bt)
                    rw.append(bt)

                    # IF I % 8 CONTINUE DRAWING BUTTONS ON THE NEXT COLUMN
                    if i % 8 == 0:
                        i = 1
                        j += 1
                    else:
                        i += 1

                w = Label(root, text=f"{attacker.name}'S HAND")
                w.grid(row=0, column=83, **btn_grid)
                rw.append(w)

                values = attacker.showHand(trump)
                i = 1
                j = 83
                for value in values:
                    bt = Button(root, text=value, command=callback_generator(
                        value.split(':')[0], var), state='disabled', **btn_settings, disabledforeground='#FA6669' if value[-1] == trump.show()[-1] else 'gray')
                    bt.grid(row=i, column=j, **btn_grid)
                    rw.append(bt)

                    # IF I % 8 CONTINUE DRAWING BUTTONS ON THE NEXT COLUMN
                    if i % 8 == 0:
                        i = 1
                        j += 1
                    else:
                        i += 1

        # GAME MODE
        else:
            # IF PLAYER IS ATTACKER THEN DRAW ATTACKER CARDS AND LENGTH OF DEFENDER HAND
            if isinstance(attacker, Player):
                w = Label(root, text=f"{attacker.name}'S HAND")
                w.grid(row=0, column=1, **btn_grid)
                rw.append(w)

                i, j, values = 1, 1, attacker.showHand(trump)
                for value in values:
                    bt = Button(root, text=value, command=callback_generator(
                        value.split(':')[0], var), **btn_settings, fg='red' if value[-1] == trump.show()[-1] else 'black')
                    bt.grid(row=i, column=j, **btn_grid)
                    buttons.append(bt)
                    rw.append(bt)

                    # IF I % 8 CONTINUE DRAWING BUTTONS ON THE NEXT COLUMN
                    if i % 8 == 0:
                        i = 1
                        j += 1
                    else:
                        i += 1

                w = Label(root, text=f"COMPUTER'S HAND")
                w.grid(row=0, column=83, **btn_grid)
                rw.append(w)

                w = Label(root, text=f"{len(defender.hand)} CARDS")
                w.grid(row=1, column=83, **btn_grid)
                rw.append(w)

            else:
                # IF PLAYER IS DEFENDER THEN DRAW DEFENDER CARDS AND LENGTH OF ATTACKER HAND
                w = Label(root, text=f"{defender.name}'S HAND")
                w.grid(row=0, column=1, **btn_grid)
                rw.append(w)

                i, j, values = 1, 1, defender.showHand(trump)
                for value in values:
                    bt = Button(root, text=value, command=callback_generator(
                        value.split(':')[0], var), **btn_settings, fg='red' if value[-1] == trump.show()[-1] else 'black')
                    bt.grid(row=i, column=j, **btn_grid)
                    buttons.append(bt)
                    rw.append(bt)

                    # IF I % 8 CONTINUE DRAWING BUTTONS ON THE NEXT COLUMN
                    if i % 8 == 0:
                        i = 1
                        j += 1
                    else:
                        i += 1

                w = Label(root, text=f"COMPUTER'S HAND")
                w.grid(row=0, column=83, **btn_grid)
                rw.append(w)

                w = Label(root, text=f"{len(attacker.hand)} CARDS")
                w.grid(row=1, column=83, **btn_grid)
                rw.append(w)

        w = Label(root, text='TABLE', width=30)
        w.grid(row=0, column=42, columnspan=2, padx=10)
        rw.append(w)

        if isinstance(attacker, Player):
            ja, jd = 42, 43
        else:
            ja, jd = 43, 42

        i, k = 1, 0
        for card in round:
            if k % 2 == 0:
                w = Label(root, text=card.show(), fg='red' if card.show()[-1] == trump.show()[-1] else 'black', **btn_settings)
                w.grid(row=i, column=ja, **btn_grid)
                rw.append(w)
                
            else:
                w = Label(root, text=card.show(), fg='red' if card.show()[-1] == trump.show()[-1] else 'black', **btn_settings)
                w.grid(row=i, column=jd, **btn_grid)
                rw.append(w)

                i += 1

            k += 1

        w = Button(root, text='PASS', command=callback_generator(
            '0', var), **btn_settings)
        w.grid(row=4, column=0, pady=6, padx=6)
        rw.append(w)

    while True:

        # INITIALIZE THE GAME

        Game = True
        Quit = False
        round = [] # CARDS ON THE TABLE
        deck = Deck()
        deck.shuffle()
        player1 = Player(name)
        computer = Computer()
        for _ in range(0, 6): # HANDS INITIALIZATION
            player1.draw(deck)
            computer.draw(deck)
        trump = deck.trump() # TRUMP CARD
        attacker = player1
        defender = computer 
        goesfirst = goesFirst(player1, computer, trump) # WHO GOES FIRST
        if goesfirst == 0:
            continue
        elif goesfirst == 2: # IF COMPUTER GOES FIRST
            attacker, defender = defender, attacker

        # GAME LOOP

        while Game:

            # TAKING CARDS FROM THE DECK
            # If it was bita, the roles switched, and attacker is now defender, taking first
            # If it was taken, the defender has > 6 cards, so the attacker takes, defender doesn't
            # If it was taken, but the defender has <= 6 cards, then the deck is empty
            while len(defender.hand) < 6:
                if deck.cards:
                    defender.draw(deck)
                else:
                    break
            while len(attacker.hand) < 6:
                if deck.cards:
                    attacker.draw(deck)
                else:
                    break

            # ROUND LOOP

            while True:

                 # CHECK FOR THE WINNER AND AUTOMATIC BITA FROM THE PREVIOUS ROUND

                if len(attacker.hand) == 0 and len(deck.cards) == 0:
                    Game = False
                    if len(defender.hand) == 0:
                        Winner = 0
                        break
                    Winner = attacker
                    break
                elif len(round) == 12: #CANNOT ATTACK WITH MORE THAN 6 CARDS
                    round.clear()
                    attacker, defender = defender, attacker
                    break
                elif len(attacker.hand) == 0 and len(deck.cards) != 0: #BITA IF ATTACKER HAS NO CARDS LEFT
                    round.clear()
                    attacker, defender = defender, attacker
                    break
                elif len(attacker.hand) == 1 and len(deck.cards) == 24: # FIRST ROUND ONLY 5 CARDS CAN BE PLAYED
                    round.clear()
                    attacker, defender = defender, attacker
                    break

                if len(defender.hand) == 0 and len(deck.cards) == 0:
                    Game = False
                    Winner = defender
                    break
                elif len(defender.hand) == 0 and len(deck.cards) != 0:
                    round.clear()
                    attacker, defender = defender, attacker # ATTACKER AND DEFENDER SWAP
                    break

                UI(attacker, defender, trump, round)

                # ATTACKER'S MOVE
                if isinstance(attacker, Computer): # IF THE ATTACKER IS COMPUTER
                    move = attacker.attack(round, trump, deck, defender)

                else:
                    w = Label(root, text="Your Move. Attack!")
                    w.grid(row=41, column=0, columnspan=4, padx=6, pady=10)
                    rw.append(w)

                    move = attacker.play(root, var)

                    while not attack_valid(move, round): # MOVE VALIDATION FOR HUMAN PLAYER
                        if isinstance(move, Card):
                            attacker.takeCard(move)  # TAKE BACK THE MOVE AND MAKE ANOTHER
                            UI(attacker, defender, trump, round)

                            w = Label(
                                root, text="Please choose a valid card")
                            w.grid(row=41, column=0, columnspan=4, padx=6, pady=10)
                            rw.append(w)

                            move = attacker.play(root, var)
                        else:
                            if move == 0:
                                UI(attacker, defender, trump, round)

                                w = Label(
                                    root, text="You can't pass on the first move.\nPlease choose another move")
                                w.grid(row=41, column=0, columnspan=4, padx=6, pady=10)
                                rw.append(w)

                                move = attacker.play(root, var)
                            elif move == "exit":
                                root.destroy()
                                exit()

                    if Game == False:
                        break

                if move == 0: # BITA
                    round.clear()
                    attacker, defender = defender, attacker
                    break

                round.append(move)
                UI(attacker, defender, trump, round)

                # DEFENDERS MOVE
                if isinstance(defender, Computer):
                    move = defender.defend(round, trump, deck)

                    if move == 0:
                        w = Label(
                            root, text=f"You can play vdoqonku.\nChoose cards and press PASS to continue.")
                        w.grid(row=41, column=0, columnspan=4, padx=6, pady=10)
                        rw.append(w)

                        vdoqonkulist = attacker.vdoqonku(root, var, buttons)
                        while True:
                            if len(vdoqonkulist) > len(defender.hand) - 1:
                                UI(attacker, defender, trump, round)

                                w = Label(
                                    root, text=f"You can play vdoqonku.\nChoose cards and press PASS to continue.")
                                w.grid(row=41, column=0, columnspan=4, padx=6, pady=10)
                                rw.append(w)

                                vdoqonkulist = attacker.vdoqonku(
                                    root, var, buttons)
                            elif len(vdoqonkulist) == 1 and vdoqonkulist[0] == 0:
                                break
                            else:
                                for card in vdoqonkulist:
                                    if not attack_valid(card, round):
                                        UI(attacker, defender, trump, round)

                                        w = Label(
                                            root, text="Invalid card(s). Make correct choice or pass.")
                                        w.grid(
                                            row=41, column=0, columnspan=4, padx=6, pady=10)
                                        rw.append(w)

                                        var.set("r")
                                        vdoqonkulist = attacker.vdoqonku(
                                            root, var, buttons)
                                        break
                                else:
                                    round = round + vdoqonkulist
                                    for i in vdoqonkulist:
                                        attacker.hand.remove(i)
                                    break

                        for card in round:
                            defender.takeCard(card)
                        round.clear()
                        break

                else:
                    w = Label(root, text="Your Move. Defend!")
                    w.grid(row=41, column=0, columnspan=4, padx=6, pady=10)
                    rw.append(w)

                    move = defender.play(root, var)

                    while not defense_valid(move, round, trump):
                        if isinstance(move, Card):
                            defender.takeCard(move)
                            UI(attacker, defender, trump, round)

                            w = Label(
                                root, text="Please choose a valid card.")
                            w.grid(row=41, column=0, columnspan=4, padx=6, pady=10)
                            rw.append(w)

                            move = defender.play(root, var)
                        else:
                            if move == "exit":
                                root.destroy()
                                exit()

                    if Game == False:
                        break

                    if move == 0:
                        for card in round:
                            defender.takeCard(card)
                        round.clear()
                        vdoqonku = attacker.vdoqonku(
                            round, trump, deck, defender)
                        round += vdoqonku
                        if len(round) > 0:
                            UI(attacker, defender, trump, round)
                            w = Label(
                                root, text="Press PASS to take computer's extra/vdoqonku cards")
                            w.grid(row=41, column=0, columnspan=4, padx=6, pady=10)
                            rw.append(w)

                            w.wait_variable(var)

                            for card in round:
                                defender.takeCard(card)
                            round.clear()
                        break

                round.append(move)

        if Quit == False:

            UI(attacker, defender, trump, round)

            # GAME IS OVER SO CREATE NEW WINDOW AND SHOW THE RESULT
            # ANIMATION AND AUDIO DEPENDS ON THE RESULT:
            # WIN AND DRAW SHOWS THE SAME ANIMATION

            gameover = Tk()
            gameover.title("GAME IS OVER")
            gameover.protocol("WM_DELETE_WINDOW", lambda: exit())
            canvas = Canvas(gameover, height=305, width=476)
            canvas.pack()

            if Winner == 0:
                winsound.PlaySound('draw.wav', winsound.SND_ASYNC)

                for i in range(1, 16):
                    img = PhotoImage(master=canvas, file=f'frame {i}.PNG')
                    canvas.create_image(238, 152, image=img)
                    canvas.update()
                    canvas.after(2)

                text = f"IT'S A DRAW!"

            else:
                if Winner.name == "COMPUTER":
                    
                    winsound.PlaySound('lose.wav', winsound.SND_ASYNC)

                    for i in range(1, 9):
                        img = PhotoImage(master=canvas, file=f'bomb {i}.PNG')
                        canvas.create_image(238, 152, image=img)
                        canvas.update()
                        canvas.after(120)

                else:
                    winsound.PlaySound('victory.wav', winsound.SND_ASYNC)

                    for i in range(1, 16):
                        img = PhotoImage(master=canvas, file=f'frame {i}.PNG')
                        canvas.create_image(238, 152, image=img)
                        canvas.update()
                        canvas.after(2)

                text = f"{Winner.name} WON"

            label = Label(gameover, text=text)
            label.pack()
            Button(gameover, text='OK', command=lambda: gameover.quit(), height=3, width=12).pack()
            gameover.mainloop()

            gameover.destroy()

            # ASK PLAYER WHETHER HE WANTS TO PLAY AGAIN
            again = messagebox.askyesno(
                title=text, message="Do you want to play again?")

            if not bool(again):
                root.destroy()
                exit()


try:
    # ASKING PLAYER WHETHER HE WANTS TO PLAY TRAINING MODE
    mode = messagebox.askyesnocancel(
        title='Choose mode', message='Would you like to run training mode?')

    # IF PLAYER CLICK ON CANCEL OR EXIT SHUT THE PROGRAM DOWN
    if mode == None:
        exit()

    root = Tk()
    # X BUTTON EXITS THE PROGRAM
    root.protocol("WM_DELETE_WINDOW", lambda: exit())
    root.title('THE GAME OF DURAK')
    # FORCE-FOCUSING THE WINDOW, MAKE IT ACTIVE
    root.focus_force()

    # THIS VARIABLE IS USING IN CALLBACKS ON THE UI BUTTONS
    # GAME WILL WAIT UNTIL THE VAR HAS CHANGED (BUTTON CLICKED -> VAR CHANGED -> GAME LOOP CONTINUES)
    var = StringVar()

    var_name = StringVar()
    name_entry = Entry(root, textvariable=var_name)

    name_label = Label(root, text='Please enter your name')

    def get_name():
        # SAVE USER'S NAME TO GLOBAL VARIABLE
        global name
        name = var_name.get()
        # UNMOUNT WIDGETS
        name_label.grid_remove()
        name_entry.grid_remove()
        name_btn.grid_remove()

        # NEXT YOU WILL BE ABLE TO CLOSE THE GAME BY SETTING 'exit' TO var
        root.protocol("WM_DELETE_WINDOW", lambda: var.set('exit'))
        # START THE GAME
        game(root, var)

    # SUBMIT BUTTON WILL START THE GAME
    name_btn = Button(root, text='Submit', command=get_name)

    name_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
    name_entry.grid(row=0, column=1, sticky='w', padx=10, pady=10)
    name_btn.grid(row=0, column=2, sticky='w', padx=10, pady=10)

    root.mainloop()


except TypeError:
    exit()
