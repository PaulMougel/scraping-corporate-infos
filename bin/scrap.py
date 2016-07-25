from lxml import html
import csv, os, json
import requests
from exceptions import ValueError
from time import sleep
 
class Scrap:
    
    response = {}
    
    def __init__(self, search):
        self.response = self.readLinkedin(search)
        
    def getResponse(self):
        # print json.dumps(self.response, indent=4, sort_keys=True)
        return self.response
        
    def linkedinCompaniesParser(self, url):
        for i in range(5):
            try:
                headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
                response = requests.get(url, headers=headers)
                formatted_response = response.content.replace('<!--', '').replace('-->', '')
                doc = html.fromstring(formatted_response)
                datafrom_xpath = doc.xpath('//code[@id="stream-promo-top-bar-embed-id-content"]//text()')
                if datafrom_xpath:
                    try:
                        logo = 'https://media.licdn.com/mpr/mpr/shrink_200_200' 
                        json_formatted_data = json.loads(datafrom_xpath[0])
                        company_name = json_formatted_data['companyName'] if 'companyName' in json_formatted_data.keys() else None
                        company_id = json_formatted_data['companyId'] if 'companyId' in json_formatted_data.keys() else None
                        logo += json_formatted_data['squareLogo'] if 'squareLogo' in json_formatted_data.keys() else None
                        size = json_formatted_data['size'] if 'size' in json_formatted_data.keys() else None
                        industry = json_formatted_data['industry'] if 'industry' in json_formatted_data.keys() else None
                        description = json_formatted_data['description'] if 'description' in json_formatted_data.keys() else None
                        follower_count = json_formatted_data['followerCount'] if 'followerCount' in json_formatted_data.keys() else None
                        year_founded = json_formatted_data['yearFounded'] if 'yearFounded' in json_formatted_data.keys() else None
                        website = json_formatted_data['website'] if 'website' in json_formatted_data.keys() else None
                        type = json_formatted_data['companyType'] if 'companyType' in json_formatted_data.keys() else None
                        specialities = json_formatted_data['specialties'] if 'specialties' in json_formatted_data.keys() else None
    
                        if "headquarters" in json_formatted_data.keys():
                            city = json_formatted_data["headquarters"]['city'] if 'city' in json_formatted_data["headquarters"].keys() else None
                            country = json_formatted_data["headquarters"]['country'] if 'country' in json_formatted_data['headquarters'].keys() else None
                            state = json_formatted_data["headquarters"]['state'] if 'state' in json_formatted_data['headquarters'].keys() else None
                            street1 = json_formatted_data["headquarters"]['street1'] if 'street1' in json_formatted_data['headquarters'].keys() else None
                            street2 = json_formatted_data["headquarters"]['street2'] if 'street2' in json_formatted_data['headquarters'].keys() else None
                            zip = json_formatted_data["headquarters"]['zip'] if 'zip' in json_formatted_data['headquarters'].keys() else None
                            street = street1 + ', ' + street2
                        else:
                            city = None
                            country = None
                            state = None
                            street1 = None
                            street2 = None
                            street = None
                            zip = None
                            

                        data = {
                                    'company_name': company_name,
                                    'company_id': company_id,
                                    'logo': logo,
                                    'size': size,
                                    'industry': industry,
                                    'description': description,
                                    'follower_count': follower_count,
                                    'founded': year_founded,
                                    'website': website,
                                    'type': type,
                                    'specialities': specialities,
                                    'city': city,
                                    'country': country,
                                    'state': state,
                                    'street': street,
                                    'zip': zip,
                                    'url': url
                                }
                        return data
                    except:
                        print "cant parse page", url
    
                if len(response.content) < 2000 or "trk=login_reg_redirect" in url:
                    if response.status_code == 404:
                        print "linkedin page not found"
                        return "linkedin page not found"
                    else:
                        raise ValueError('redirecting to login page or captcha found')
            except :
                print "retrying :",url
    
    def readLinkedin(self, search):
        url = 'https://www.linkedin.com/company/' 
        url += search.replace(' ', '-')
        extracted_data = self.linkedinCompaniesParser(url)
        return extracted_data
