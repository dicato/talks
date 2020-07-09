import unittest

from license import is_license_expired

class LicenseTests(unittest.TestCase):

    def test_special_licenses(self):
        # Some licenses never expire
        self.assertFalse(is_license_expired('never'))
        self.assertFalse(is_license_expired('0'))

    def test_expired_license(self):
        # Expired
        self.assertTrue(is_license_expired('Aug-07-2017'))
        self.assertTrue(is_license_expired('07-Aug-2017'))

    def test_not_expired_license(self):
        # Not expired
        self.assertFalse(is_license_expired('Aug-07-2099'))
        self.assertFalse(is_license_expired('07-Aug-2099'))

    def test_invalid_format(self):
        # Invalid date formats should return True
        self.assertTrue(is_license_expired('2020-Jul-10'))

if __name__ == '__main__':
    unittest.main()
