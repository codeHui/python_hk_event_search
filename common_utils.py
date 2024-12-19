from datetime import datetime, time, timedelta

class CommonUtils:
    @staticmethod
    def is_event_on_weekend_or_after_hours(event_start, event_end):
        # Return true if there is Saturday or Sunday between event_start and event_end
        current_date = event_start
        while current_date <= event_end:
            if current_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
                return True
            current_date += timedelta(days=1)

        # Return true if event_start is after 18:20 on a weekday
        return event_start.time() >= time(18, 20)
    
