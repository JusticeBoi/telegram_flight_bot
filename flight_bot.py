from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
import pandas as pd
from datetime import datetime
from sky_picker import SkyPickerApi
from sky_picker_helper import time_of_day, prepare_final, prepare_sp_data, convert_to_date_string, convert_to_time_string

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def bop(bot, update, args):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)
    bot.send_message(chat_id=chat_id, text='asd')
    for arg in args:
        bot.send_message(chat_id=chat_id, text=arg)

def IstToMuc(bot, update, args):
    chat_id = update.message.chat_id
    if len(args) != 2:
        bot.send_message(chat_id=chat_id, text='I need two arguments, first is date of departure, second is date of arrival')
        bot.send_message(chat_id=chat_id, text='format = %m/%d/%y i.e. 04/24/1980 ')

    sp_api = SkyPickerApi()
    try:
        departure_date_dt = datetime.strptime(args[0], '%m/%d/%Y')
        arrival_date_dt = datetime.strptime(args[1], '%m/%d/%Y')
    except ValueError:
        bot.send_message(chat_id=chat_id, text='invalid date given')

    sky_picker_resp = sp_api.search_flights('MUC', 'IST', departure_date_dt, arrival_date_dt, 1)

    sky_picker_final = prepare_sp_data(sky_picker_resp)
    sky_picker_final = prepare_final(sky_picker_final)
    sky_picker_final.drop(sky_picker_final[sky_picker_final.num_stops > 0].index, inplace=True)
    index_to_be_deleted = []
    for row in sky_picker_final.itertuples(index=True, name='Pandas'):
        if (row.departure.day != departure_date_dt.day and row.departure.day != arrival_date_dt.day):
            index_to_be_deleted.append(row.Index)

    cols_to_be_deleted = ['legs','arrival','departure_tod','duration_hours', 'search_engine', 'num_stops']
    sky_picker_final.drop(index_to_be_deleted, inplace=True)
    sky_picker_final.drop(cols_to_be_deleted, axis=1, inplace=True)

    sky_picker_final['time'] = sky_picker_final['departure'].apply(convert_to_time_string)
    sky_picker_final['departure'] = sky_picker_final['departure'].apply(convert_to_date_string)
    sky_picker_final = sky_picker_final.sort_values("departure")
    departures_rows = []

    arrivals_rows = []
    departures = pd.DataFrame()
    arrivals = pd.DataFrame()
    for row in sky_picker_final.itertuples(index=True, name='Pandas'):
        if ( int(row.departure[0:2]) == arrival_date_dt.day ):
            arrivals_rows.append(row)
        else:
            departures_rows.append(row)
    departures = departures.append(departures_rows)
    arrivals = arrivals.append(arrivals_rows)
    departures.drop(['Index'], axis=1, inplace=True)
    arrivals.drop(['Index'], axis=1, inplace=True)

    bot.send_message(chat_id=chat_id, text=departures.to_string(index=False))
    bot.send_message(chat_id=chat_id, text=arrivals.to_string(index=False))
def main():
    updater = Updater('881782290:AAGdtWZAtHuNe1O93ZWY2Ua8EbtBFoAKLnc')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop, pass_args=True))
    dp.add_handler(CommandHandler('istmuc',IstToMuc, pass_args=True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
