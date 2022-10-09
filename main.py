import random
from tkinter import *
import json
import pandas

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}
try:
    data = pandas.read_csv("data/remaining_words.csv")
except FileNotFoundError:
    real_data = pandas.read_csv("data/french_words.csv")
    to_learn = real_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# Creates the word to learn after clicking the button
def read_file():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill='black')
    canvas.itemconfig(card_word, text=current_card["French"], fill='black')
    canvas.itemconfig(background_img, image=front_img)
    flip_timer = window.after(3000, func=flip_card)


# Shows the answer to the word
def flip_card():
    canvas.itemconfig(card_title, text="English", fill='white')
    canvas.itemconfig(card_word, text=current_card["English"], fill='white')
    canvas.itemconfig(background_img, image=back_img)


# For Known words
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/remaining_words.csv", index=False)
    read_file()


# --------------------------------- UI SETUP -------------------------------------#
window = Tk()
window.title("FlashApp")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(height=526, width=800)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
background_img = canvas.create_image(400, 263, image=front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill='blue')
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), fill='black')
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
cancel_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cancel_img, highlightthickness=0, command=read_file)
unknown_button.grid(row=1, column=0)

correct_img = PhotoImage(file="images/right.png")
known_button = Button(image=correct_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

read_file()
window.mainloop()
