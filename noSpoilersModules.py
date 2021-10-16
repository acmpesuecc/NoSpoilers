'''
This is the modules file for NoSpoilers
All functions defined for the specific task is featured here
'''

import pandas as pd
import requests

def inputQuery(query):
        '''
        This function is used to take input for the API call
        '''
        url = f"https://tvjan-tvmaze-v1.p.rapidapi.com/search/shows?q={query}"
        headers = {
            'x-rapidapi-key': "c130b92fbamsh3611aaa6003b0fep1c9b82jsnf0c2faa52da9",
            'x-rapidapi-host': "tvjan-tvmaze-v1.p.rapidapi.com"
            }
        response = requests.request('GET', url, headers=headers)
        lst = response.text.split('"')
        return lst

def splitID(a):
        '''
        This function is used to extract the ID of the TV show from the API dataset
        '''
        try:
            temp = list(a)
            temp.pop(0)
            temp.pop(-1)
            a = ''.join(temp)
            return a

        except IndexError:
            raise Exception('Something went wrong!')


def addData_ppl(a, fl):
    '''
    This function is used to add certain data to a dataframe and display it for the actor
    '''
    try:
        global df
        fl = [a]
        df = pd.DataFrame(fl, columns=['Name of the Actor', 'ID', 'Country', 'Birthday', 'Gender'], index=[1])
        return df
    except ValueError:
        print('Something went wrong!')


def call_ppl(a):
    '''
    This function is to call addData function fr the actor
    '''
    global name, new_id, country, birthday, gender, fl
    fl = []
    return addData_ppl(a, fl)

def addData(a, fl):
        '''
        This function is used to add certain data to a dataframe and display it
        '''
        try:
            global df
            fl = [a]
            df = pd.DataFrame(fl, columns = ['Name of the show', 'ID', 'Langauge', 'Genre', 'Status'], index = [1])
            return df
        except ValueError:
            print('Something went wrong!')

def call(a):
        '''
        This function is to call addData function
        '''
        global name, new_id, lang, gen, stat, fl
        fl = []
        return addData(a, fl)


def scrape_ppl(a):
    '''
    This function is used to scrape and parse the crude data output from API
    '''



    try:
        scrape.id = a[6]
        scrape.name = a[13]
        scrape.country = a[19]
        scrape.birthday = a[31]
        scrape.gender=a[37]
    except IndexError:
        print('Something went wrong!')

    return scrape.name, scrape.id, scrape.country, scrape.birthday, scrape.gender


def scrape(a):
        '''
        This function is used to scrape and parse the crude data output from API
        '''
        try:
            statind = a.index('status')
            scrape.stat = a[(statind+2)]
        except ValueError:
            scrape.stat = 'Not Known'

        try:
            scrape.id = a[6]
            scrape.name = a[13]
            scrape.lang = a[21]
            scrape.gen = a[25]
        except IndexError:
            print('Something went wrong!')

        return scrape.name, scrape.id, scrape.lang, scrape.gen, scrape.stat


def ppl_search(people):
    '''
            This function is used to take input for the API call for searching for actor
            '''
    url = f" https://api.tvmaze.com/search/people?q={people}"
    headers = {
        'x-rapidapi-key': "c130b92fbamsh3611aaa6003b0fep1c9b82jsnf0c2faa52da9",
        'x-rapidapi-host': "tvjan-tvmaze-v1.p.rapidapi.com"
    }
    response = requests.request('GET', url, headers=headers)
    lst = response.text.split('"')
    return lst



