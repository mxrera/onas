# Contributing

## Adding codification algorithms

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

- `checkbox`: A checkbox with a boolean value. No values are needed.

```python
{
    "Option name": {
        "type": "checkbox",
        "default": False
    }
}
```

- `spinbox`: A spinbox with a range of values. The values are a list with the minimum, maximum and step.

```python
{
    "Option name": {
        "type": "spinbox",
        "values": [1, 10, 1],
        "default": 5
    }
}
```
