# Contributing

## Adding codification algorithms

### Codification class

The codification class must contain the following methods:

- `options`: A method that returns the options that the user can configure. For more information, see [Codification options](#codification-options).

```python
def options(self) -> dict:
    return {
        "Option name": {
            "type": "combobox",
            "values": ["value1", "value2", "value3"],
            "default": "value1"
        },
        "Option name": {
            "type": "switch",
            "default": False
        },
        "Option name": {
            "type": "slider",
            "values": [1, 10, 1],
            "default": 5
        }
    }
```

- `steps`: A method that returns the steps that the codification algorithm will take as a list of `StepsFrame` objects.

```python
from steps import StepsFrame

def steps(self, steps_parent) -> list:
    self.codification_steps = [ 
        StepsFrame(
            name="Block creation",
            parent=steps_parent,
            description="Divide the image into blocks of the selected size...
        ),
        StepsFrame(
            name="Direct Transform",
            parent=steps_parent,
            description="Each block is transformed using the selected method...
        ),
        ...
    ]
    return self.codification_steps
```

> [!TIP]
> The `StepsFrame` object has a `matplotlib` figure that can be used to show images or plots. It has the follwing methods to make plots:
> - `get_plot()`: Returns the `matplotlib` subplot to make plots.
> - `update_plot()`: Updates the plot with the chandes made.
>
> e.g.,
>
> ```python
> plot = self.codification_steps[0].get_plot()
> t = np.arange(0, 3, .01)
> plot.plot(t, 2 * np.sin(2 * np.pi * t))
> self.codification_steps[0].udpate_plot()
> ```

- `configure`: A method that receives the options that the user has configured.

```python
def configure(self, **kwargs) -> None:
    self.option1 = kwargs.get("Option name", "value1")
    self.option2 = kwargs.get("Option name", False)
    self.option3 = kwargs.get("Option name", 5)
```

- `__call__`: A method that receives the image and returns a dictionary with the [codification results](#codification-results).

```python
def __call__(self, image: np.ndarray) -> dict:
    ...
    return {
        "image": image,
        "encoded_image": encoded_image,
        "metrics": {
            "PSNR": psnr,
            "MSE": mse,
            "SSIM": ssim
            ...
        }
    }
```

### Codification options

The options method should return a dictionary with the options that the user can configure. The options are defined by a dictionary with the name of the option as the key and a dictionary that contains the type of the option, the values and the default value.

- `combobox`: A combobox with a list of values. The values are a list of valid values.

```python
{
    "Option name": {
        "type": "combobox",
        "values": ["value1", "value2", "value3"],
        "default": "value1"
    }
}
```

> [!IMPORTANT]  
> The values must always be a list of strings.

- `switch`: A switch with a boolean value as default. No values are needed.

```python
{
    "Option name": {
        "type": "switch",
        "default": False
    }
}
```

- `slider`: A slider with a range of values. The values are a list with the minimum, maximum and the step.

```python
{
    "Option name": {
        "type": "slider",
        "values": [1, 10, 1],
        "default": 5
    }
}
```

### Codification results

The `__call__` method must return a dictionary with the following keys:

- `image`: The visual representation of the image after the codification process.
- `encoded_image`: The encoded image as a binary string.
- `metrics`: A dictionary with the metrics of the codification process. The metrics are defined by a key and a value and should contain at least the PSNR, MSE and SSIM. You can add more metrics if needed and the functions are available in the `metrics.py` file.

```python
{
    "image": image,
    "encoded_image": encoded_image,
    "metrics": {
        "PSNR": psnr,
        "MSE": mse,
        "SSIM": ssim
        ...
    }
}
```
