import unittest

suite = unittest.defaultTestLoader.discover('tests', pattern='test_gui.py')
result = unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful():
    raise SystemExit(1)
if not result.testsRun or result.skipped:
    raise SystemExit('Dashboard tests must execute without skips.')
