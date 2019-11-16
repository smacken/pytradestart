import sys
import os
import time
path_to_append = os.path.join(os.path.dirname(__file__), os.pardir, "mockportfolio")
print(path_to_append)
sys.path.append(path_to_append)

now = str(round(time.time()))
__version__ = f'0.1.0.{now}'
