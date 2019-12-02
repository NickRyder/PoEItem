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
                named, unnamed = parse_clipboard_text(clipboard_entry)
                rarity = named["Rarity"]
                if rarity not in rarity_to_keys:
                    rarity_to_keys[rarity] = set()
                rarity_to_keys[rarity] = rarity_to_keys[rarity].union(set(named.keys()))
                if rarity == "Rare":
                    print(clipboard_entry)
                assert "Rarity" in named.keys(), print(repr(clipboard_entry))
    print(rarity_to_keys.keys())


if __name__ == "__main__":
    test_parse_clipboard_text()
