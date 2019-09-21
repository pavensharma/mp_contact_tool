import requests
import json
import codecs
from bs4 import BeautifulSoup
import smtplib


class Mp:
    def __init__(self, postcode):
        self.user_postcode = postcode
        self.user_name = "test"
        self.user_email = "pavensharma90@gmail.com"
        self.unique_id = "123"
        self.name = "Unknown"
        self.constituency = "Unknown"
        self.email = "Unknown"
        self.twitter = "z"
        self.parliament_link = "parliament link"
        self.bio_page = "bio page"
        self.address = "address"
        self.bio_soup ="xyz"


    def find_constituency(self):
        consituancy_finder = "https://constituencyfinder.digiminster.com/Search?searchTerm="
        consituancy_finder = consituancy_finder + self.user_postcode
        consituancy_page = requests.get(consituancy_finder)
        constituency_label = consituancy_page.text
        post_code_soup = BeautifulSoup(constituency_label, 'html.parser')
        constituency_name = post_code_soup.find('span', attrs={'class': 'constituency'})
        constituency_name = constituency_name.text
        self.constituency = constituency_name


    def find_mp_parliament_address(self):
        api_address = "http://data.parliament.uk/membersdataplatform/services/mnis/members/query/house=Commons|IsEligible=true|constituency="
        full_link = api_address + self.constituency
        self.parliament_link = full_link


    def find_extract_mp_details(self):
        pull = requests.get(self.parliament_link, headers={"content-type": "application/json"})
        y = open("sample.json", "w")
        y.write(pull.text)
        y.close()
        x = json.load(codecs.open('sample.json', 'r', 'utf-8-sig'))
        mp_name = x['Members']['Member']['FullTitle']
        mp_id = x['Members']['Member']['@Member_Id']
        self.name = mp_name
        self.unique_id = mp_id


    def find_bio_page(self):
        self.name = self.name[:-3]
        mp_name = self.name.replace(" ", "-")
        mp_bio = f"https://www.parliament.uk/biographies/commons/{mp_name}/{self.unique_id}"
        self.bio_page = mp_bio


    def find_email_address(self):
        page = requests.get(self.bio_page)
        data = page.text
        self.bio_soup = BeautifulSoup(data, 'html.parser')
        email = self.bio_soup.select('a[href^="mailto"]')
        for link in email:
            mp_email_address = link.text
        self.email = mp_email_address


    def find_constituant_address(self):
        x = "ctl00_ctl00_FormContent_SiteSpecificPlaceholder_PageContent_addConstituencyAddress_rptAddresses_ctl00_pnlAddress"
        try:
            address = self.bio_soup.find('p', attrs={'id': x})

            address = str(address.text)

            address = address.strip()

            self.address = address

        except:
            self.address = "No address found!"

def send_email():
    username = "cheaptechexpert@gmail.com"
    password = "Singapore2019@"
    MESSAGE = "xyz"
    FROM_EMAIL_ADDRESS = "cheaptechexpert@gmail.com"
    TO_EMAIL_ADDRESS = "pavensharma90@gmail.com"
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login(username,password)
    server.sendmail(FROM_EMAIL_ADDRESS,TO_EMAIL_ADDRESS,MESSAGE)
    return