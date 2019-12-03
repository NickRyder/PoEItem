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
    import os
    import base64
    import json

    script_dir = os.path.dirname(__file__)
    rel_path = "standarditemdataset.txt"

    abs_file_path = os.path.join(script_dir, rel_path)
    rarity_to_keys = {}
    with open(abs_file_path, "r") as file:
        json_data = json.load(file)
    item_keys = set()
    socket_attr = set()
    socket_color = set()
    test = {"A": "A", "D": "G", "I": "B", "S": "R", "G": "W"}
    for entry in json_data:

        clipboard_entry = base64.b64decode(entry["item"]["extended"]["text"]).decode(
            "utf-8"
        )
        socket_attr.add(entry["item"].get("frameType", ""))
        if entry["item"].get("frameType", "") == 9:
            print(clipboard_entry)

    print(socket_attr)
    print(socket_color)
    # item = PoEItem()
    # for key in item_keys:
    #     getattr(item, key)


if __name__ == "__main__":
    test_parse_clipboard_text()
