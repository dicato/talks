# Ahem, you should use requests...
import urllib


def get_external_address():
    url = 'https://dnswatch.watchguard.com/whatismyip/'
    return urllib.urlopen(url).read()
