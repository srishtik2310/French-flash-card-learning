from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
word_dict = {}
window = Tk()
window.title("Flash card")
window.config(bg = BACKGROUND_COLOR, padx= 50, pady = 50)


try:
    word_df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    word_df_exception = pandas.read_csv("data/french_words.csv")
    word_dict = word_df_exception.to_dict(orient="records")
else:
    word_dict = word_df.to_dict(orient="records")

def display_next_word():
    global word_dict, title, word, current_word, flip_timer
    window.after_cancel(flip_timer)
    new_dict = random.choice(word_dict)
    new_word = new_dict["French"]
    canvas.itemconfig(card_image, image=card_front_image)
    canvas.itemconfig(title, text = "French", fill = "black")
    canvas.itemconfig(word, text = f"{new_word}", fill = "black")
    current_word = new_dict
    flip_timer = window.after(3000, func = english_translation)


def english_translation():
    global title, word, card_back_image
    english_word = current_word["English"]
    canvas.itemconfig(card_image, image = card_back_image)
    canvas.itemconfig(title, text="English", fill = "white")
    canvas.itemconfig(word, text=f"{english_word}", fill = "white")

def known_word():
    global word_dict
    word_dict.remove(current_word)
    data = pandas.DataFrame(word_dict)
    data.to_csv("data/words_to_learn.csv", index = False)
    display_next_word()

flip_timer = window.after(3000, func= english_translation)

canvas = Canvas(width= 800, height= 526, bg = BACKGROUND_COLOR, highlightthickness= 0)
card_front_image = PhotoImage(file = "/Users/srish/PycharmProjects/flash_card/images/card_front.png")
card_back_image = PhotoImage(file = "/Users/srish/PycharmProjects/flash_card/images/card_back.png")
card_image = canvas.create_image(400, 263, image = card_front_image)
canvas.grid(row = 0, column = 0, columnspan = 2)
title = canvas.create_text(400, 150, text = "", font = ("Ariel", 40, "bold"))
word = canvas.create_text(400, 250, text = "", font = ("Ariel", 30, "normal"))

right_image = PhotoImage(file = "images/right.png")
right_button = Button(image = right_image, command = known_word)
right_button.grid(row=1, column = 0)

wrong_image = PhotoImage(file = "images/wrong.png")
wrong_button = Button(image = wrong_image, command = display_next_word)
wrong_button.grid(row= 1, column=1)

display_next_word()

window.mainloop()