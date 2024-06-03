import customtkinter as ctk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from onas.gui import FG_COLOR, FONT_COLOR, FONT_COLOR, PARAGRAPH_FONT, BG_COLOR

class StepsFrame(ctk.CTkFrame):
    def __init__(self, name: str, parent, description: str):
        super().__init__(
            parent, 
            width=708,
            height=189//2,
            corner_radius=10,
            fg_color=FG_COLOR,
        )
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=2, uniform="a")
        self.grid_rowconfigure(0, weight=1, uniform="a")
        self.grid_rowconfigure(1, weight=4, uniform="a")
        
        self.name = ctk.CTkLabel(
            self,
            text=name,
            font=PARAGRAPH_FONT,
            text_color=FONT_COLOR,
            fg_color=FG_COLOR
        )
        self.name.grid(row=0, column=0, columnspan=2, sticky=ctk.N + ctk.W + ctk.E, padx=10, pady=10)

        self.description = ctk.CTkTextbox(
            self,
            fg_color=FG_COLOR,
            font=PARAGRAPH_FONT,
            text_color=FONT_COLOR,
            wrap="word",
        )
        self.description.grid(row=1, column=1, sticky=ctk.N + ctk.S + ctk.E + ctk.W, padx=10, pady=10)
        self.description.insert("0.0", self.remove_spaces(description))
        self.description.configure(state="disabled")
    
        self.fig = Figure()
        self.fig.set_size_inches(2, 2)
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().place(relx=0.05, rely=0.15)
    
    def get_plot(self, *args):
        if len(args) == 0:
            return self.fig.add_subplot(111)
        
        return self.fig.add_subplot(*args)
    
    def update_plot(self):
        self.canvas.draw()

    def remove_spaces(self, text: str) -> str:
        return " ".join(text.split())
    