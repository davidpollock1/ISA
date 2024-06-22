from itertools import tee
from typing import List
from .models import TeeSheetSettings, TeeSheetTime, TeeTimeSlot
import datetime

def generate_tee_times(tee_sheet_settings: TeeSheetSettings, start_date: datetime, end_date: datetime ) -> List[TeeSheetTime]:
    tee_sheet_times = []
    start_datetime = datetime.datetime.combine(start_date, tee_sheet_settings.start_time)
    end_datetime = datetime.datetime.combine(end_date, tee_sheet_settings.end_time)
    current_datetime = start_datetime
    interval = tee_sheet_settings.interval

    while current_datetime < end_datetime:
        tee_sheet_time = TeeSheetTime(
            time=current_datetime,
            price=tee_sheet_settings.default_price,
            tee_sheet_settings=tee_sheet_settings,
            customer=tee_sheet_settings.customer,
            golf_course=tee_sheet_settings.golf_course
        )
        tee_sheet_times.append(tee_sheet_time)
        current_datetime += interval

    return tee_sheet_times

def generate_tee_time_slots(tee_sheet_time: TeeSheetTime, number_of_slots: int) -> List[TeeTimeSlot]:
    tee_time_slots = []
    for _ in range(number_of_slots):
        tee_time_slot = TeeTimeSlot(
            status=1,
            tee_sheet_time=tee_sheet_time,
            customer=tee_sheet_time.customer
        )
        tee_time_slots.append(tee_time_slot)

    return tee_time_slots