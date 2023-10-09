import requests
from data import INFINITIVES
from bs4 import BeautifulSoup
import time
#from selenium.webdriver import Firefox
#from selenium.webdriver.firefox.options import Options
import random
import os.path
import pickle

BASE_URL = "https://la-conjugaison.nouvelobs.com/espagnol/verbe/"


class Scraper:
    def __init__(self, verb):
        self.verb = verb

        self.page_content = self.get_page_content()
        self.translation = None
        return

    def get_page_content(self):
        url = BASE_URL + self.verb + ".php"
        page = requests.get(url)
        page_content = BeautifulSoup(page.content, "html.parser")

        try:
            page_content.find('div', {'class': 'bloc'}).text
        except AttributeError:
            print("Verbe", self.verb, "introuvable.")
            return

        return page_content

    def get_translation(self):
        # Traduction du verbe
        translation_bloc = self.page_content.find('div', {'class': 'bloc b t22'})
        try:
            translation = translation_bloc.a.get_text()
        except AttributeError:
            translation = "Pas de traduction disponible"
        self.translation = translation
        return translation

    def scraping_conjugations(self):

        #print(traduction)
        #Temps de conjugaison
        tense_blocs = self.page_content.find_all('div', {'class': 'tempstab'})

        #seulement le présent pour commencer
        #print(tempsblocs[1].text)
        present = tense_blocs[0].text
        preterito_perfecto_simple = tense_blocs[5].text
        a = present.split(")",1)
        temps = a[0]+')'
        #conjugaisons:
        conjugaisons_brutes = a[1]
        pronombres = ['yo', 'tú','él','nosotros','vosotros','ellos']
        for i in pronombres:
            try:
                conjugaisons_brutes = conjugaisons_brutes.replace(i,'/',1)
            except:
                pass
        #print(conjugaisons_brutes)
        conjugaisons = conjugaisons_brutes.split('/')
        conjugaison = [b.replace('  ',' ').lstrip() for b in conjugaisons if b!='']
        #print(conjugaison)
        verbpackage = [temps, traduction, verbetype, conjugaison]

        dicoverbes[verbe] = verbpackage
        #print(dicoverbes)


def get_verb_html_page_content(infinitive):
    url = BASE_URL + infinitive + ".php"
    page = requests.get(url)
    page_content = BeautifulSoup(page.content, "html.parser")

    try:
        page_content.find('div', {'class': 'bloc'}).text
    except AttributeError:
        print("Verbe", infinitive, "introuvable.")
        return

    return page_content


def get_verb_translation(html_page_content):
    translation_bloc = html_page_content.find('div', {'class': 'bloc b t22'})
    try:
        translation = translation_bloc.a.get_text()
    except AttributeError:
        translation = "Pas de traduction disponible"
    return translation


def get_verb_type(html_page_content):
    translation_bloc = html_page_content.find('div', {'class': 'bloc'})
    try:
        translation = translation_bloc.b.get_text()
    except AttributeError:
        translation = "sans type"
    return translation


def get_conjugation(verb_page_content, tense):
    """ Get the conjugation of a verb at a specific tense.

    Input:

    -- verb_page_content (html?): the full html page of a verb.
    -- tense (str): the tense to which the verb hqs to be conjugated.

    Ouptput:

    -- tense_conjugation_dictionnary (dict): dictionary containing the conjugations of the verb for each pronoun."""
    tense_blocs = verb_page_content.find_all('div', {'class': 'tempstab'})
    tense_id = tense_list.index(tense)

    tense_conjugation = tense_blocs[tense_id].text
    tense_conjugation_string = tense_conjugation.split(")", 1)
    temps = tense_conjugation_string[0] + ')'
    # conjugaisons:
    conjugaisons_brutes = tense_conjugation_string[1]
    pronombres = ['yo', 'tú', 'él', 'nosotros', 'vosotros', 'ellos']
    for i in pronombres:
        try:
            conjugaisons_brutes = conjugaisons_brutes.replace(i, '/', 1)
        except:
            pass

    print(conjugaisons_brutes)
    conjugations = conjugaisons_brutes.split('/')
    conjugation = [b.replace('  ', ' ').lstrip() for b in conjugations if b != '']
    # print(conjugaison)
    verbpackage = [temps, traduction, verbetype, conjugaison]

    dicoverbes[verbe] = verbpackage
    # print(dicoverbes)

    return conjugation_dict

verbs = {} # dictionnary containing information about verbs

print(get_verb_html_page_content('tener'))
for verb_infinitive in INFINITIVES:
    # get information from scrapping the verb's webpage
    verb_page = get_verb_html_page_content(verb_infinitive)

    # use scrapping data to obtain verb's information
    verb_translation = get_verb_translation(verb_page)
    verb_type = get_verb_type(verb_page)
    verb_conjugation = get_verb_conjugation(verb_page)

    # add the verb to the dictionary that will store the information necessary for the quizz
    verbs[verb_infinitive] = [verb_translation, verb_type, verb_conjugation]


# save dictionary to a file, to avoid having to do the scrapping evry time the app is loaded
# TODO: add a function that saves the dictionary to a file