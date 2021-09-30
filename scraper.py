import requests, csv, os
from bs4 import BeautifulSoup

def scrap(day, month, year = 2021, write_to_csv = False, filename = 'predictions'):
    games = []
    url = 'https://www.forebet.com/en/football-predictions/under-over-25-goals/{}-{}-{}'.format(year, str(month).zfill(2), str(day).zfill(2))
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('div', {'class': 'schema tbuo'})
    tr_0 = table.findAll('div',{'class': 'rcnt tr_0'})
    tr_1 = table.findAll('div',{'class': 'rcnt tr_1'})

    lines = tr_0 + tr_1
    
    for line in lines:
        game_played = True if not line.findAll('div', {'class': 'predict'}) else False
        if(game_played):
            liga = line.find('div', {'class': 'stcn'}).find('span', {'class': 'shortTag'}).text
            homeTeam = line.find('div', {'class': 'tnms'}).find('span', {'class': 'homeTeam'}).text
            awayTeam = line.find('div', {'class': 'tnms'}).find('span', {'class': 'awayTeam'}).text
            date = line.find('div', {'class': 'tnms'}).find('time').span.text
            probUnder = int(line.find('div', {'class': 'fprc'}).findAll('span')[0].text)
            probOver = int(line.find('div', {'class': 'fprc'}).findAll('span')[1].text)
            predicted_result = line.find('span', {'class': 'forepr'}).span.text
            odd_str = line.find('div', {'class': 'bigOnly prmod'}).span.text
            if(odd_str != ' - '):
                odd = float(odd_str)
                score_arr = line.find('b', {'class': 'l_scr'}).text.split('-')
                scoreHomeTeam = int(score_arr[0])
                scoreAwayTeam = int(score_arr[1])

                if(line.findAll('div', {'class': 'predict_y'})):
                    result = 'win'
                else:
                    if(line.findAll('div', {'class': 'predict_no'})):
                        result = 'lose'
                    else:
                        result = 'undefined'

                game = {'liga': liga, 'homeTeam': homeTeam, 'awayTeam': awayTeam, 'probUnder': probUnder, 'probOver': probOver, 'predicted_result': predicted_result, 'odd': odd, 'scoreHomeTeam': scoreHomeTeam, 'scoreAwayTeam': scoreAwayTeam, 'result': result, 'date': date}
                games.append(game)

    if(write_to_csv):
        with open('{}.csv'.format(filename), mode = 'a', newline='\n', encoding='utf-8') as file:
            writer = csv.writer(file)
            if(os.stat('predictions.csv').st_size == 0):
                writer.writerow(game.keys())
            for game in games:
                writer.writerow(game.values())

def read_from_csv(filename):
    games = []
    with open('{}.csv'.format(filename), mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            games.append(row)
    return games

def scrap_month(month, filename = 'predictions'):
    for day in range(1,32):
        print("Day {}".format(day))
        scrap(day, month, write_to_csv = True, filename = filename)

def main():
    scrap_month(9)

if __name__ == '__main__':
    main()