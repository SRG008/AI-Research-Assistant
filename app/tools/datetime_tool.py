
from datetime import datetime


class DateTimeTool:

    def get_current_datetime(self) -> dict:
        """Return the current local date, time and timezone."""

        now = datetime.now().astimezone()

        return {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%I:%M:%S %p"),
            "day": now.strftime("%A"),
            "timezone": str(now.tzinfo)
        }
