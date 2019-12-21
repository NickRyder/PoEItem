from RePoE import stat_translations
from RePoE import mods
from tqdm import tqdm

import re
import itertools

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


re_number_pattern = r"\+?(-?\d+\.?\d*)\%?"
re_insert_pattern = r"\+?-?{(\d+)}\%?"


def _split_stat_translation(stat_translation):
    """
    takes in stat_translation and spits out 
    string
    sub_numbers
    text_numbers
    """
    stat_splits = re.split(f"{re_insert_pattern}|{re_number_pattern}", stat_translation)
    text_splits = stat_splits[::3]
    sub_numbers = stat_splits[1::3]
    text_numbers = stat_splits[2::3]
    return text_splits, sub_numbers, text_numbers


def _validate_stat_translation():
    """

    """

    translation_strings = set()
    for stat_translation in stat_translations:
        if "English" in stat_translation:
            english_stat_translation = stat_translation["English"]
            for stat_translation_entry in english_stat_translation:
                translation_strings.add(stat_translation_entry["string"])
    split_strings = [_split_stat_translation(s) for s in translation_strings]
    for s1, s2 in itertools.combinations(split_strings, 2):
        text_splits_1, sub_numbers_1, text_numbers_1 = s1
        text_splits_2, sub_numbers_2, text_numbers_2 = s2
        if text_splits_1 == text_splits_2:
            print(s1)
            print(s2)


def _return_possible_stats_from_explicit_line(explicit_line):
    """
    takes in explicit line
    first removes all numeric values (including +/-/%)
    
    """

    re_result = re.split(re_number_pattern, explicit_line)
    explicit_splits = re_result[::2]
    explicit_numbers = re_result[1::2]
    possible_stat_results = []
    for stat in stat_translations:
        stat_english = stat["English"]

        for stat_entry in stat_english:
            text_splits, sub_numbers, text_numbers = _split_stat_translation(
                stat_entry["string"]
            )

            if explicit_splits == text_splits:
                values = []
                for sub_index, text_number, explicit_number in zip(
                    sub_numbers, text_numbers, explicit_numbers
                ):
                    # assert all numbers in pattern not in {} agree with query string
                    if text_number is not None:
                        if text_number != explicit_number:
                            break
                    else:
                        format_str = stat_entry["format"][int(sub_index)]

                        value = float(explicit_number)
                        for index_handler in stat_entry["index_handlers"][
                            int(sub_index)
                        ]:
                            value *= index_handlers[index_handler]
                        value = int(value)

                        conditions = stat_entry["condition"][int(sub_index)]
                        if "min" in conditions and conditions["min"] > value:
                            break
                        if "max" in conditions and conditions["max"] < value:
                            break

                        values.append(value)
                else:
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
    _validate_stat_translation()
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
