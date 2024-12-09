from tkinter import Canvas, Entry, Label, Tk
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
        self.root.input_text.bind('<KeyRelease>', self.spell_check)
        self.root.canvas = Canvas(self.root, width=600, height=200, bg="white", borderwidth=2, highlightbackground="black")
        self.root.canvas.pack(pady=20)
        self.word_api = RandomWordAPI()
        self.current_word_index = 0
        self.display_words()
        self.highlight_current_word()
        self.root.label_time = Label(self.root, font="Roboto 20 bold", fg="black")
        self.root.label_time.pack(pady=20)
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

    def start_timer(self, event):
        if not hasattr(self, 'timer_started'):
            self.timer_started = True
            self.count_down()

    def display_words(self):
        self.root.canvas.delete("all")
        self.words = self.word_api.get_random_words(10)
        self.word_positions = []
        
        x_position = 20
        y_position = 100
        line_height = 30
        current_line = 1
        
        for word in self.words:
            word_width = len(word) * 10  
            
            if x_position + word_width > 580:
                x_position = 10
                y_position += line_height
                current_line += 1
            
            text_id = self.root.canvas.create_text(
                x_position,
                y_position,
                text=word,
                font=("Roboto", 16),
                fill="black",
                anchor="w"  
            )
            self.word_positions.append(text_id)
            x_position += word_width + 25


    def spell_check(self, event):
        if not hasattr(self, 'timer_started'):
            return
        
        current_word = self.words[self.current_word_index]
        input_text = self.root.input_text.get()

        if event.char == ' ':
            self.root.input_text.delete(0, 'end')
            if self.current_word_index < len(self.words) - 1:
                self.current_word_index += 1
                self.highlight_current_word()
        else:
            if len(input_text) <= len(current_word):
                all_correct = True
                for i in range(len(input_text)):
                    if input_text[i] != current_word[i]:
                        all_correct = False
                        break
                
                self.root.canvas.itemconfig(
                    self.word_positions[self.current_word_index],
                    fill="green" if all_correct else "red"
                )

    def highlight_current_word(self):
        for i, text_id in enumerate(self.word_positions):
            self.root.canvas.itemconfig(i, fill="black")
        
        if self.current_word_index < len(self.word_positions):
            self.root.canvas.itemconfig(
                self.word_positions[self.current_word_index], 
                fill="blue"
            )



