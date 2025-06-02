import csv
import sys
import json
from typing import List, Union
from model.classes import Regulative, Constitutive

def extract_components(s: str) -> List[str]:
    """
    Extracts components that follow the pattern <SYMBOL>(<INNER_CONTENT>) from a string.
    """
    components = []
    i = 0
    while i < len(s):
        pos = s.find('(', i)
        if pos == -1:
            break
        start = pos - 1
        while start >= 0 and not s[start].isspace():
            start -= 1
        token_start = start + 1
        depth = 0
        j = pos
        while j < len(s):
            if s[j] == '(':
                depth += 1
            elif s[j] == ')':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if j < len(s):
            token = s[token_start:j+1]
            components.append(token)
            i = j + 1
        else:
            break
    return components

def array_to_dict(components: List[str], statement_type: str) -> dict:
    if statement_type == "regulative":
        model_cls = Regulative
    elif statement_type == "constitutive":
        model_cls = Constitutive
    else:
        raise ValueError("Invalid statement_type. Must be 'regulative' or 'constitutive'.")

    instance = model_cls()
    field_map = {
        (field.alias or name): name
        for name, field in model_cls.model_fields.items()
    }

    for token in components:
        if "(" in token and token.endswith(")"):
            symbol, inner = token.split("(", 1)
            inner = inner.rsplit(")", 1)[0].strip()
            symbol = symbol.strip()
            if symbol in field_map:
                # Initialize the field to an empty list if it is None.
                current_value = getattr(instance, field_map[symbol])
                if current_value is None:
                    setattr(instance, field_map[symbol], [])
                getattr(instance, field_map[symbol]).append(inner)

    return instance.to_dict()

def format_classification(input_text: str, statement_type: str) -> dict:
    return {
        "input": input_text,
        "type": statement_type
    }

def format_components(input_text: str, output_text: str, statement_type: str) -> dict:
    components = extract_components(output_text)
    parsed = array_to_dict(components, statement_type)
    return {
        "input": input_text,
        "expected_components": parsed
    }

def csv_to_json(file_path: str, statement_type: str, classification: bool = False) -> List[dict]:
    """
    Converts a CSV file to a list of JSON objects, with optional classification mode.
    """
    output = []
    formatter = format_classification if classification else format_components

    with open(file_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if not all(k in row for k in ("Input", "Output")):
                continue
            input_text = row["Input"].strip()
            output_text = row["Output"].strip()
            formatted = formatter(input_text, statement_type) if classification else formatter(input_text, output_text, statement_type)
            output.append(formatted)

    return output

if __name__ == "__main__":
    # CLI usage: python convert_to_json.py input.csv regulative [--classification]
    if len(sys.argv) < 3:
        print("Usage: python convert_to_json.py <input_csv_file> <statement_type> [--classification]")
        sys.exit(1)

    file_path = sys.argv[1]
    statement_type = sys.argv[2].lower()
    classification_flag = "--classification" in sys.argv

    try:
        result = csv_to_json(file_path, statement_type, classification=classification_flag)
        print(json.dumps(result, indent=4))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
