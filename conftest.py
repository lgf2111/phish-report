# Lets the tests find the code in the app/ folder.
# pytest loads this file automatically before running tests.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))
