"""
Program: test_ddg_api.py
Name: Matthew Neiditch
Date: 10/19/2020
Course: CSC256.0001

Program Description:
Write a PyTest module that queries the DuckDuckGo api for “presidents of the united states,” and tests that each president is listed in the response.  (If you need a list or our presidents, see Presidents (opens new window)).

The presidents should be listed in the RelatedTopics returned field.  RelatedTopics is a list, and you should check the Text entries of RelatedTopics to search for presidents.  We’ll only look for the last name of a president.  That means that we won’t distinguish between John Adams and his son, John Quincy Adams, or George Bush the senior and ‘W.’
"""

import requests, pytest


presidents = [
    'George Washington',
    'John Adams',
    'Thomas Jefferson',
    'James Madison',
    'James Monroe',
    'John Quincy Adams',
    'Andrew Jackson',
    'Martin Van Buren',
    'William Henry Harrison',
    'John Tyler', # 10th
    'James K. Polk',
    'Zachary Taylor',
    'Millard Fillmore',
    'Franklin Pierce',
    'James Buchanan',
    'Abraham Lincoln',
    'Andrew Johnson',
    'Ulysses S. Grant',
    'Rutherford B. Hayes',
    'James Garfield', # 20th
    'Chester A. Arthur',
    'Grover Cleveland',
    'Benjamin Harrison',
    'Grover Cleveland',
    'William McKinley',
    'Theodore Roosevelt',
    'William Howard Taft',
    'Woodrow Wilson',
    'Warren G. Harding',
    'Calvin Coolidge', # 30th
    'Herbert Hoover',
    'Franklin D. Roosevelt',
    'Harry S. Truman',
    'Dwight D. Eisenhower',
    'John F. Kennedy',
    'Lyndon B. Johnson',
    'Richard M. Nixon',
    'Gerald R. Ford',
    'James Carter',
    'Ronald Reagan', # 40th
    'George H. W. Bush',
    'William J. Clinton',
    'George W. Bush',
    'Barack Obama',
    'Donald J. Trump'] # 45th
# remove repeat presidents (ex: Grover Cleveland)
presidents = list(set(presidents))
# get a list of presidental last names (including repeat last names)
president_last_names = [name.split()[-1] for name in presidents]


# send a duckduckgo search query and get the results
url_ddg = "https://api.duckduckgo.com"
query = "presidents of the united states"
resp = requests.get(url_ddg + '/?q=' + query + '&format=json')
if resp == None:
    print('Error: "' + url_ddg + '/?q=' + query + '&format=json" returned None')
    exit(1)
# extract relevant data from results
data_json = resp.json()
related_topics = data_json['RelatedTopics']
texts = [topic['Text'].split(' - ')[0] for topic in related_topics]


@pytest.fixture
def texts_copy():
    return texts[:]


def get_index_with_string(astring, alist):
    """returns the index position of an string in a list that 
       contains a given string, or -1 if not found.
       Raises IndexError if the list is empty
    """
    if len(alist) == 0:
        raise IndexError('Empty list.')
    for i, val in enumerate(alist):
        if astring in val:
            return i
    return -1


def test_ddg_get_all_presidents_by_last_name_non_repeating(texts_copy):
    for name in president_last_names:
        # find the index of the president's last name in the list
        name_index = get_index_with_string(name, texts_copy)
        assert name_index != -1, name + ' not found.'
        # remove the entry where name was found
        del texts_copy[name_index]