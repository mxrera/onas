import customtkinter as ctk
from jpeg import JPEG
from constants import BG_COLOR, FG_COLOR

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)

        # Window settings
        self.title("Onas")
        self.geometry("1024x768")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.image = None
        self.codification = None
        self.codification_options = {}
        self.codification_steps = []
        self.results = {}

        self.__init_navbar()
        self.__init_settings_tab()
        self.__init_results_tab()

    def __init_navbar(self):
        self.tabview = ctk.CTkTabview(self, fg_color=FG_COLOR)
        self.tabview.grid(row=0, column=0, sticky=ctk.N + ctk.E + ctk.S + ctk.W)
        self.tabview.add("settings")
        self.tabview.add("results")

    def __init_settings_tab(self):
        self.tabview.tab("settings").grid_columnconfigure(0, weight=1, uniform="a")
        self.tabview.tab("settings").grid_columnconfigure(1, weight=3, uniform="a")
        pass    

    def __init_results_tab(self):
        self.tabview.tab("results").grid_columnconfigure(0, weight=1)
        self.tabview.tab("results").grid_columnconfigure(1, weight=3)
        pass

    def on_run(self):
        if self.image is None or self.codification is None:
            return
        
        self.codification.configure(self.codification_options)
        self.codification_steps = self.codification.steps(self.steps_frame)
        self.results = self.codification(self.image)
        self.fill_results()

    def fill_results(self):
        pass


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()