from RePoE import stat_translations
from RePoE import mods

index_handlers = {
    "negate": -1,
    "canonical_stat": 1,
    "divide_by_fifteen_0dp": 15,
    "per_minute_to_per_second_1dp": 60,
    "divide_by_twenty_then_double_0dp": 10,
    "60%_of_value": 5.0 / 3,
    "divide_by_one_hundred_2dp": 100,
    "milliseconds_to_seconds_0dp": 1000,
    "per_minute_to_per_second_2dp_if_required": 60,
    "deciseconds_to_seconds": 10,
    "divide_by_ten_0dp": 10,
    "multiplicative_damage_modifier": 1,
    "milliseconds_to_seconds": 1000,
    "mod_value_to_item_class": 1,
    "old_leech_percent": 1,
    "old_leech_permyriad": 10000,
    "30%_of_value": 10.0 / 3,
    "per_minute_to_per_second_0dp": 60,
    "per_minute_to_per_second": 60,
    "divide_by_two_0dp": 2,
    "milliseconds_to_seconds_2dp": 1000,
    "divide_by_one_hundred": 100,
    "per_minute_to_per_second_2dp": 60,
    "divide_by_twelve": 10,
    "divide_by_six": 6,
    "times_twenty": 1 / 20,
}

formats = ["#%", "+#%", "+#", "#"]


import re


def _return_possible_stats_from_explicit_line(explicit_line):
    re_number_pattern = r"\+?(-?\d+\.?\d*)\%?"

    re_result = re.split(re_number_pattern, explicit_line)
    explicit_splits = re_result[::2]
    explicit_numbers = re_result[1::2]
    possible_stat_results = []
    for stat in stat_translations:
        stat_english = stat["English"]

        for stat_entry in stat_english:
            stat_splits = re.split(
                r"\+?-?{(\d+)}\%?|" + re_number_pattern, stat_entry["string"]
            )
            text_splits = stat_splits[::3]

            if explicit_splits == text_splits:
                sub_numbers = stat_splits[1::3]
                text_numbers = stat_splits[2::3]
                valid_entry = True
                values = []
                for sub_index, text_number, explicit_number in zip(
                    sub_numbers, text_numbers, explicit_numbers
                ):
                    if text_number is not None:
                        if text_number != explicit_number:
                            valid_entry = False
                    else:
                        format_str = stat_entry["format"][int(sub_index)]

                        # if "%" == format_str[-1]:
                        #     if explicit_number[-1] != "%":
                        #         valid_entry = False
                        #     explicit_number = explicit_number[:-1]

                        # if (explicit_number[0] not in ["+", "-"]) != (
                        #     format_str[0] not in ["+", "-"]
                        # ):
                        #     valid_entry = False

                        value = float(explicit_number)
                        for index_handler in stat_entry["index_handlers"][
                            int(sub_index)
                        ]:
                            value *= index_handlers[index_handler]
                        value = int(value)

                        conditions = stat_entry["condition"][int(sub_index)]
                        if "min" in conditions and conditions["min"] > value:
                            valid_entry = False
                        if "max" in conditions and conditions["max"] < value:
                            valid_entry = False

                        values.append(value)
                if valid_entry:
                    stat_entry = {}
                    for stat_id, value in zip(stat["ids"], values):
                        stat_entry[stat_id] = value
                    possible_stat_results.append(stat_entry)
    print(possible_stat_results)
    return possible_stat_results


from collections import Counter, defaultdict


def _find_duplicate_stat_translations(stat_id_pool):
    """

    """

    string_to_stats = defaultdict(list)
    for stat_translation in stat_translations:
        if "English" in stat_translation and set(stat_translation["ids"]).issubset(
            stat_id_pool
        ):
            english_stat_translation = stat_translation["English"]
            for stat_translation_entry in english_stat_translation:
                string = stat_translation_entry["string"]
            string_to_stats[string] += [set(stat_translation["ids"])]

    output = {}
    for key, value in string_to_stats.items():
        if len(value) > 1:
            output[key] = value
    return output


if __name__ == "__main__":
    # test inputs

    _return_possible_stats_from_explicit_line("+8 to Strength")
    _return_possible_stats_from_explicit_line("Regenerate 5.1 Mana per second")
    _return_possible_stats_from_explicit_line(
        "Totems gain +9% to all Elemental Resistances"
    )
    _return_possible_stats_from_explicit_line("Adds 8 to 9 Physical Damage")
    _return_possible_stats_from_explicit_line("4% reduced Mana Cost of Skills")
    _return_possible_stats_from_explicit_line("6% reduced Mana Reserved")
    _return_possible_stats_from_explicit_line("Has -1 Abyssal Sockets")
    _return_possible_stats_from_explicit_line(
        "Adds 1 to 160 Lightning Damage if you haven't Killed Recently"
    )
    from PoEItem.clipboard_parser import rare_stats
    from itertools import chain

    for key, value in _find_duplicate_stat_translations(rare_stats).items():
        for sub_key in set(chain.from_iterable(value)):
            if "local" in sub_key:
                break
        else:
            print(key, value)
