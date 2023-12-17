import unittest

# discover all tests in the 'tests' directory
suite = unittest.defaultTestLoader.discover(start_dir='tests')

# run the tests
runner = unittest.TextTestRunner()
runner.run(suite)
