import datetime
import time

before = datetime.datetime.now()

# time.sleep(1)

now = datetime.datetime.now()
start = time.time_ns()
print(f"{now.minute-9:02d}")
end = time.time_ns()
print(f"Calc time: {end - start}")

start = time.time_ns()
print(f"{str(now.minute-9).zfill(2)}")
end = time.time_ns()
print(f"Calc time: {end}, {start}")
