import sys
import unittest

# discover all tests in the 'tests' directory
suite = unittest.defaultTestLoader.discover(start_dir='tests')

# run the tests
runner = unittest.TextTestRunner()
result = runner.run(suite)
sys.exit(not result.wasSuccessful())
