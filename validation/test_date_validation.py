import unittest

from validation.date_validation import validate_date_format


class DateFormatValidationTests(unittest.TestCase):

    def test_valid_date_format(self):
        # Test a valid date format
        self.assertTrue(validate_date_format("2023-06-07", "%Y-%m-%d"))

    def test_invalid_date_format(self):
        # Test an invalid date format
        self.assertFalse(validate_date_format("07-06-2023", "%Y-%m-%d"))

    def test_invalid_date_value(self):
        # Test an invalid date value
        self.assertFalse(validate_date_format("2023-06-40", "%Y-%m-%d"))

    def test_empty_date_string(self):
        # Test an empty date string
        self.assertFalse(validate_date_format("", "%Y-%m-%d"))
