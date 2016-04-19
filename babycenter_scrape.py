# Test Scrape Program - Baby Names

import re
import urllib.request
import robots

primary_url = 'http://www.babycenter.com'
explicit_allowed = robots.allowed(primary_url)
explicit_disallowed = robots.disallowed(primary_url)

years = set()
boy_names = dict()
girl_names = dict()

boy_search = {'B', 'Boy', 'M', 'Male', 'b', 'boy', 'm', 'male'}
girl_search = {'F', 'Female', 'G', 'Girl', 'f', 'female', 'g', 'girl'}

boys = re.compile(r'<a id="bcBoy_\d+" href="http://www.babycenter.com/baby-names-\w+-\d+.htm">(\w+)</a>')
girls = re.compile(r'<a id="bcGirl_\d+" href="http://www.babycenter.com/baby-names-\w+-\d+.htm">(\w+)</a>')

def obtain_names(obtain_year):

    for year in obtain_year:
        try:
            url_exists = True
            sample_url = ('http://www.babycenter.com/popularBabyNames.htm?year=%s' % year)
            url = urllib.request.urlopen(sample_url)
        except:
            print('%s not in website database!  Aborting!' % year)
            years.discard(year)
            url_exists = False
        if url_exists:
            charset = url.info().get_content_charset()
            content = url.read().decode(charset)

            find_boys = boys.findall(content)
            if find_boys != []:
                boy_names[year] = find_boys
                print('Boy names appended to %s' % year)

            find_girls = girls.findall(content)
            if find_girls != []:
                girl_names[year] = find_girls
                print('Girl names appended to %s' % year)

            if find_boys == [] or find_girls == []:
                print('Website exists, but no data!  Removing year.')
                years.discard(year)
            
            url.close()


def recall(year, gender=None, count=5):
    if type(year) in [type(int()), type(str())]:
        if type(year) == type(int()): year = str(year)
        if year not in set(boy_names.keys()) | set(girl_names.keys()):
            print('%s not in the database, downloading...' % year)
            years.add(year)

            to_recall = list()
            to_recall.append(year)
            obtain_names(to_recall)
            print('\n')

    def print_girls():
        print('Girls:')
        for name in girl_names[str(year)][:count]:
            print('  ', name)

    def print_boys():
        print('Boys:')
        for name in boy_names[str(year)][:count]:
            print('  ', name)
            
    if year in years:
        print('%s: Top %s' % (year, count))
        if gender in boy_search:
            print_boys()
        elif gender in girl_search:
            print_girls()
        else:
            print_boys()
            print_girls()


def allnames(gender = None):

    girlnames = set()
    for names in girl_names.values():
        for name in set(names):
            girlnames.add(name)

    boynames = set()
    for names in boy_names.values():
        for name in set(names):
            boynames.add(name)

    if gender == None:
        print('Boys: All')
        for name in sorted(boynames):
            print('  ', name)
        print('Girls: All')
        for name in sorted(girlnames):
            print('  ', name)
    elif gender in boy_search:
        print('Boys: All')
        for name in sorted(boynames):
            print('  ', name)
    elif gender in girl_search:
        print('Girls: All')
        for name in sorted(girlnames):
            print('  ', name)
