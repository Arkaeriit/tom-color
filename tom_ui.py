#!/usr/bin/env python3

from tkinter import *
from time import sleep
from tom_color import *
from tkinter import filedialog
import sys
import os
import traceback

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def hex_entry_cb(sv):
    ss = ""
    for c in sv.get()[0:6]:
        if c.lower() in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]:
            ss += c
    sv.set(ss)

class TomUI(Tk):

    def __init__(self):
        super().__init__()
        self.title("Tom Color")
        try:
            self.iconbitmap(resource_path("tom_color.ico")) 
        except:
            pass
        # Color choise
        number_color_choise = list(range(1,31))
        self.number_color = StringVar(self)
        self.number_color.set(number_color_choise[5])
        w = OptionMenu(self, self.number_color, *number_color_choise)
        w.grid(row=0, column=0)
        self.color_labels = []
        self.set_color_labels()
        set_color = Button(self, text="Valider nombre de couleurs", command=self.set_color_labels)
        set_color.grid(row=0, column=1)
        Label(text="Nombre maximum de cette couleur").grid(row=0, column=2)
        # Other parameters
        Label(text="Couleur de la marge").grid(row=0, column=3)
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: hex_entry_cb(sv))
        self.margin_color = Entry(self, textvariable=sv, fg="black", bg="white")
        self.margin_color.grid(row=0, column=4)
        Label(text="Taille des blocks").grid(row=1, column=3)
        self.block_size = Entry(text="", fg="black", bg="white")
        self.block_size.grid(row=1, column=4)
        Label(text="Taille de la marge").grid(row=2, column=3)
        self.margin_size = Entry(text="", fg="black", bg="white")
        self.margin_size.grid(row=2, column=4)
        Label(text="Blocks en largeur").grid(row=3, column=3)
        self.width = Entry(text="", fg="black", bg="white")
        self.width.grid(row=3, column=4)
        Label(text="Blocks en hauteur").grid(row=4, column=3)
        self.height = Entry(text="", fg="black", bg="white")
        self.height.grid(row=4, column=4)
        # Output file
        self.out = ""
        Button(self, text="Fichier destination", command=self.set_file).grid(row=5, column=3)
        self.out_label = Label(text="", fg="black", bg="white")
        self.out_label.grid(row=5, column=4)
        # Generate and report
        Button(self, text="Génération", command=self.generate).grid(row=6, column=3, columnspan=2)
        self.raport = Label(text="", fg="white", bg="white")
        self.raport.grid(row=7, column=2, columnspan=3)

    def generate(self):
        ok, msg = self.sanitize()
        if ok:
            self.raport.config(text="Génération en cours...", fg="blue")
            self.update()
            max_of_colors = []
            colors = []
            max_of_all_colors = int(self.height.get()) * int(self.width.get())
            for color in self.color_labels:
                colors.append(str(color[1].get()))
                if str(color[2].get()) == "":
                    max_of_colors.append(max_of_all_colors)
                else:
                    max_of_colors.append(int(str(color[2].get())))                    
            if sum(max_of_colors) < max_of_all_colors:
                self.raport.config(text="Erreur, le nombre total de couleur max est trop faible", fg="red")
                return

            palette = hex_list_to_palette(colors)
            self.raport.config(text="Palette générée", fg="blue")
            self.update()
            try:
                base_grid = random_fill(int(self.height.get()), int(self.width.get()), palette, max_of_colors)
            except Exception as e:
                self.raport.config(text=repr(e), fg="red")
                traceback.print_exception(type(e), e, e.__traceback__)
                return
            self.raport.config(text="Image aléatoire créée", fg="blue")
            self.update()
            expanded = expand_image_with_margin(base_grid, int(self.block_size.get()), int(self.margin_size.get()), hex_to_rgb(self.margin_color.get()))
            self.raport.config(text="Image finale dessinée", fg="blue")
            self.update()
            make_png(expanded, self.out)
            self.raport.config(text="Nickel, chrome", fg="green")
            self.update()
        else:
            self.raport.config(text=msg, fg="red")

    def set_file(self):
        self.out = filedialog.asksaveasfilename()
        self.out_label.config(text=self.out) 

    def sanitize(self):
        def color_valid(color):
            try:
                int(color, 16)
            except:
                return False
            return len(color) == 6

        for i in range(len(self.color_labels)):
            if not color_valid(str(self.color_labels[i][1].get())):
                return False, f"La couleur {i+1} doit être un code couleur hexadécimal de 6 chiffres (123ABC, 00FF12)"
            if (not str(self.color_labels[i][2].get()) == "") and (not str(self.color_labels[i][2].get()).isnumeric()):
                return False, f"La nombre max de la couleur {i+1} doit être un nombre valide"
        if not color_valid(str(self.margin_color.get())):
            return False, f"La couleur de marge doit être un code couleur hexadécimal de 6 chiffres (123ABC, 00FF12)"
        try:
            with open(self.out, "a") as f:
                pass
            if self.out[-4:] != ".png":
                raise Exception()
        except:
            return False, "Le fichier de destination doit être un png valide."
        try:
            if int(self.margin_size.get()) < 0 or int(self.block_size.get()) <= 0:
                raise Exception()
        except:
            return False, "La taille des blocks et des marges doivent êtres des nombres positifs."
        try:
            if int(self.width.get()) <= 0 or int(self.height.get()) <= 0:
                raise Exception()
        except:
            return False, "Le nombre de blocks en hauteur et en largeur doivent êtres des nombres positifs."
        return True, ""

    def set_color_labels(self):
        for _ in range(len(self.color_labels)):
            self.color_labels[0][0].grid_forget()
            self.color_labels[0][1].grid_forget()
            self.color_labels[0][2].grid_forget()
            self.color_labels.pop(0)
        for i in range(int(str(self.number_color.get()))):
            sv = StringVar()
            sv.trace("w", lambda name, index, mode, sv=sv: hex_entry_cb(sv))
            label = Label(self, text=f"Couleur {1+i}")
            entry = Entry(self, textvariable=sv, fg="black", bg="white")
            entry_max_of_color = Entry(text="", fg="black", bg="white")
            label.grid(row=1+i, column=0)
            entry.grid(row=1+i, column=1)
            entry_max_of_color.grid(row=1+i, column=2)
            self.color_labels.append((label, entry, entry_max_of_color))



if __name__ == "__main__":
    tui = TomUI()
    tui.mainloop()
