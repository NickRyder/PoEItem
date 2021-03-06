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
            for sub_number_1, sub_number_2 in zip(sub_numbers_1, sub_numbers_2):
                if (sub_number_1 is None) != (sub_number_2 is None):
                    print(s1)
                    print(s2)
                    break


def validate_value_stat_entry(string_values, stat_translation_entry):
    """throws a ValueError if conditions are not met with given value"""
    raise NotImplementedError("Need to handle ignore format")

    final_values = []
    assert len(string_values) == len(
        stat_translation_entry["format"]
    ), "value length doesnt match entry"

    string_value_idx = 0
    for format_, index_handler, condition in zip(
        stat_translation_entry["format"],
        stat_translation_entry["index_handlers"],
        stat_translation_entry["condition"],
    ):
        if format_ != "ignore":
            value = float(string_values[string_value_idx])
            for handler in index_handler:
                value *= index_handlers[handler]
            value = int(value)

            if "min" in condition and condition["min"] > value:
                raise ValueError(
                    f"min condition not met : {value} < {condition['min']}"
                )
            if "max" in condition and condition["max"] < value:
                raise ValueError(
                    f"max condition not met : {value} > {condition['max']}"
                )
            final_values.append(value)
            string_value_idx += 1
        else:
            final_values.append(None)

    return final_values


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

        for stat_translation_entry in stat_english:
            text_splits, sub_numbers, text_numbers = _split_stat_translation(
                stat_translation_entry["string"]
            )

            if explicit_splits == text_splits:
                string_values = []
                try:
                    for sub_index, text_number, explicit_number in zip(
                        sub_numbers, text_numbers, explicit_numbers
                    ):

                        # assert all numbers in pattern not in {} agree with query string
                        if text_number is not None:
                            if text_number != explicit_number:
                                raise ValueError(
                                    "numbers from the stat itself dont match"
                                )
                        else:
                            string_values.append(explicit_number)

                    final_values = validate_value_stat_entry(
                        string_values, stat_translation_entry
                    )
                    stat_entry = {}
                    for stat_id, value in zip(stat["ids"], final_values):
                        stat_entry[stat_id] = value
                    possible_stat_results.append(stat_entry)
                except Exception:
                    pass
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


def _validate_duplicate_stat_strings():
    """

    """

    all_stat_strings = set()
    stat_string_groups = set()
    for stat_translation in stat_translations:
        if "English" in stat_translation:
            stat_group = set()

            english_stat_translation = stat_translation["English"]

            check_stat_group = False
            for stat_translation_entry in english_stat_translation:
                string = stat_translation_entry["string"]
                if string in all_stat_strings:
                    check_stat_group = True
                stat_group.add(string)
            if check_stat_group:
                assert (
                    frozenset(stat_group) in stat_string_groups
                ), f"stat_translation in two separate groups: {stat_group}"
            all_stat_strings |= stat_group
            stat_string_groups.add(frozenset(stat_group))


def _validate_ignore_format():
    for stat_translation in stat_translations:
        if "English" in stat_translation:
            english_stat_translation = stat_translation["English"]
            for translation_entry in english_stat_translation:
                conditions = translation_entry["condition"]
                formats = translation_entry["format"]
                index_handlers = translation_entry["index_handlers"]
                for condition, format_, index_handler in zip(
                    conditions, formats, index_handlers
                ):
                    if format_ == "ignore":
                        pass


def _find_duplicate_strat_translations():
    """
    Finds all stat strings that show up in two mulitple stat ids
    """
    strings = set()
    for stat_translation in stat_translations:
        english_stat_translation = stat_translation["English"]
        for translation_entry in english_stat_translation:
            groups = re.split(
                f"{re_insert_pattern}|{re_number_pattern}", translation_entry["string"]
            )
            entry = (len(stat_translation["ids"]), tuple(groups[::3]))
            if entry in strings:
                print(entry)
            else:
                strings.add(entry)


def _validate_no_stat_overlap_in_stat_translations():
    """
    This validates that every stat shows up in only one stat translations
    """
    for stat_translation_1, stat_translation_2 in tqdm(
        itertools.combinations(stat_translations, 2),
        total=len(stat_translations) * (len(stat_translations) - 1) / 2,
    ):
        assert not set(stat_translation_1["ids"]) & set(
            stat_translation_2["ids"]
        ), f"stat with multiple translations {stat_translation_1['ids']}, {stat_translation_2['ids']}"


def _validate_index_handlers_duplicates():
    """ searches through stat translations for inconsistent format entries """
    for stat_translation in stat_translations:
        english_stat_translation = stat_translation["English"]
        translation_string_to_index_handlers = {}
        for translation_entry in english_stat_translation:
            string = translation_entry["string"]
            index_handlers = tuple(translation_entry["index_handlers"])
            if string in translation_string_to_index_handlers:
                if index_handlers != translation_string_to_index_handlers[string]:
                    print("#######")
                    print(string)
                    print(index_handlers)
                    print(translation_string_to_index_handlers[string])
            translation_string_to_index_handlers[string] = index_handlers


def get_condition_pairs():
    condition_pairs = set()
    for stat_translation in stat_translations:
        english_stat_translation = stat_translation["English"]
        for translation_entry in english_stat_translation:
            for condition in translation_entry["condition"]:
                min_ = condition.get("min", None)
                max_ = condition.get("max", None)
                condition_pairs.add((min_, max_))
    return condition_pairs


if __name__ == "__main__":
    # _validate_no_stat_overlap_in_stat_translations()
    # get_condition_pairs()
    _validate_index_handlers_duplicates()
    # _find_duplicate_strat_translations()
    # _return_possible_stats_from_explicit_line("+8 to Strength")
    # _return_possible_stats_from_explicit_line("Regenerate 5.1 Mana per second")
    # _return_possible_stats_from_explicit_line(
    #     "Totems gain +9% to all Elemental Resistances"
    # )
    # _return_possible_stats_from_explicit_line("Adds 8 to 9 Physical Damage")
    # _return_possible_stats_from_explicit_line("4% reduced Mana Cost of Skills")
    # _return_possible_stats_from_explicit_line("6% reduced Mana Reserved")
    # _return_possible_stats_from_explicit_line("Has -1 Abyssal Sockets")
    # _return_possible_stats_from_explicit_line(
    #     "Adds 1 to 160 Lightning Damage if you haven't Killed Recently"
    # )
    # from PoEItem.clipboard_parser import rare_stats
    # from itertools import chain

    # for key, value in _find_duplicate_stat_translations(rare_stats).items():
    #     for sub_key in set(chain.from_iterable(value)):
    #         if "local" in sub_key:
    #             break
    #     else:
    #         print(key, value)
