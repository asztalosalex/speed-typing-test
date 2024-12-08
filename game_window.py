from tkinter import *

class GameWindow:

    def __init__(self):
        self.root = Tk()
        self.root.title("Speed Typing Test")
        self.root.geometry("370x400+0+0")
        self.root.resizable(False, False)
        self.root.label = Label(self.root, text="Type the word as fast as you can!", font="Helvetica 20 bold", fg="white", bg="#20bebe", wraplength=350)
        self.root.label.pack(pady=20)
        self.root.input_text = Entry(self.root, font="Roboto 20", borderwidth=1, width=25)
        self.root.input_text.pack(pady=20)
        self.root.mainloop()
        self.start_timer()

    random_words: str[str] = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon", "lime", "mango", "nectarine", "orange", "papaya", "pear", "plum", "pomegranate", "quince", "raspberry", "strawberry", "tangerine", "watermelon"]

    def count_down(self):
        if self.counter > 0:
            self.counter -= 1
            self.timer = self.root.after(1000, self.count_down)


    def start_timer(self):
        self.counter = 60
        self.active = True
        self.timer = self.root.after(1000, self.count_down)
