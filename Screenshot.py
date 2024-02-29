import requests
import xml.etree.ElementTree as ET
from Upload import upload_file

config_file = ET.parse('resources/config.xml').getroot()


# Get response from screenshot machine
# Also get api query fields from config file
def make_screenshot(url):
    # If no url was introduced, the execution stops
    if url == '':
        quit()

    response = requests.get(config_file[0].text + "?key=" + config_file[1][0].text + "&url=" +
                            url + "&dimension=" + config_file[1][1].text + "&format=" + config_file[1][2].text)

    if not response.status_code == 200:
        print("Error")

    else:
        file_name = name_file(url)
        upload_file(response, file_name)


# This method removes the www subdomain, the cheme and the top domain
def name_file(url):
    split_url = url.split('/', 2)[-1]
    if split_url.startswith('www'):
        site_name = split_url.split('.', 2)[1]
    else:
        site_name = split_url.split('.')[0]

    file_name = "{}.jpg".format(site_name)
    return file_name
