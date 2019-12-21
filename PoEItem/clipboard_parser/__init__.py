from RePoE import mods, base_items


implicit_mods = set()
for item in base_items.values():
    for implicit_mod in item["implicits"]:
        implicit_mods.add(implicit_mod)
print(implicit_mods)

unique_mods = set()
rare_mods = set()
enchantment_mods = set()

for mod_name, mod_value in mods.items():
    if mod_value["generation_type"] == "enchantment":
        enchantment_mods.add(mod_name)
    elif (
        mod_value["generation_type"] in ["prefix", "suffix"]
        and mod_value["domain"] != "atlas"
    ):
        rare_mods.add(mod_name)
    elif mod_value["generation_type"] == "unique":
        unique_mods.add(mod_name)
unique_mods = unique_mods.difference(implicit_mods)


def mods_to_stats(mod_names):
    ids = set()
    for mod_name in mod_names:
        mod_value = mods[mod_name]
        for stat in mod_value["stats"]:
            ids.add(stat["id"])
    return ids


implicit_stats = mods_to_stats(implicit_mods)
unique_stats = mods_to_stats(unique_mods)
rare_stats = mods_to_stats(rare_mods)
enchantment_stats = mods_to_stats(enchantment_mods)


##### CONSTANTS

# override_enchant_stats =


print(rare_stats)
