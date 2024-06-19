import json
import re
import pprint

import pytz
from dateutil import parser
import datetime


def getSalaryPrice(day):
    is_saturday = day.weekday() == 5  # In Python's datetime library, Saturday is 5
    is_friday = day.weekday() == 4  # Friday is 4
    is_evening = day.hour >= 14

    if is_saturday:
        return 50
    elif is_friday:
        if is_evening:
            return 50
        else:
            return 45
    return 45



TotalHoursWorked = 0
TotalPay = 0
totalReport = []
adress = "Pardes Meshutaf St 5, Ra\u0027anana, 43355, Israel"
f = open('2024_MAY.json', encoding="utf8")
data = json.load(f)["timelineObjects"]
values = [d['placeVisit'] for d in data if 'placeVisit' in d]
workInstanses = []
for place in values:
    try:
        if place["location"]["address"] == adress:
            workInstanses.append(place["duration"])
    except:
        pass
print(len(workInstanses))
for times in workInstanses:
    startTime = parser.parse(times["startTimestamp"])
    endTime = parser.parse(times["endTimestamp"])
    israel = pytz.timezone('Asia/Jerusalem')
    start_obj_israel = startTime.astimezone(israel)
    end_obj_israel = endTime.astimezone(israel)
    durationTimeWorked = (end_obj_israel - start_obj_israel).total_seconds() / 3600
    TotalHoursWorked = TotalHoursWorked + durationTimeWorked
    TotalDayPay = getSalaryPrice(start_obj_israel)*durationTimeWorked
    TotalPay = TotalPay+TotalDayPay
    totalReport.append({"startTime": start_obj_israel, "endTime": end_obj_israel, "Duration": durationTimeWorked,"pay": getSalaryPrice(start_obj_israel),"totalPay": TotalDayPay})

for dayOfWork in totalReport:
    print("------------------------------------------------------")
    print(" day: ", dayOfWork["startTime"].day, "\n",
          f"start: {dayOfWork["startTime"].hour}:{dayOfWork["startTime"].minute}\n",
          f"end: {dayOfWork["endTime"].hour}:{dayOfWork["endTime"].minute}\n",
          f"HoursWorked: {dayOfWork["Duration"]}",
          f"hourly: {dayOfWork["pay"]}",
          f"Total: {dayOfWork["totalPay"]}")
print(TotalHoursWorked)
print(TotalPay)
