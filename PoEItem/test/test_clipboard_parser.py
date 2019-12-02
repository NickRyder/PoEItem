from PoEItem.clipboard_parser import parse_clipboard_text


def test_parse_clipboard_text():
    import os
    import base64

    script_dir = os.path.dirname(__file__)
    rel_path = "itemstextdata.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    rarity_to_keys = {}
    with open(abs_file_path, "r") as file:
        for line in file:
            if line != "\n":
                clipboard_entry = base64.b64decode(line).decode("utf-8")
                parse_clipboard_text(clipboard_entry)
                # if "Rarity: Rare" in clipboard_entry:
                #     print(clipboard_entry)
    print(rarity_to_keys.keys())


if __name__ == "__main__":
    test_parse_clipboard_text()
