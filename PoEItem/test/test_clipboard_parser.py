from PoEItem.clipboard_parser import parse_clipboard_text


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
    rel_path = "itemsfullsetdata.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    rarity_to_keys = {}
    with open(abs_file_path, "r") as file:
        json_data = json.load(file)
    item_keys = set()
    name_to_type = {}
    type_to_name = {}
    for entry in json_data:
        clipboard_entry = base64.b64decode(entry["item"]["extended"]["text"]).decode(
            "utf-8"
        )
        # parse_clipboard_text(clipboard_entry)
        combined_properties = (
            entry["item"].get("properties", [])
            + entry["item"].get("additionalProperties", [])
            + entry["item"].get("nextLevelRequirements", [])
            + entry["item"].get("requirements", [])
        )
        for property in combined_properties:
            name = property.get("name")
            type = property.get("type", "")
            if type != "":
                if name not in name_to_type:
                    name_to_type[name] = set()
                if type not in type_to_name:
                    type_to_name[type] = set()
                type_to_name[type].add(name)
                name_to_type[name].add(type)
        item_keys = item_keys.union(set(entry["item"].keys()))
    print(type_to_name)
    print(name_to_type)
    print(item_keys)
    to_return = []
    for i in range(1, 30):
        try:
            to_return.append(type_to_name[i].pop())
        except KeyError:
            to_return.append(None)
    print(to_return)


if __name__ == "__main__":
    test_parse_clipboard_text()
