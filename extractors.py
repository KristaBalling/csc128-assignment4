"""
CSC-128 Assignment 4: entity extraction
Krista Balling
"""

import re

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday",
        "saturday", "sunday"]

NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def find_room(text):
    """TODO 1: find and return a three-digit room number as a string, or None."""
    match = re.search(r"\broom\s+(\d{3})\b", text.lower())
    if match:
        return match.group(1)
    return None


def strip_room(text):
    """
    TODO 2: remove the room number from the text.

    Read the warning in the Week 4 page first. If you do not do this,
    find_time will read "room 214" as 2:14 and your bot will book the
    wrong time.
    """
    cleaned = re.sub(r"\broom\s+\d{3}\b", "", text, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", cleaned).strip()


def find_day(text):
    """TODO 3: return a capitalized weekday name, or None."""
    lowered = text.lower()

    for day in DAYS:
        if day in lowered:
            return day.capitalize()

    return None


def find_time(text):
    """TODO 4: handle 3pm, 3 pm, 3:30pm, and 15:00. Return None if absent."""
    lowered = text.lower()

    match = re.search(
        r"\b(\d{1,2}):(\d{2})\s*(am|pm)?\b",
        lowered
    )

    if match:
        hour = match.group(1)
        minute = match.group(2)
        period = match.group(3) or ""
        return f"{hour}:{minute}{period}"

    match = re.search(
        r"\b(\d{1,2})\s*(am|pm)\b",
        lowered
    )

    if match:
        hour = match.group(1)
        period = match.group(2)
        return f"{hour}:00{period}"

    return None


def find_party_size(text):
    """TODO 5: handle "4 people", "four people", and "just me"."""
    lowered = text.lower().strip()

    if "just me" in lowered:
        return 1

    match = re.search(r"\b(\d+)\s*(people|person|of us)\b", lowered)
    if match:
        return int(match.group(1))

    for word, value in NUMBER_WORDS.items():
        if re.search(rf"\b{word}\b\s*(people|person|of us)\b", lowered):
            return value
        if re.search(rf"\b{word}\b", lowered):
            return value

    return None


def extract_all(text):
    """TODO 6: run every extractor in the correct order and return a dict."""
    room = find_room(text)
    cleaned = strip_room(text)

    return {
        "room": room,
        "day": find_day(cleaned),
        "time": find_time(cleaned),
        "party_size": find_party_size(cleaned)
    }