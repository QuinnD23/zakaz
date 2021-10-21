import datetime

now_named_day = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime("%A"))

text = "Thursday"
if text == now_named_day:
    print(now_named_day)