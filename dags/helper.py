from bs4 import BeautifulSoup
import re
from requests import get
from datetime import datetime
from os.path import dirname, abspath

def find_no_of_cases():

    dir_path = dirname(dirname(abspath(__file__)))
    print(dir_path)
    URL = 'https://www.mygov.in/covid-19/'
    response = get(URL)

    value  = re.compile("^color")
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.find_all("div", {"class": "information_row"})
    for data in mydivs:
        time = data.find("span").text
        counts = data.find_all("span",{'class':'icount'})
        div_count = data.find_all("div",{'class':value})

    Total_cases = counts[0].text
    Active_cases = counts[1].text
    Discharged = counts[2].text
    Deaths = counts[3].text

    total_cases_class = div_count[0]["class"]
    total_cases_value = div_count[0].text.strip()
    if('up-arrow' in total_cases_class):
        total_cases_text = f'There has been an increase in {total_cases_value} number of cases'
    else:
        total_cases_text = f'There has been decrease in {total_cases_value} number of cases'

    active_cases_class = div_count[1]["class"]
    active_cases_value = div_count[1].text.strip()
    if('up-arrow' in active_cases_class):
        active_cases_text = f'There has been an increase in {active_cases_value} number of active cases'
    else:
        active_cases_text = f'There has been decrease in {active_cases_value} number of active cases'

    discharged_class = div_count[2]["class"]
    discharged_value = div_count[2].text.strip()
    if('up-arrow' in discharged_class):
        discharged_cases_text = f'There has been an increase in {discharged_value} number of people discharged from hospital'
    else:
        discharged_cases_text = f'There has been decrease in {discharged_value} number of people discharged from hospital'


    deaths_class = div_count[3]["class"]
    death_value = div_count[3].text.strip()
    if('up-arrow' in deaths_class):
        death_cases_text = f'There has been an increase in {death_value} number of deaths'
    else:
        death_cases_text = f'There has been decrease in {death_value} number of deaths'

    print(time)
    print("Total_cases : ",Total_cases)
    print("Active_cases : ",Active_cases)
    print("Discharged : ",Discharged)
    print("Deaths : ",Deaths)

    print(total_cases_text)

    print(active_cases_text)

    print(discharged_cases_text)

    print(death_cases_text)
    
    date_val = datetime.today().strftime('%Y-%m-%d')
    f = open(f'{dir_path}/data/cases_india_{date_val}.txt', "w")
    f.write(f'{time}<br>\n')
    f.write(f'Total_cases : {Total_cases}<br>\n')
    f.write(f'Active_cases : {Active_cases}<br>\n')
    f.write(f'Discharged : {Discharged}<br>\n')
    f.write(f'Deaths :  {Deaths}<br>\n')
    f.write(f'{total_cases_text}<br>\n')
    f.write(f'{active_cases_text}<br>\n')
    f.write(f'{discharged_cases_text}<br>\n')
    f.write(f'{death_cases_text}<br>\n')
    f.close()


def create_email_content(**context):
    date_val = datetime.today().strftime('%Y-%m-%d')
    dir_path = dirname(dirname(abspath(__file__)))
    with open(f'{dir_path}/data/cases_india_{date_val}.txt', 'r') as file:
        data = file.read().splitlines()
        file.close()
    content = ""
    for i in data:
        content = f'{content}{i}\n'
    task_instance = context["task_instance"]
    task_instance.xcom_push(key="email_content", value=content)
    print(content)
