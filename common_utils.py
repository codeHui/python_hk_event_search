from datetime import datetime, time, timedelta, date # Added date import

# Define Hong Kong public holidays for 2025
hk_public_holidays_2025 = [
    date(2025, 1, 1),   # The first day of January
    date(2025, 1, 29),  # Lunar New Year’s Day
    date(2025, 1, 30),  # The second day of Lunar New Year
    date(2025, 1, 31),  # The third day of Lunar New Year
    date(2025, 4, 4),   # Ching Ming Festival
    date(2025, 4, 18),  # Good Friday
    date(2025, 4, 19),  # The day following Good Friday
    date(2025, 4, 21),  # Easter Monday
    date(2025, 5, 1),   # Labour Day
    date(2025, 5, 5),   # The Birthday of the Buddha
    date(2025, 5, 31),  # Tuen Ng Festival
    date(2025, 7, 1),   # Hong Kong Special Administrative Region Establishment Day
    date(2025, 10, 1),  # National Day
    date(2025, 10, 7),  # The day following the Chinese Mid-Autumn Festival
    date(2025, 10, 29), # Chung Yeung Festival
    date(2025, 12, 25), # Christmas Day
    date(2025, 12, 26)  # The first weekday after Christmas Day
]

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
        # Check if event_start date is a public holiday
        if event_start.date() in hk_public_holidays_2025:
            return True

        # Return true if it's Saturday or Sunday
        if event_start.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
            return True

        # Return true if event_start is after 18:20 on a weekday
        return event_start.time() >= time(18, 20)

