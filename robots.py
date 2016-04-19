import urllib.request
import re



def robots(url):
    if not url.endswith('/'):
        url += '/'
    robot = urllib.request.urlopen('%srobots.txt' % url)
    decoder = 'utf-8'
    charset = robot.info().get_content_charset()
    if charset:
        decoder = charset
    content = robot.read().decode(decoder)
    robot.close()
    return [line for line in content.split('\n')]

def allowed(url):
    allow = set()
    for line in robots(url):
        findit = re.search(r'Allow:\s+(/.*)', line)
        if findit:
            allow.add(findit.group(1))
    return allow

def disallowed(url):
    disallow = set()
    for line in robots(url):
        findit = re.search(r'Disallow:\s+(/.*)', line)
        if findit:
            disallow.add(findit.group(1))
    return disallow


    
    
url = 'http://www.babycenter.com'
    




