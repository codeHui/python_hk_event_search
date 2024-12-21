from datetime import datetime, time, timedelta

class CommonUtils:
    @staticmethod
    def is_period_after_work(event_start, event_end):
        # Return true if there is Saturday or Sunday between event_start and event_end
        current_date = event_start
        while current_date <= event_end:
            if current_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
                return True
            current_date += timedelta(days=1)

        # Return true if event_start is after 18:20 on a weekday
        return event_start.time() >= time(18, 20)
    
    @staticmethod
    def is_time_after_work(event_start):
        # Return true if there is Saturday or Sunday between event_start and event_end
        if event_start.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
            return True

        # Return true if event_start is after 18:20 on a weekday
        return event_start.time() >= time(18, 20)
    
