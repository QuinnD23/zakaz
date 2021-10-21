import datetime

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime("%A")

text = "Thursday"
if text == now:
    print(now)