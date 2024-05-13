import customtkinter as ctk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from constants import (
    FG_COLOR, FONT_COLOR, FONT_COLOR_HIGHLIGHT)

class StepsFrame(ctk.CTkFrame):
    def __init__(self, name: str, parent, description: str):
        super().__init__(
            parent, 
            width=708,
            height=189,
            corner_radius=10,
            fg_color=FG_COLOR,
        )
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=3, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        
        self.name = ctk.Label(self, text=name, fg=FONT_COLOR, font=("Inter", 14))
        self.name.grid(row=0, column=0, sticky=ctk.N + ctk.W + ctk.E)

        self.description = ctk.CTkTextbox(self, fg_color=FG_COLOR, state="disabled",)
        self.description.insert("0.0", self.remove_spaces(description))
        self.description.grid(row=0, column=1, sticky=ctk.S + ctk.E + ctk.W)
    
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

    def update_plot(self):
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=ctk.BOTTOM, fill=ctk.BOTH, expand=True)

    def remove_spaces(self, text: str) -> str:
        pass