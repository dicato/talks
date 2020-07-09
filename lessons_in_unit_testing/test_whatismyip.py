from StringIO import StringIO
import unittest

import mock

from whatismyip import get_external_address


class ExternalAddressTests(unittest.TestCase):
    def test_get_address(self):
        with mock.patch('urllib.urlopen') as urlopen:
            fake_ip = StringIO('12.12.12.12')
            urlopen.return_value = fake_ip

            self.assertEqual(get_external_address(), '12.12.12.12')

            urlopen.assert_called_with(
                'https://dnswatch.watchguard.com/whatismyip/'
            )


if __name__ == '__main__':
    unittest.main()
