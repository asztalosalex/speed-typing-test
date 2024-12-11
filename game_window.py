from tkinter import Canvas, Entry, Label, Tk, Text, END, Button
import time
from random_word_api import RandomWordAPI

class GameWindow:

    def __init__(self):
        self.root = Tk()
        self.root.title("Speed Typing Test")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.label = Label(self.root, text="Type as fast as you can!", font="Roboto 20 bold", fg="black", wraplength=750)
        self.root.label.pack(pady=20)
        self.root.input_text = Entry(self.root, font="Roboto 16", fg="black", borderwidth=2, highlightbackground="black")
        self.root.input_text.pack(pady=20)
        self.root.input_text.bind('<Key>', self.start_timer)
        self.root.input_text.bind('<KeyRelease>', self.check_character_match)
        self.root.input_text.bind('<space>', self.handle_space)
        self.word_display = Text(self.root, font=("Roboto", 16), height=5, width=50, wrap='word', state='disabled')
        self.word_display.pack(pady=20)
        self.word_api = RandomWordAPI()
        self.current_word_index = 0
        self.display_words()
        self.root.label_time = Label(self.root, font="Roboto 20 bold", fg="black")
        self.root.label_time.pack(pady=20)
        self.root.button_restart = Button(self.root, text="Restart", font="Roboto 16", fg="black", borderwidth=2, highlightbackground="black", command=self.restart_game)
        self.root.button_restart.place(x=350, y=500)
        self.root.button_restart.config(width=10, height=2, disabledforeground="black", state="disabled")
        self.root.button_restart.pack(pady=20)
        self.root.mainloop()

    def count_down(self):
        if not hasattr(self, 'counter'):
            self.counter = 60
            
        if self.counter > 0:
            self.root.label_time.config(text=f"Time left: {self.counter}")
            self.counter -= 1
            self.timer = self.root.after(1000, self.count_down)

        if self.counter == 0:
            self.root.after_cancel(self.timer)
            self.root.label_time.config(text="Time's up!", fg="red")
            self.root.input_text.unbind('<Key>')
            self.root.input_text.unbind('<KeyRelease>')
            self.root.input_text.unbind('<space>')
            self.root.input_text.unbind('<BackSpace>')
            self.root.input_text.config(state='disabled')
            self.root.button_restart.config(state="normal")

    def start_timer(self, event):
        if not hasattr(self, 'timer_started'):
            self.timer_started = True
            self.count_down()

    def display_words(self):
        self.words = self.word_api.get_random_words(10)
        self.update_word_display()

    def update_word_display(self):
        self.word_display.config(state='normal')
        self.word_display.delete(1.0, END)
        self.word_display.insert(END, ' '.join(self.words))
        self.word_display.config(state='disabled')

    def check_character_match(self, event):
        current_word = self.words[self.current_word_index]
        input_text = self.root.input_text.get().strip()

        self.word_display.config(state='normal')
        self.word_display.delete(1.0, END)
        
        for i, word in enumerate(self.words):
            if i == self.current_word_index:
                start_index = self.word_display.index(END)
                for j, char in enumerate(word):
                    if j < len(input_text):
                        char_color = "green" if input_text[j] == char else "red"
                        self.word_display.insert(END, char, char_color)
                    else:
                        self.word_display.insert(END, char)
                end_index = self.word_display.index(END)
                self.word_display.tag_add("current_word_bg", start_index, end_index)
                self.word_display.insert(END, ' ')
            else:
                self.word_display.insert(END, word + ' ')
        
        self.word_display.tag_configure("green", foreground="green")
        self.word_display.tag_configure("red", foreground="red")
        self.word_display.tag_configure("current_word_bg", background="yellow")
        self.word_display.config(state='disabled')

        if event.keysym == 'BackSpace' and len(input_text) == 0 and self.current_word_index > 0:
            self.current_word_index -= 1
            self.root.input_text.delete(0, 'end')
            self.root.input_text.insert(0, self.words[self.current_word_index])

    def handle_space(self, event):
        self.root.input_text.delete(0, 'end')
        if self.current_word_index < len(self.words) - 1:
            self.current_word_index += 1
            self.root.input_text.delete(0, 'end')

    def check_words_left(self):
        if self.current_word_index >= len(self.words):
            rand_words = self.word_api.get_random_words(10)
            self.words.extend(rand_words)
            self.update_word_display()
            self.current_word_index = 0

    def restart_game(self):
        self.root.button_restart.config(state="disabled")
        self.root.input_text.config(state='normal')
        self.root.input_text.delete(0, 'end')
        self.root.input_text.insert(0, self.words[self.current_word_index])
        self.root.input_text.focus_set()
        self.root.label_time.config(fg="black")
        self.root.label_time.pack(pady=20)
        self.root.display_words()
        self.count_down()
