import customtkinter as ctk
from tkinter import filedialog
from jpeg import JPEG
from constants import BG_COLOR, FG_COLOR, HIGHLIGHT_COLOR

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)

        # Window settings
        self.title("Onas")
        self.geometry("1024x768")
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=3, uniform="a")
        self.grid_rowconfigure(0, weight=1)

        self.image = None
        self.codification = None
        self.codification_options = {}
        self.options_list = []
        self.codification_steps = []
        self.results = {}

        self.__init_navbar()
        self.__init_settings_tab()
        self.__init_results_tab()
        self.__init_main_frame()

        self.tabview.set("settings")
        self.on_codification_select("JPEG")

    def __init_navbar(self):
        self.tabview = ctk.CTkTabview(self, fg_color=FG_COLOR, bg_color =FG_COLOR)
        self.tabview.grid(row=0, column=0, sticky=ctk.N + ctk.E + ctk.S + ctk.W)
        self.tabview.add("settings")
        self.tabview.add("results")

    def __init_settings_tab(self):
        self.tabview.tab("settings").grid_columnconfigure(0, weight=1, uniform="a")
        self.tabview.tab("settings").grid_rowconfigure(0, weight=1, uniform="a")
        self.tabview.tab("settings").grid_rowconfigure(1, weight=2, uniform="a")
        self.tabview.tab("settings").grid_rowconfigure(2, weight=1, uniform="a")
        self.tabview.tab("settings").grid_rowconfigure(3, weight=1, uniform="a")
        self.tabview.tab("settings").grid_rowconfigure(4, weight=1, uniform="a")
        self.tabview.tab("settings").grid_rowconfigure(5, weight=6, uniform="a")
        self.tabview.tab("settings").grid_rowconfigure(6, weight=1, uniform="a")

        ctk.CTkLabel(self.tabview.tab("settings"), text="Settings").grid(row=0, column=0, sticky=ctk.W + ctk.E)
        ctk.CTkLabel(self.tabview.tab("settings"), text="Image").grid(row=1, column=0, sticky=ctk.W + ctk.E + ctk.N + ctk.S)
        ctk.CTkButton(
            self.tabview.tab("settings"),
            command=self.on_image_select,
            text="Select",
            fg_color=BG_COLOR
        ).grid(row=2, column=0, sticky=ctk.W + ctk.E)
        
        ctk.CTkComboBox(
            self.tabview.tab("settings"),
            values=["JPEG"],
            command=self.on_codification_select,
            fg_color=BG_COLOR
        ).grid(row=3, column=0, sticky=ctk.W + ctk.E)
        
        ctk.CTkLabel(self.tabview.tab("settings"), text="Codification Options").grid(row=4, column=0, sticky=ctk.W + ctk.E)
        
        self.options_frame = ctk.CTkScrollableFrame(
            self.tabview.tab("settings"),
            fg_color=FG_COLOR
        )
        self.options_frame.grid(row=5, column=0, sticky=ctk.N + ctk.E + ctk.S + ctk.W)
        self.options_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(self.tabview.tab("settings"), text="run", command=self.on_run, fg_color=HIGHLIGHT_COLOR).grid(row=6, column=0, sticky=ctk.W + ctk.E)

    def __init_results_tab(self):
        self.tabview.tab("results").grid_columnconfigure(0, weight=1)
        self.tabview.tab("results").grid_rowconfigure(0, weight=1)
        self.tabview.tab("results").grid_rowconfigure(1, weight=9)

        ctk.CTkLabel(self.tabview.tab("results"), text="Results").grid(row=0, column=0, sticky=ctk.W + ctk.E)
        self.results_frame = ctk.CTkScrollableFrame(self.tabview.tab("results"), fg_color=FG_COLOR)        
        self.results_frame.grid(row=1, column=0, sticky=ctk.N + ctk.E + ctk.S + ctk.W)

    def __init_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.main_frame.grid(row=0, column=1, sticky=ctk.N + ctk.E + ctk.S + ctk.W)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.main_frame.grid_rowconfigure(1, weight=1, uniform="a")

        image_comparison_frame = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR, corner_radius=0)
        image_comparison_frame.grid(row=0, column=0, sticky=ctk.N + ctk.E + ctk.S + ctk.W)
        self.original_image = ctk.CTkFrame(image_comparison_frame, fg_color=FG_COLOR)
        self.codified_image = ctk.CTkFrame(image_comparison_frame, fg_color=FG_COLOR)

        self.steps_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color=BG_COLOR, corner_radius=0)
        self.steps_frame.grid(row=1, column=0, sticky=ctk.N + ctk.E + ctk.S + ctk.W)

    def on_image_select(self):
        file_path = filedialog.askopenfilename()
    
    def on_codification_select(self, codification):
        if codification == "JPEG":
            self.codification = JPEG()
            self.fill_codification_options(self.codification.options())

    def on_run(self):
        if self.image is None or self.codification is None:
            return
        
        self.codification.configure(self.variable_to_dict(self.codification_options))
        self.codification_steps = self.codification.steps(self.steps_frame)
        self.results = self.codification(self.image)
        self.fill_results()

    def fill_codification_options(self, options: dict):
        # Clean previous options
        for option in self.options_list:
            option.destroy()
        self.options_list = []
        self.codification_options = {}

        # Create new options
        for key, value in options.items():            
            option_frame = ctk.CTkFrame(
                self.options_frame,
                width=210,
                corner_radius=5,
                fg_color=BG_COLOR
            )
            option_frame.grid(row=len(self.options_list), column=0, sticky=ctk.W + ctk.E, pady=5, padx=5)
            option_frame.grid_columnconfigure(1, weight=1, uniform="a")
            option_frame.grid_rowconfigure(0, weight=1, uniform="a")
            option_frame.grid_rowconfigure(1, weight=1, uniform="a")
            
            ctk.CTkLabel(
                option_frame,
                justify="left",
                text=key
            ).grid(row=0, column=0, sticky=ctk.W + ctk.N + ctk.S, pady=5, padx=5)
            if value["type"] == "combobox":
                var = ctk.StringVar(value=value["default"])
                ctk.CTkComboBox(
                    option_frame,
                    variable=var,
                    values=value["values"],
                    fg_color=BG_COLOR
                ).grid(row=1, column=0, sticky=ctk.W + ctk.E + ctk.N + ctk.S, pady=5, padx=5)

            elif value["type"] == "slider":
                var = ctk.DoubleVar(value=value["default"])
                ctk.CTkSlider(
                    option_frame,
                    variable=var,
                    from_=value["values"][0],
                    to=value["values"][1],
                    number_of_steps=((value["values"][1] - value["values"][0]) / value["values"][2]),
                    fg_color=BG_COLOR
                ).grid(row=1, column=0, sticky=ctk.W + ctk.E + ctk.N + ctk.S, pady=5, padx=5)
                ctk.CTkLabel(
                    option_frame,
                    textvariable=var,
                    fg_color=BG_COLOR
                ).grid(row=0, column=0, sticky=ctk.N + ctk.S + ctk.E, pady=5, padx=5)
            
            elif value["type"] == "switch":
                var = ctk.BooleanVar(value=value["default"])
                ctk.CTkSwitch(
                    option_frame,
                    variable=var,
                    onvalue=True,
                    offvalue=False,
                    fg_color=BG_COLOR
                ).grid(row=1, column=0, sticky=ctk.W + ctk.E + ctk.N + ctk.S, pady=5, padx=5)
            else:
                raise ValueError(f"Invalid option type: {value['type']}")

            self.codification_options[key] = var
            self.options_list.append(option_frame)
                
    def fill_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for key, value in self.results.items():
            ctk.CTkLabel(self.results_frame, text=key, fg_color=BG_COLOR)
            ctk.CTkLabel(self.results_frame, text=value, fg_color=BG_COLOR)

        for widget in self.steps_frame.winfo_children():
            widget.destroy()

        for step in self.codification_steps:
            ctk.CTkLabel(self.results_frame, text=step.name, fg_color=BG_COLOR).pack()
            ctk.CTkLabel(self.results_frame, text=step.description, fg_color=BG_COLOR).pack()
        
    def variable_to_dict(self, variables: dict) -> dict:
        return {key: value.get() for key, value in variables.items()}


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()
