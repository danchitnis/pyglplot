import os
import sys
import time
import numpy as np

try:
    from pyglplot import roll

except ImportError:
    print("ImportError: pyglplot not found")
    print("trying pyglplot from local folder")

    import repackage
    abs_path = os.getcwd()
    print("abs_path=", abs_path)
    repackage.add_path(abs_path)
    print("")

from pyglplot import roll

NUM_LINES = 3

if len(sys.argv) < 2:
    CONTEXT_API = "auto"
else:
    CONTEXT_API = sys.argv[1]

plot_roll = roll.Roll(2000, num_lines=NUM_LINES, context_api=CONTEXT_API)


for i in range(NUM_LINES):
    plot_roll.update_line_color([np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)], i)


y = np.zeros(NUM_LINES)

time_stamp = []

k = 1


def update():
    time_stamp.append(time.perf_counter())
    
    for i in range(NUM_LINES):
        a = y[i] + 0.01 * (i+1) / NUM_LINES
        y[i] = a - np.round(a)

    plot_roll.add_point(y)
    

    if len(time_stamp) > 100:
        print(int(1/np.mean(np.diff(time_stamp))))
        time_stamp.clear()


plot_roll.run(update)
