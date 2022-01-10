from tkinter import *
from tkinter import messagebox
from random import randint
import pandas

review = []
FONT = ("Verdana", 20, "normal")
prev_selected = []
init_length = 0
english = ""
spanish = ""
language_dict = {}
select = 0
need_reviewed = {'Spanish': [], 'English': []}
flip = 0


# ------------ Refreshes the list from scratch ---------------- #
def restart():
    global need_reviewed, prev_selected
    need_reviewed = {'Spanish': [], 'English': []}
    prev_selected = []
    flash_label.config(text="Get Ready to Learn Spanish", font=FONT, bg="#dde1e0", height=7)
    gen_dict()


# ----------------- Review Missed Words ----------------------- #
def review():
    global prev_selected
    flash_label.config(text="Review what you missed", font=FONT, bg="#dde1e0", height=7)
    prev_selected = []
    gen_dict()


# ----------------- Create Dict of Words ----------------------- #
def gen_dict():
    global language_dict, need_reviewed, init_length

    if len(need_reviewed['Spanish']) > 0:
        language_dict = pandas.DataFrame(need_reviewed)
        need_reviewed = {'Spanish': [], 'English': []}
    else:
        language_dict = pandas.read_csv('spanish.csv', encoding='utf-8')
    init_length = len(language_dict)


# ------------- Add Missed Word for Review -------------------- #
def wrong():
    need_reviewed['Spanish'].append(spanish)
    need_reviewed['English'].append(english)
    word_gen()


# ------------------ Generate a Word -------------------------- #
def word_gen():
    global init_length, prev_selected, select, english, spanish, flip
    flip = 0
    if len(language_dict) > 0:
        sel = True
        while sel:
            select = randint(0, init_length - 1)
            print(select)
            if select not in prev_selected:
                sel = False
        prev_selected.append(select)
        flash_button.config(image=flash_front)
        flash_label.config(text=language_dict.Spanish[select], font=FONT, bg="#dde1e0", height=7)

    else:
        flash_label.config(font=("verdana", 13, "normal"), text="You have reached the end of the list.\nPress "
                        "either button to start all.\nOr select review to only go over\nthe ones you missed", height=12)
        gen_dict()
        prev_selected = []

    english = language_dict.English[select]
    spanish = language_dict.Spanish[select]
    print(language_dict)
    language_dict.drop(labels=select, axis=0, inplace=True)


# -------------------------- Flip Card --------------------- #
def flip_card():
    global flip
    if flip == 0:
        flash_label.config(text=english, bg="#4a9082")
        flash_button.config(image=flash_back)
        flip = 1
    else:
        flash_label.config(text=spanish, bg="#dde1e0")
        flash_button.config(image=flash_front)
        flip = 0


# -------------------- Window Set-Up --------------------------- #
window = Tk()
window.config(bg="#81f2df", padx=20, pady=20)
window.title("Learn Spanish With Flash Cards")
x_Left = int(window.winfo_screenwidth()/2 - 350)
y_Top = int(window.winfo_screenheight()/2 - 300)
window.geometry("+{}+{}".format(x_Left, y_Top))
window.resizable(width=False, height=False)

# ------------------------- GUI -------------------------------- #
gen_dict()

restart_button = Button(text="Restart", width=5, command=restart)
restart_button.place(x=0, y=0)

review_button = Button(text="Review", width=5, command=review)
review_button.place(x=495, y=0)

flash_front = PhotoImage(file="flash_front.png")
flash_back = PhotoImage(file="flash_back.png")
flash_button = Button(image=flash_front, highlightthickness=0, bd=0, command=flip_card)
flash_button.place(x=25, y=35)
flash_label = Label(text="Get Ready to Learn Spanish", font=FONT, bg="#dde1e0", height=7)
flash_label.grid(columnspan=3, column=1, row=1, pady=50, padx=45)

green_check = PhotoImage(file="green_check.png")
correct_button = Button(image=green_check, highlightthickness=0, bd=0, command=word_gen)
correct_button.grid(column=3, row=3, padx=80, pady=10)

red_x = PhotoImage(file="red_x.png")
wrong_button = Button(image=red_x, highlightthickness=0, bd=0, command=wrong)
wrong_button.grid(column=1, row=3, padx=80, pady=10)

messagebox.showinfo("Instructions", "Welcome to flashcards:\n\n"
                                    "To start: Press the green check.\n"
                                    "To flip a card: press anywhere on card\n"
                                    "If you know the answer: press the green check\n"
                                    "If you do not know the answer: press the red X\n"
                                    "To review missed cards: press review in the upper right\n"
                                    "to restart all cards: press start in upper left\n\n"
                                    "Have fun and enjoy learning!")

window.mainloop()
