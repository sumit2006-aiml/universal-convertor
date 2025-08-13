# Universal Python Converter

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A versatile Python utility for converting between various data types and formats with a unified interface.

## Features

- **Type Conversions**: String ↔ Integer, Float, Boolean
- **Date/Time**: String ↔ Datetime objects
- **Data Formats**: 
  - JSON ↔ Python dictionaries
  - YAML ↔ Python dictionaries (requires PyYAML)
  - XML ↔ Python dictionaries (basic implementation)
- **Encoding**: String ↔ Base64
- **Unified API**: Single `convert()` method for all operations
- **Error Handling**: Consistent validation and error reporting

## Installation

```bash
pip install pyyaml  # Required for YAML support
```

## Quick Start

```python
from universal_converter import UniversalConverter

converter = UniversalConverter()

# Basic type conversion
num = converter.convert("42", "str", "int")
bool_val = converter.convert("true", "str", "bool")

# JSON handling
json_dict = converter.convert('{"name": "Alice"}', "json", "dict")
json_str = converter.convert({"name": "Alice"}, "dict", "json")

# Date conversion
dt = converter.convert("2023-01-01", "str", "datetime", fmt="%Y-%m-%d")
```

## API Reference

### `convert(value, from_type, to_type, **kwargs)`

Main conversion method that routes to specific converters.

**Parameters:**
- `value`: Input value to convert
- `from_type`: Source type (`str`, `int`, `float`, `bool`, `json`, `yaml`, `xml`, `datetime`, `base64`)
- `to_type`: Target type (same as `from_type` options plus `dict`)
- `**kwargs`: Format-specific options (e.g., `fmt` for datetime formats)

**Returns:** Converted value

**Raises:** `ValueError` for unsupported conversions or invalid inputs

### Direct Methods

All conversion methods are also available as static methods:

```python
UniversalConverter.str_to_int("42")
UniversalConverter.dict_to_json({"key": "value"}, indent=2)
# etc.
```

## Supported Conversions

| From Type | To Type | Notes |
|-----------|---------|-------|
| str       | int     |       |
| str       | float   |       |
| str       | bool    | Accepts 'true'/'false', '1'/'0', etc. |
| str       | datetime | Requires format string (`fmt` kwarg) |
| str       | base64  |       |
| int       | str     |       |
| float     | str     |       |
| bool      | str     |       |
| datetime  | str     | Requires format string (`fmt` kwarg) |
| base64    | str     |       |
| json      | dict    |       |
| dict      | json    | Accepts `indent` kwarg |
| yaml      | dict    | Requires PyYAML |
| dict      | yaml    | Requires PyYAML |
| xml       | dict    | Basic implementation |
| dict      | xml     | Basic implementation, accepts `root_tag` kwarg |

## Examples

### Working with Configuration Files

```python
# Convert YAML config to JSON
yaml_config = """
app:
  name: MyApp
  port: 8000
"""
json_config = converter.convert(
    converter.convert(yaml_config, "yaml", "dict"),
    "dict", "json", indent=2
)
```

### API Response Processing

```python
# Convert XML API response to Python dict
xml_response = "<user><id>123</id><name>John Doe</name></user>"
user_data = converter.convert(xml_response, "xml", "dict")
```
