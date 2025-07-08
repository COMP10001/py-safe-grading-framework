# COPYRIGHT EDSTEM

import json
import sys
import traceback
import unittest

class EdTestResult(unittest.TestResult):
	def __init__(self, stream, descriptions, verbosity):
		super().__init__(stream, descriptions, verbosity)
		self.passed = []
		self.failed = []

	def startTest(self, test):
		super().startTest(test)

	def addSubTest(self, test, subtest, outcome):
		super().addSubTest(test, subtest, outcome)
		if outcome is None:
			self.passed.append(subtest)
		else:
			self.failed.append((subtest, outcome))

	def addSuccess(self, test):
		super().addSuccess(test)
		self.passed.append(test)

	def addError(self, test, err):
		super().addError(test, err)
		self.failed.append((test, err))

	def addFailure(self, test, err):
		super().addFailure(test, err)
		self.failed.append((test, err))

	def addSkip(self, test, reason):
		super().addSkip(test, reason)

	def addExpectedFailure(self, test, err):
		super().addExpectedFailure(test, err)

	def addUnexpectedSuccess(self, test):
		super().addUnexpectedSuccess(test)

def _exc_info_to_string(test, err):
	"""Converts a sys.exc_info()-style tuple of values into a string."""
	exctype, value, tb = err

	# Skip test runner traceback levels
	while tb and _is_relevant_tb_level(tb):
		tb = tb.tb_next

	if exctype is test.failureException:
		# Skip assert*() traceback levels
		length = _count_relevant_tb_levels(tb)
	else:
		length = None

	return ''.join(traceback.format_tb(tb, limit=length))

def _is_relevant_tb_level(tb):
	return '__unittest' in tb.tb_frame.f_globals

def _count_relevant_tb_levels(tb):
	length = 0
	while tb and not _is_relevant_tb_level(tb):
		length += 1
		tb = tb.tb_next
	return length

class EdTestLoader(unittest.TestLoader):
	def __init__(self):
		super().__init__()

		self.test_descriptions = {}

	def getTestCaseNames(self, testCaseClass):
		test_names = super().getTestCaseNames(testCaseClass)
		testcase_methods = list(testCaseClass.__dict__.keys())
		test_names.sort(key=testcase_methods.index)
		descriptions = { k: v.__doc__ for k, v in testCaseClass.__dict__.items() if callable(v)}
		self.test_descriptions = {**self.test_descriptions, **descriptions}
		return test_names

if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit(1)

	loader = EdTestLoader()
	tests = loader.discover('.')
	runner = unittest.TextTestRunner(resultclass=EdTestResult)
	result = runner.run(tests)

	with open(sys.argv[1], 'wb') as outfile:
		def strline(s):
			sb = str(s).encode('utf-8')
			outfile.write((str(len(sb)) + ' ').encode('utf-8'))
			outfile.write(sb)
			outfile.write('\n'.encode('utf-8'))

		outfile.write((json.dumps(loader.test_descriptions) + '\n').encode('utf-8'))
		outfile.write((str(len(result.passed)) + '\n').encode('utf-8'))
		for passed in result.passed:
			strline(passed)

		outfile.write((str(len(result.failed)) + '\n').encode('utf-8'))
		for (test, err) in result.failed:
			strline(test)
			strline(str(err[0].__name__))
			strline(str(err[1]))
			strline(_exc_info_to_string(test, err))

		outfile.write('fin\n'.encode('utf-8'))