#building this mainly for line 4, but also in future when
#I want to incorporate more seasons this map will come in handy
ESPN_ABBREV_MAP = {
    "WSH": "WAS",
    "LA": "LAR",
    "STL": "LAR",
    "SD": "LAC",
    "OAK": "LV",
    "ARZ" : "ARI",
    "BLT": "BAL",
    "CLV": "CLE",
    "HST": "HOU"
}


def normalize_abbrev(abbrev):
    return ESPN_ABBREV_MAP.get(abbrev, abbrev)