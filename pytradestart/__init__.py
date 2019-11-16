import sys
import os
import time
path_to_append = os.path.join(os.path.dirname(__file__), os.pardir, "mockportfolio")
print(path_to_append)
sys.path.append(path_to_append)

__version__ = '0.1.0.' + str(round(time.time()))
