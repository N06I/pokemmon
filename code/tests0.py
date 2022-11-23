import datetime
import time

before = datetime.datetime.now()

time.sleep(1)

now = datetime.datetime.now()

if now - before >= 1:
    print(now.minu)
