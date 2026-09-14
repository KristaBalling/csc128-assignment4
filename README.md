# Assignment 4: Slot-Filling Reservation Bot

This project is a Streamlit study room reservation chatbot that uses regular expressions to extract booking details and slot filling to ask for missing information.

## How to Run

Activate the virtual environment, then run:

streamlit run app.py

To run the tests:

python test_booking.py

## Slots

Required:
- Day
- Time
- Party size

Optional:
- Room number

## Extraction Collision

A room number can be mistaken for a time. For example:

Book room 214 on Thursday

The room number 214 could interfere with time extraction if both extractors examine the same text.

The fix was to extract the room number first and remove it from the text before running the time extractor.

The test_room_time_collision test verifies that room 214 is extracted as the room number while the time remains None.

## What I Would Improve With More Time

With more time, I would add support for relative dates such as tomorrow and next Tuesday, more flexible time formats, and additional confirmation options.