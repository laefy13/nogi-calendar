from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event

import os
from datetime import datetime


def save_calendar(sched, adj_time):

    calendar = GoogleCalendar(credentials_path="credentials.json")
    calendar.clear_calendar()
    for key, events in sched.items():
        for event in events:
            time_range, evName = event.popitem()
            temp_key = int(key)
            try:
                if "-" in time_range:
                    hour, minute = map(int, time_range.split("-")[0].split(":"))
                elif "～" in time_range:
                    hour, minute = map(int, time_range.split("～")[0].split(":"))
                else:
                    hour, minute = 0, 0
                hour += adj_time
                if hour >= 24:
                    hour = hour - 24
                    temp_key += 1
            except ValueError:
                hour, minute = adj_time, 0
            data = {
                "event": evName,
                "start": datetime(2024, 3, temp_key, hour, minute),
            }
            gEvent = Event(
                data["event"], start=data["start"], minutes_before_popup_reminder=15
            )
            calendar.add_event(gEvent)
