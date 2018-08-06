#!/usr/bin/python3.6

import billboard
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import time
from multiprocessing import Process




def top_songs(mm, dd, yyyy):
    chart = billboard.ChartData('hot-100', date=f'{yyyy}-{mm}-{dd}', fetch=True, timeout=25)
    for i in range(0, 10):
        top_song = chart[i]
        print(i+1, '. ', top_song.title, sep='')


def validate(date_input):
    try:
        # may more format error checking such as 005/23/1994
        valid_date = datetime.strptime(date_input, '%m/%d/%Y').date()
        if not (date(1958, 8, 4) <= valid_date <= date.today()):
            print("Incorrect Format or Date: Should be MM/DD/YYYY and "
                  "between 08/04/1958 and", time.strftime('%m/%d/%Y'))
            print("Please try again.")
            main()
        else:
            mm, dd, yyyy = date_input.split('/')
            return mm, dd, yyyy
    finally:
        pass


def yearly_song(mm, dd, yyyy):
    now = datetime.today()
    bday = date(int(yyyy), int(mm), int(dd))
    today = date(now.year, now.month, now.day)

    while bday < today:
        chart = billboard.ChartData('hot-100', date=bday, fetch=True, timeout=25)
        print(bday, ':', chart[0])
        bday = bday + relativedelta(years=1)

    return


def main():
    try:
        month, day, year = validate(date_input=input('Input date (mm/dd/yyyy): '))
        top_songs(month, day, year)
        print(f"\nTop 10 songs on {month}/{day}/{year} returned above.\n")
        '''
        p = Process(target=yearly_song, args=(month, day, year))
        p.start()
        p.join()
        '''
        yearly_song(month, day, year)  # This was before I added process to see if I could speed it up
    # this is needed due to receiving "TypeError 'NoneType'" error when someone enters wrong format or date then loops
    # back to main and enters a correct date and format. Not sure why but this handles it for now.
    except TypeError:
        pass


if __name__ == '__main__':
    main()



