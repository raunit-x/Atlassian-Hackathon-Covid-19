import datetime
import json
import requests

from bs4 import BeautifulSoup
from tabulate import tabulate
from slack_client import slacker
from collections import namedtuple


Constants = namedtuple("Constants", ["URL", "TABLE_HEADERS", "FILE_NAME", "STATE"])
my_constants = Constants('https://www.mohfw.gov.in/', ['Sno', 'State/UT', 'Confirmed', 'Migrated/Cured', 'Deaths'], 
                         'corona_india_data.json', 'Delhi')


def extract_contents(curr_row):
    return [x.text.replace('\n', '') for x in curr_row]


def save(x):
    with open(my_constants.FILE_NAME, 'w') as f:
        json.dump(x, f)


def load():
    res = {}
    with open(my_constants.FILE_NAME, 'r') as f:
        res = json.load(f)
    return res


def find_change(curr_data, prev_data, current_time) -> bool:
    flag = False
    for cur_state in curr_data:
        if cur_state not in prev_data:
            info.append(f'NEW_STATE {cur_state} got corona virus: {curr_data[cur_state][current_time]}')
            prev_data[cur_state] = {}
            flag = True
        else:
            prev = prev_data[cur_state]['latest']
            curr = curr_data[cur_state][current_time]
            if prev != curr:
                flag = True
                info.append(f'Changes for {cur_state}: {prev}->{curr}')
    return flag


def scrape_from_url():
    response = requests.get(my_constants.URL).content
    soup = BeautifulSoup(response, 'html.parser')
    stats = []
    my_state_stat = []
    # my_state = 'Delhi'
    all_rows = soup.find_all('tr')
    for row in all_rows:
        stat = extract_contents(row.find_all('td'))
        # print(stat)
        if stat:
            if len(stat) == 5:
                if stat[1] == my_constants.STATE:
                    my_state_stat.append(stat)
                stat = ['', *stat]
                stats.append(stat)
    return stats, my_state_stat


def main():
    current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    info = []
    try:
        stats, my_state_stat = scrape_from_url()
        past_data = load()
        cur_data = {x[1]: {current_time: x[2:]} for x in stats}
        changed = find_change(cur_data, past_data, current_time)
        events_info = ''
        for event in info:
            events_info += '\n - ' + event.replace("'", "")
        # changed = True
        if changed:
            for state in cur_data:
                past_data[state]['latest'] = cur_data[state][current_time]
                past_data[state][current_time] = cur_data[state][current_time]
            save(past_data)
            table = tabulate(stats, headers=my_constants.TABLE_HEADERS, tablefmt='psql')
            table2 = tabulate(my_state_stat, headers=my_constants.TABLE_HEADERS, tablefmt='psql')
            slack_text = f'`{my_constants.STATE}`(Your State/UT) details:\n```{table2}```'
            slacker()(slack_text)
            slack_text = f'Please find Coronavirus stats for all Indian States/UT below:\n{events_info}\n ```{table}```'
            slacker()(slack_text)
    except Exception as e:
        slacker()(f'Exception occurred: [{e}]')


if __name__ == '__main__':
    main()
