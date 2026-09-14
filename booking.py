"""
CSC-128 Assignment 4: slot-filling logic
Krista Balling
"""

from extractors import extract_all

REQUIRED = ["day", "time", "party_size"]

PROMPTS = {
    "day": "What day do you need the room?",
    "time": "What time works for you?",
    "party_size": "How many people will be using it?"
}

def next_missing_slot(slots):
    """Return the first required slot that is still empty."""
    for name in REQUIRED:
        if slots.get(name) is None:
            return name
    return None

CORRECTION_WORDS = ["actually", "no wait", "change that", "instead", "i meant"]


def is_correction(text):
    lowered = text.lower()
    return any(word in lowered for word in CORRECTION_WORDS)

def handle(text, slots):
    """Collect slot values, handle corrections, and return the next response."""
    lowered = text.lower().strip()

    if next_missing_slot(slots) is None:
        if lowered in ["yes", "y", "confirm"]:
            room_text = ""
            if slots.get("room"):
                room_text = f" in room {slots['room']}"

            return (
                f"Confirmed! Your booking is set for {slots['day']} "
                f"at {slots['time']} for {slots['party_size']}{room_text}.",
                slots
            )

        if lowered in ["no", "n", "nope"]:
            return "Okay. Tell me what you'd like to change.", slots
    corrected = False

    if is_correction(text):
        lowered = text.lower()
        positions = [
            lowered.find(word)
            for word in CORRECTION_WORDS
            if word in lowered
        ]
        start = min(positions)
        correction_text = text[start:]
        extracted = extract_all(correction_text)

        for name, value in extracted.items():
            if value is not None:
                slots[name] = value
                corrected = True
    else:
        extracted = extract_all(text)

        for name, value in extracted.items():
            if slots.get(name) is None and value is not None:
                slots[name] = value

    if is_correction(text):
        for name, value in extracted.items():
            if value is not None:
                slots[name] = value
                corrected = True
    else:
        for name, value in extracted.items():
            if slots.get(name) is None and value is not None:
                slots[name] = value

    missing = next_missing_slot(slots)

    if missing:
        response = PROMPTS[missing]
        if corrected:
            response = f"Updated. {response}"
        return response, slots

    room_text = ""
    if slots.get("room"):
        room_text = f" in room {slots['room']}"

    response = (
        f"Booking for {slots['day']} at {slots['time']} "
        f"for {slots['party_size']}{room_text}. Confirm?"
    )

    if corrected:
        response = f"Updated. {response}"

    return response, slots