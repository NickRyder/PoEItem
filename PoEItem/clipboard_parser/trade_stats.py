import json
import requests
import itertools

_STATS_URL = "https://www.pathofexile.com/api/trade/data/stats"

stats = requests.get(_STATS_URL).json()["result"]

stat_entries_list = [stat["entries"] for stat in stats]

stat_entries = itertools.chain.from_iterable(stat_entries_list)

stat_keys = set()
for stat_entry in stat_entries:
    if "option" in stat_entry:
        print(stat_entry["text"])
print(stat_keys)


# def extract_values()