import os
import customtkinter as ctk
from tkinter import filedialog
from jpeg import JPEG
from constants import BG_COLOR, FG_COLOR, HIGHLIGHT_COLOR
from PIL import Image

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
        self.source_image_frame = None
        self.codification = None
        self.codification_options = {}
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
        placeholder_path = os.path.join(
            os.path.dirname(__file__), "../images/placeholder.png")
        placeholder_image = ctk.CTkImage(Image.open(placeholder_path), size=(95, 84))
        self.image_preview = ctk.CTkLabel(
            self.tabview.tab("settings"),
            text="",
            image=placeholder_image
        )
        self.image_preview.grid(row=1, column=0, sticky=ctk.W + ctk.E + ctk.N + ctk.S)
        ctk.CTkButton(
            self.tabview.tab("settings"),
            command=self.on_image_select,
            text="Select Image",
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
        self.options_frame.grid_columnconfigure(0, weight=1, uniform="a")

        ctk.CTkButton(self.tabview.tab("settings"), text="run", command=self.on_run, fg_color=HIGHLIGHT_COLOR).grid(row=6, column=0, sticky=ctk.W + ctk.E)

    def __init_results_tab(self):
        self.tabview.tab("results").grid_columnconfigure(0, weight=1)
        self.tabview.tab("results").grid_rowconfigure(0, weight=1)
        self.tabview.tab("results").grid_rowconfigure(1, weight=9)
        self.tabview.tab("results").grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self.tabview.tab("results"), text="Results").grid(row=0, column=0, sticky=ctk.W + ctk.E)
        self.results_frame = ctk.CTkScrollableFrame(self.tabview.tab("results"), fg_color=FG_COLOR)        
        self.results_frame.grid(row=1, column=0, sticky=ctk.N + ctk.E + ctk.S + ctk.W)
        self.results_frame.grid_columnconfigure(0, weight=1, uniform="a")
        ctk.CTkButton(
            self.tabview.tab("results"),
            text="save image",
            command=self.on_save_image,
            fg_color=HIGHLIGHT_COLOR
        ).grid(row=2, column=0, sticky=ctk.W + ctk.E)

    def __init_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.main_frame.grid(row=0, column=1, sticky=ctk.N + ctk.E + ctk.S + ctk.W)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.main_frame.grid_rowconfigure(1, weight=1, uniform="a")

        image_comparison_frame = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR, corner_radius=0)
        image_comparison_frame.grid(row=0, column=0, sticky=ctk.N + ctk.E + ctk.S + ctk.W)
        image_comparison_frame.grid_columnconfigure(0, weight=1, uniform="a")
        image_comparison_frame.grid_columnconfigure(1, weight=1, uniform="a")
        image_comparison_frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.original_image = ctk.CTkLabel(image_comparison_frame, fg_color=FG_COLOR, text="")
        self.original_image.grid(row=0, column=0, sticky=ctk.N + ctk.E + ctk.S + ctk.W, padx=15, pady=15)
        self.codified_image = ctk.CTkLabel(image_comparison_frame, fg_color=FG_COLOR, text="")
        self.codified_image.grid(row=0, column=1, sticky=ctk.N + ctk.E + ctk.S + ctk.W, padx=15, pady=15)

        self.steps_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color=BG_COLOR,
            corner_radius=0
        )
        self.steps_frame.grid(row=1, column=0, sticky=ctk.N + ctk.E + ctk.S + ctk.W)
        self.steps_frame.grid_columnconfigure(0, weight=1, uniform="a")

    def on_image_select(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.image = Image.open(file_path)
            self.source_image_frame = ctk.CTkImage(
                self.image,
                size=(210, self.image.height * 210 // self.image.width)
            )
            self.image_preview.configure(image=self.source_image_frame)
    
    def on_save_image(self):
        if self.results.get("image") is None:
            return
        file_path = filedialog.asksaveasfilename(
            title="Save image",
            filetypes=[
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.codification.save_image(self.results["image"], file_path)

    def on_codification_select(self, codification):
        if codification == "JPEG":
            self.codification = JPEG()
            self.fill_codification_options(self.codification.options())

    def on_run(self):
        if self.image is None or self.codification is None:
            return
        self.clear_results_tab()

        self.tabview.set("results")
        self.source_image_frame.configure(size=(341, self.image.height * 341 // self.image.width))
        self.original_image.configure(image=self.source_image_frame)

        self.codification.configure(**self.variable_to_dict(self.codification_options))
        self.place_steps(self.codification.steps(self.steps_frame))
        self.results = self.codification(self.image)

        self.codified_image.configure(
            image=ctk.CTkImage(
                self.results["image"],
                size=(341, self.results["image"].height * 341 // self.results["image"].width)
            )
        )
        self.fill_results()

    def fill_codification_options(self, options: dict):
        # Clean previous options
        for option in self.options_frame.winfo_children():
            option.destroy()
        self.codification_options = {}

        # Create new options
        for key, value in options.items():            
            option_frame = ctk.CTkFrame(
                self.options_frame,
                width=210,
                corner_radius=5,
                fg_color=BG_COLOR
            )
            option_frame.grid(row=len(self.options_frame.winfo_children()), column=0, sticky=ctk.W + ctk.E, pady=5, padx=5)
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
    
    def place_steps(self, steps: list):            
        for i, step in enumerate(steps):
            step.grid(row=i, column=0, sticky="nsew", padx=10, pady=10)
    
    def clear_results_tab(self):
        for widget in self.steps_frame.winfo_children():
            widget.destroy()
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def fill_results(self):
        for key, value in self.results.items():
            result_frame = ctk.CTkFrame(
                self.results_frame,
                fg_color=FG_COLOR,
                corner_radius=5
            )
            result_frame.grid(row=len(self.results_frame.winfo_children()), column=0, sticky=ctk.W + ctk.E, pady=5, padx=5)
            result_frame.grid_columnconfigure(0, weight=1, uniform="a")
            result_frame.grid_columnconfigure(1, weight=1, uniform="a")
            result_frame.grid_rowconfigure(0, weight=1, uniform="a")
            ctk.CTkLabel(result_frame, text=key, fg_color=FG_COLOR).grid(row=0, column=0, sticky=ctk.W + ctk.E)
            ctk.CTkLabel(result_frame, text=str(value), fg_color=FG_COLOR).grid(row=0, column=1, sticky=ctk.W + ctk.E)
        
    def variable_to_dict(self, variables: dict) -> dict:
        return {key: value.get() for key, value in variables.items()}


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()
