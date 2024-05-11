<h1 align="center">
    Onas
</h1>

![onas settings](./images/onas-settings.png)
![onas results](./images/onas-results.png)

## `App` class

```python
import customtkinter as ctk

class App(ctk.App): # or tk.Tk, where tk is the tkinter module
    def __init__(self):
        super().__init__(title="Onas")
        
        self.codification = None
        self.settings = {}
        self.results = {}
        self.steps = []
        self.image = None

        self.__init_navbar()
        self.__init_settings_tab()
        self.__init_results_tab()
    
    def __init_navbar(self):
        ...

    def __init_settings_tab(self):
        ...
    
    def __init__results_tab(self):
        ...

    def on_run(self):
        self.codification.configure(self.settings)
        self.results, self.steps = self.codification(input=self.image, parent=self.steps_frame)
        self.fill_results()
    
    def fill_results(self):
        ...

if __name__ == "__main__":
    app = App()
    app.mainloop()
```

## `Codification` class

```python
class Codification:
    def __init__(self):
        pass
    
    def options(self) -> dict:
        return {
            "Option name": {
                "type": "combobox",
                "values": ["value1", "value2", "value3"],
                "default": "value1"
            },
            "Option name": {
                "type": "checkbox",
                "default": True
            },
        }
    
    def steps(self, parent) -> list:
        return [
            StepFrame(
                name="First step",
                description="Description of the step",
                parent=parent
            ),
            StepFrame(
                name="Second step",
                description="Description of the step",
                parent=parent
            ),
            StepFrame(
                name="Third step",
                description="Description of the step",
                parent=parent
            )
        ]
    
    def configure(self, options) -> bool:
        pass
    
    def __call__(self, image, steps_parent) -> dict | dict:
        steps = self.steps(steps_parent)
        ...
        axes = steps[0].figure.add_subplot()
        axes.imshow(image)
        ...
        results = {
            "image": compressed_image,
            "parameter1": "value1",
            "parameter2": "value2",
            "parameter3": "value3"
        }

        return results, steps
```
