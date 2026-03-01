import json


def parse_gpt_output(json_path: str) -> str:
    """
    Load the GPT JSON file and extract the markdown string from 'gptOutput'.
    Raises ValueError if the field is missing or empty.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    gpt_output = data.get("gptOutput", "").strip()

    if not gpt_output:
        raise ValueError(f"'gptOutput' field is missing or empty in {json_path}")

    return gpt_output
