#!/usr/bin/env python3

from tkinter import *
from tom_color import *

class TomUI(Tk):

    def __init__(self):
        super().__init__()
        # Color choise
        number_color_choise = list(range(1,31))
        self.number_color = StringVar(self)
        self.number_color.set(number_color_choise[5])
        w = OptionMenu(self, self.number_color, *number_color_choise)
        w.grid(row=0, column=0)
        self.color_labels = []
        self.set_color_labels()
        set_color = Button(self, text="Valider nombre de couleur", command=self.set_color_labels)
        set_color.grid(row=0, column=1)
        # Other parameters
        Label(text="Couleur de la marge").grid(row=0, column=2)
        margin_color = Entry(text="", fg="black", bg="white")
        margin_color.grid(row=0, column=3)
        Label(text="Taille des blocks").grid(row=1, column=2)
        margin_color = Entry(text="", fg="black", bg="white")
        margin_color.grid(row=1, column=3)
        Label(text="Taille de la marge").grid(row=2, column=2)
        margin_color = Entry(text="", fg="black", bg="white")
        margin_color.grid(row=2, column=3)

    def set_color_labels(self):
        print("lol")
        for _ in range(len(self.color_labels)):
            self.color_labels[0][0].grid_forget()
            self.color_labels[0][1].grid_forget()
            self.color_labels.pop(0)
        for i in range(int(str(self.number_color.get()))):
            label = Label(text=f"Couleur {1+i}")
            entry = Entry(text="", fg="black", bg="white")
            label.grid(row=1+i, column=0)
            entry.grid(row=1+i, column=1)
            self.color_labels.append((label, entry))



if __name__ == "__main__":
    tui = TomUI()
    tui.mainloop()
