import requests
import json
from bs4 import BeautifulSoup
import datetime


def getScore(year, month):
    url = 'https://www.koreabaseball.com/ws/Schedule.asmx/GetScheduleList'

    data = {
        'leId': '1',
        'srIdList': '0,9,6',
        'seasonId': year,
        'gameMonth': str(month).zfill(2),
        'teamId': ''
    }

    response = requests.post(url, data=data)

    # json to python object
    # Parse the response text into a Python object
    response_text = response.text
    resDict = json.loads(response_text)

    # Initialize variables to keep track of the current date
    current_date = ""

    # Loop through each game's information
    for game in resDict['rows']:
        row = game['row']

        # Extract date if available
        if row[0]['Class'] == 'day':
            current_date = row[0]['Text']
            time_index = 1
            play_index = 2
            note_index = 8
        else:
            time_index = 0
            play_index = 1
            note_index = 7

        # Extract time
        time_soup = BeautifulSoup(row[time_index]['Text'], 'html.parser')
        time = time_soup.get_text()

        # Extract teams and result
        play_soup = BeautifulSoup(row[play_index]['Text'], 'html.parser')
        teams_result = play_soup.get_text(separator=' ')

        note_soup = BeautifulSoup(row[note_index]['Text'], 'html.parser')
        note = note_soup.get_text()


        month = int(current_date.split('.')[0])
        day = int(current_date.split('.')[1].split('(')[0])

        # 2018년 10월 6일 KIA 5 vs 7 SK 경기 정보만 오류남 (시간이 없음)
        if year ==2018 and month == 10 and time == "":
            time ="18:45"

        hour = time.split(':')[0]
        minute = time.split(':')[1]
        KST = datetime.timezone(datetime.timedelta(hours=9))
        gameTime = datetime.datetime(year, month, day, int(hour), int(minute), tzinfo=KST)

        # Extract teams and result
        A, AScore, B, BScore, winner = splitScore(teams_result)
        print(f"{gameTime} {A} vs {B} {AScore} : {BScore} Winner: {winner} {note}  ")


def splitScore(matchResult):
    A, B = matchResult.split('vs')
    AandScore = sorted(A.split(' '))
    BandScore = sorted(B.split(' '))
    if len(AandScore) == 2:
        A = AandScore[1]
        A_score = None
    else:
        A = AandScore[2]
        A_score = int(AandScore[1])

    if len(BandScore) == 2:
        B = BandScore[1]
        B_score = None
    else:
        B = BandScore[2]
        B_score = int(BandScore[1])

    if A_score is None or B_score is None:
        return A, A_score, B, B_score, None
    else:
        if A_score == B_score:
            winner = 'Draw'
        elif A_score > B_score:
            winner = A
        else:
            winner = B
        return A, A_score, B, B_score, winner



for year in range(2001, 2025):
    for month in range(1, 13):
        getScore(year,month)
