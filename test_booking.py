import unittest

from extractors import (
    find_room,
    strip_room,
    find_day,
    find_time,
    find_party_size,
    extract_all
)

from booking import (
    next_missing_slot,
    is_correction,
    handle
)


class TestBooking(unittest.TestCase):

    def test_room_214(self):
        self.assertEqual(find_room("room 214"), "214")

    def test_room_305(self):
        self.assertEqual(find_room("Book room 305"), "305")

    def test_room_none(self):
        self.assertIsNone(find_room("I need a study room"))

    def test_strip_room(self):
        self.assertEqual(strip_room("Book room 214 at 3pm"), "Book at 3pm")

    def test_day_thursday(self):
        self.assertEqual(find_day("Thursday"), "Thursday")

    def test_day_friday_lowercase(self):
        self.assertEqual(find_day("friday"), "Friday")

    def test_day_in_sentence(self):
        self.assertEqual(find_day("I need it on Monday"), "Monday")

    def test_day_none(self):
        self.assertIsNone(find_day("I need a room"))

    def test_time_3pm(self):
        self.assertEqual(find_time("3pm"), "3:00pm")

    def test_time_3_space_pm(self):
        self.assertEqual(find_time("3 pm"), "3:00pm")

    def test_time_330pm(self):
        self.assertEqual(find_time("3:30pm"), "3:30pm")

    def test_time_24_hour(self):
        self.assertEqual(find_time("15:00"), "15:00")

    def test_party_digit(self):
        self.assertEqual(find_party_size("4 people"), 4)

    def test_party_word(self):
        self.assertEqual(find_party_size("four people"), 4)

    def test_party_just_me(self):
        self.assertEqual(find_party_size("just me"), 1)

    def test_party_bare_word(self):
        self.assertEqual(find_party_size("four"), 4)

    def test_party_word_in_sentence(self):
        self.assertEqual(find_party_size("Thursday at 3pm for four"), 4)

    def test_extract_all(self):
        result = extract_all(
            "Book room 214 for Thursday at 3pm for four people"
        )
        self.assertEqual(result["room"], "214")
        self.assertEqual(result["day"], "Thursday")
        self.assertEqual(result["time"], "3:00pm")
        self.assertEqual(result["party_size"], 4)

    def test_room_time_collision(self):
        result = extract_all("Book room 214 on Thursday")
        self.assertEqual(result["room"], "214")
        self.assertIsNone(result["time"])

    def test_next_missing_day(self):
        slots = {
            "day": None,
            "time": None,
            "party_size": None,
            "room": None
        }
        self.assertEqual(next_missing_slot(slots), "day")

    def test_next_missing_time(self):
        slots = {
            "day": "Thursday",
            "time": None,
            "party_size": None,
            "room": None
        }
        self.assertEqual(next_missing_slot(slots), "time")

    def test_next_missing_party(self):
        slots = {
            "day": "Thursday",
            "time": "3:00pm",
            "party_size": None,
            "room": None
        }
        self.assertEqual(next_missing_slot(slots), "party_size")

    def test_no_missing_slot(self):
        slots = {
            "day": "Thursday",
            "time": "3:00pm",
            "party_size": 4,
            "room": None
        }
        self.assertIsNone(next_missing_slot(slots))

    def test_is_correction(self):
        self.assertTrue(is_correction("Actually make it Friday"))

    def test_not_correction(self):
        self.assertFalse(is_correction("Thursday at 3pm"))

    def test_volunteered_information(self):
        slots = {
            "day": None,
            "time": None,
            "party_size": None,
            "room": None
        }
        response, slots = handle("Thursday at 3pm", slots)
        self.assertEqual(slots["day"], "Thursday")
        self.assertEqual(slots["time"], "3:00pm")
        self.assertEqual(response, "How many people will be using it?")

    def test_complete_booking(self):
        slots = {
            "day": None,
            "time": None,
            "party_size": None,
            "room": None
        }
        response, slots = handle(
            "Thursday at 3pm for four people",
            slots
        )
        self.assertIn("Confirm?", response)

    def test_optional_room(self):
        slots = {
            "day": None,
            "time": None,
            "party_size": None,
            "room": None
        }
        response, slots = handle(
            "Book room 214 Thursday at 3pm for four people",
            slots
        )
        self.assertIn("room 214", response)

    def test_correction_overwrites_day(self):
        slots = {
            "day": "Thursday",
            "time": "3:00pm",
            "party_size": 4,
            "room": "214"
        }
        response, slots = handle("Actually make it Friday", slots)
        self.assertEqual(slots["day"], "Friday")
        self.assertIn("Updated.", response)

    def test_confirmation_yes(self):
        slots = {
            "day": "Friday",
            "time": "3:00pm",
            "party_size": 4,
            "room": None
        }
        response, slots = handle("yes", slots)
        self.assertIn("Confirmed!", response)

    def test_confirmation_no(self):
        slots = {
            "day": "Friday",
            "time": "3:00pm",
            "party_size": 4,
            "room": None
        }
        response, slots = handle("no", slots)
        self.assertEqual(
            response,
            "Okay. Tell me what you'd like to change."
        )

    def test_party_size_not_time(self):
        result = extract_all("Thursday for 4 people")
        self.assertEqual(result["party_size"], 4)
        self.assertIsNone(result["time"])


if __name__ == "__main__":
    unittest.main()