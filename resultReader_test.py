import unittest

from resultReader import ResultReader

class TestResultReader(unittest.TestCase):
  def setUp(self):
      self._json_file_name = "output_for_test.json"
      self._result_reader = ResultReader(self._json_file_name)

  def test_get_browser_names(self):
      target = self._result_reader.get_browser_names()
      expect = ["firefox.nightly", "android-browser", "mock-browser"]

      target.sort();
      expect.sort();

      self.assertEqual(target, expect)

  def test_get_test_case_name_list(self):
      target = self._result_reader.get_test_case_name_list()
      expect = ["mockTest", "mockTest2"]

      target.sort();
      expect.sort();

      self.assertEqual(target, expect)

  def test_get_test_case_value_lists(self):
      target = self._result_reader.get_test_case_value_lists()
      expect = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]

      target.sort();
      expect.sort();

      self.assertEqual(target, expect)

if __name__ == '__main__':
    unittest.main()
