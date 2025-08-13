import json
import yaml  # requires PyYAML package
import xml.etree.ElementTree as ET
from datetime import datetime
import base64
import binascii

class UniversalConverter:
    """
    A universal converter that handles various data format conversions in Python.
    """
    
    @staticmethod
    def str_to_int(value: str) -> int:
        """Convert string to integer with error handling."""
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert '{value}' to integer")

    @staticmethod
    def str_to_float(value: str) -> float:
        """Convert string to float with error handling."""
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert '{value}' to float")

    @staticmethod
    def str_to_bool(value: str) -> bool:
        """Convert string to boolean (case-insensitive, handles common variants)."""
        true_values = ['true', '1', 't', 'y', 'yes', 'on']
        false_values = ['false', '0', 'f', 'n', 'no', 'off']
        
        if str(value).lower() in true_values:
            return True
        elif str(value).lower() in false_values:
            return False
        else:
            raise ValueError(f"Cannot convert '{value}' to boolean")

    @staticmethod
    def json_to_dict(json_str: str) -> dict:
        """Convert JSON string to Python dictionary."""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    @staticmethod
    def dict_to_json(py_dict: dict, indent: int = None) -> str:
        """Convert Python dictionary to JSON string."""
        try:
            return json.dumps(py_dict, indent=indent)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Dictionary to JSON conversion failed: {e}")

    @staticmethod
    def yaml_to_dict(yaml_str: str) -> dict:
        """Convert YAML string to Python dictionary."""
        try:
            return yaml.safe_load(yaml_str)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}")

    @staticmethod
    def dict_to_yaml(py_dict: dict) -> str:
        """Convert Python dictionary to YAML string."""
        try:
            return yaml.dump(py_dict)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Dictionary to YAML conversion failed: {e}")

    @staticmethod
    def xml_to_dict(xml_str: str) -> dict:
        """Convert XML string to Python dictionary (simple implementation)."""
        try:
            root = ET.fromstring(xml_str)
            return UniversalConverter._xml_element_to_dict(root)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {e}")

    @staticmethod
    def _xml_element_to_dict(element) -> dict:
        """Helper method to convert XML element to dictionary."""
        result = {}
        if element.attrib:
            result.update(element.attrib)
        if element.text and element.text.strip():
            result['_text'] = element.text.strip()
        
        for child in element:
            child_data = UniversalConverter._xml_element_to_dict(child)
            if child.tag in result:
                if isinstance(result[child.tag], list):
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = [result[child.tag], child_data]
            else:
                result[child.tag] = child_data
        return result

    @staticmethod
    def dict_to_xml(py_dict: dict, root_tag: str = 'root') -> str:
        """Convert Python dictionary to XML string (simple implementation)."""
        try:
            root = ET.Element(root_tag)
            UniversalConverter._dict_to_xml_element(py_dict, root)
            return ET.tostring(root, encoding='unicode')
        except (TypeError, ValueError) as e:
            raise ValueError(f"Dictionary to XML conversion failed: {e}")

    @staticmethod
    def _dict_to_xml_element(data, parent):
        """Helper method to convert dictionary to XML element."""
        if isinstance(data, dict):
            for key, value in data.items():
                if key == '_text':
                    parent.text = str(value)
                elif isinstance(value, list):
                    for item in value:
                        elem = ET.SubElement(parent, key)
                        UniversalConverter._dict_to_xml_element(item, elem)
                else:
                    elem = ET.SubElement(parent, key)
                    UniversalConverter._dict_to_xml_element(value, elem)
        else:
            parent.text = str(data)

    @staticmethod
    def str_to_datetime(date_str: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> datetime:
        """Convert string to datetime object using specified format."""
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError as e:
            raise ValueError(f"Date string doesn't match format '{fmt}': {e}")

    @staticmethod
    def datetime_to_str(dt: datetime, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
        """Convert datetime object to string using specified format."""
        try:
            return dt.strftime(fmt)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Datetime to string conversion failed: {e}")

    @staticmethod
    def str_to_base64(text: str, encoding: str = 'utf-8') -> str:
        """Encode string to Base64."""
        try:
            return base64.b64encode(text.encode(encoding)).decode(encoding)
        except (UnicodeError, binascii.Error) as e:
            raise ValueError(f"Base64 encoding failed: {e}")

    @staticmethod
    def base64_to_str(b64_str: str, encoding: str = 'utf-8') -> str:
        """Decode Base64 string to original text."""
        try:
            return base64.b64decode(b64_str).decode(encoding)
        except (UnicodeError, binascii.Error) as e:
            raise ValueError(f"Base64 decoding failed: {e}")

    @staticmethod
    def convert(value, from_type: str, to_type: str, **kwargs):
        """
        Universal conversion method that routes to specific converters.
        
        Args:
            value: Input value to convert
            from_type: Source type ('str', 'int', 'float', 'bool', 'json', 'yaml', 'xml', 'datetime', 'base64')
            to_type: Target type ('str', 'int', 'float', 'bool', 'dict', 'json', 'yaml', 'xml', 'datetime', 'base64')
            **kwargs: Additional arguments for specific converters
            
        Returns:
            Converted value
            
        Raises:
            ValueError: If conversion is not supported or fails
        """
        conversion_key = f"{from_type}_to_{to_type}"
        
        converters = {
            'str_to_int': UniversalConverter.str_to_int,
            'str_to_float': UniversalConverter.str_to_float,
            'str_to_bool': UniversalConverter.str_to_bool,
            'str_to_datetime': UniversalConverter.str_to_datetime,
            'str_to_base64': UniversalConverter.str_to_base64,
            'int_to_str': str,
            'float_to_str': str,
            'bool_to_str': str,
            'datetime_to_str': UniversalConverter.datetime_to_str,
            'base64_to_str': UniversalConverter.base64_to_str,
            'json_to_dict': UniversalConverter.json_to_dict,
            'dict_to_json': UniversalConverter.dict_to_json,
            'yaml_to_dict': UniversalConverter.yaml_to_dict,
            'dict_to_yaml': UniversalConverter.dict_to_yaml,
            'xml_to_dict': UniversalConverter.xml_to_dict,
            'dict_to_xml': UniversalConverter.dict_to_xml,
        }
        
        if conversion_key in converters:
            return converters[conversion_key](value, **kwargs)
        else:
            raise ValueError(f"Unsupported conversion from {from_type} to {to_type}")


# Example usage
if __name__ == "__main__":
    converter = UniversalConverter()
    
    # String conversions
    print("String to int:", converter.convert("42", "str", "int"))
    print("String to float:", converter.convert("3.14", "str", "float"))
    print("String to bool:", converter.convert("true", "str", "bool"))
    
    # JSON conversions
    json_str = '{"name": "Alice", "age": 30}'
    json_dict = converter.convert(json_str, "json", "dict")
    print("JSON to dict:", json_dict)
    print("Dict to JSON:", converter.convert(json_dict, "dict", "json", indent=2))
    
    # Date conversion
    date_str = "2023-05-15 14:30:00"
    date_obj = converter.convert(date_str, "str", "datetime", fmt="%Y-%m-%d %H:%M:%S")
    print("String to datetime:", date_obj)
    print("Datetime to string:", converter.convert(date_obj, "datetime", "str"))
    
    # Base64 conversion
    original = "Hello World!"
    encoded = converter.convert(original, "str", "base64")
    print("String to Base64:", encoded)
    print("Base64 to string:", converter.convert(encoded, "base64", "str"))