import urllib.request
import re


class Robots():

    def __init__(self, url):
        self._url = url
        self._data = dict()
        self._users = set()
        self._sitemaps = set()

    def url(self):
        """Returns the primary URL pertaining to the robots.txt file"""
        return self._url

    def _robots(self):
        """Given a URL, fetches data from the site's
        robots.txt file and returns a list
        """
        if not self._url.endswith('/'):
            self._url += '/'
        robot = urllib.request.urlopen('%srobots.txt' % self._url)
        decoder = 'utf-8'
        charset = robot.info().get_content_charset()
        if charset:
            decoder = charset
        content = robot.read().decode(decoder)
        robot.close()
        return [line for line in content.split('\n')]

    def read(self):
        """Fetches and parses data from robots.txt"""
        
        if self._data:
            self._data = dict()  # Reset _data if _data exists
    
        for line in self._robots():
            if 'User-agent:' in line:
                user = re.search(r'User-agent:\s+(.*)', line).group(1)
                self._data[user] = {'Allow:': set(), 'Disallow:': set()}
            elif 'Allow:' in line:
                findit = re.search(r'Allow:\s+(/.*)', line)
                self._data[user]['Allow:'].add(findit.group(1))
            elif 'Disallow:' in line:
                findit = re.search(r'Disallow:\s+(/.*)', line)
                self._data[user]['Disallow:'].add(findit.group(1))
            elif 'Sitemap:' in line:
                findit = re.search(r'Sitemap:\s+(.*)', line)
                self._sitemaps.add(findit.group(1))

    def sitemaps(self):
        """Returns a set of Sitemap URLs associated with primary URL."""
        if not self._data:
            print('Error:  /robots.txt/ file not parsed!  Please run Robots.read() first.')
        return self._sitemaps

    def users(self):
        """Returns a set of User-agents explicitly called by robots.txt"""
        if not self._data:
            print('Error:  /robots.txt/ file not parsed!  Please run Robots.read() first.')
        else:
            return set(self._data.keys())

    def allowed(self, user_agent):
        """Given a User-agent, return a set of explicitly Allowed URLs"""
        if not self._data:
            print('Error:  /robots.txt/ file not parsed!  Please run Robots.read() first.')
        else:
            return self._data[user_agent]['Allow:']
    
    def disallowed(self, user_agent):
        """Given a User-agent, return a set of explicitly Disallowed URLs"""
        if not self._data:
            print('Error:  /robots.txt/ file not parsed!  Please run Robots.read() first.')
        else:
            return self._data[user_agent]['Disallow:']
    

    
if __name__ == '__main__':

    # Test URL
    url = 'http://www.google.com'
    test = Robots(url)
    




