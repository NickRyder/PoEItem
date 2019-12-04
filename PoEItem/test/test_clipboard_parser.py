from PoEItem.clipboard_parser import parse_clipboard_text
from PoEItem.poe_item import PoEItem

# def test_parse_clipboard_text():
#     import os
#     import base64

#     script_dir = os.path.dirname(__file__)
#     rel_path = "itemstextdata.txt"
#     abs_file_path = os.path.join(script_dir, rel_path)
#     rarity_to_keys = {}
#     with open(abs_file_path, "r") as file:
#         for line in file:
#             if line != "\n":
#                 clipboard_entry = base64.b64decode(line).decode("utf-8")
#                 parse_clipboard_text(clipboard_entry)
#                 # if "Rarity: Rare" in clipboard_entry:
#                 #     print(clipboard_entry)
#     print(rarity_to_keys.keys())

def test_parse_clipboard_text():
    
    example = None


    import os
    import base64
    import json

    script_dir = os.path.dirname(__file__)
    rel_path = "itemsfullsetdata.txt"

    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        json_data = json.load(file)
    for entry in json_data:

        clipboard_entry = base64.b64decode(entry["item"]["extended"]["text"]).decode(
            "utf-8"
        )
        parse_clipboard_text(clipboard_entry)
        if "delve" in entry["item"]:
            example = clipboard_entry
    print(example)


if __name__ == "__main__":
    test_parse_clipboard_text()
