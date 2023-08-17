import os
import sys
import time
import numpy as np

try:
    from pyglplot import scatter

except ImportError:
    print("ImportError: pyglplot not found")
    print("trying pyglplot from local folder")

    import repackage
    abs_path = os.getcwd()
    print("abs_path=", abs_path)
    repackage.add_path(abs_path)
    print("")

from pyglplot import scatter

MAX_SQUARE_NUM = 1_000
SQUARE_SIZE = 0.01
NEW_DATA_NUM = 1

if len(sys.argv) < 2:
    CONTEXT_API = "auto"
else:
    CONTEXT_API = sys.argv[1]

plot_scatter = scatter.Scatter(MAX_SQUARE_NUM, SQUARE_SIZE, context_api=CONTEXT_API)




time_stamp = []


counter = 0

def update():
    time_stamp.append(time.perf_counter())

    global counter

    rand = np.random.rand(1, NEW_DATA_NUM * 2)
    pos = np.array(rand, dtype=np.float32)
    pos[0::2] = (2*pos[0::2] - 1) * plot_scatter.aspect_ratio
    pos[1::2] = 2*pos[1::2] - 1
    
    plot_scatter.add_point(pos)

    
    counter += 1

    if counter*NEW_DATA_NUM > MAX_SQUARE_NUM:
        counter = 0
        plot_scatter.reset_pos()

    
    if len(time_stamp) > 100:
        print(int(1/np.mean(np.diff(time_stamp))))
        time_stamp.clear()


plot_scatter.run(update)
