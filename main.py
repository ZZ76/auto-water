import pandas as pd
import time
from datetime import datetime
import logging
import sys
import s3
import water
import config
'''
csv file:
date, start, finish, duration
yyyy-mm-dd, HH-MM-SS, HH-MM-SS, int
water after 6am, use now.hour

while True:
  1.load latest data time
  2.get current time
  3.calculate time delta between current time and data time, compare with gap days
  4.if True:
          water
          write data
      else:
          pass
    sleep interval
'''

log = config.LOG_FILE
csv_file = config.CSV_FILE
start_time = config.START_TIME
water_duration = config.WATER_DURATION
check_interval = config.CHECK_INTERVAL
gap_days = config.GAP_DAYS
duty = config.DUTY
pin = config.PIN

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log, encoding='utf-8', level=logging.INFO)
logging.info(f'start')

#def water():
#    time.sleep(water_duration)

def process_last_date(d: str):
    global df
    now = datetime.now()
    last_day = datetime.strptime(d, '%Y-%m-%d')
    if now.day - last_day.day > gap_days:
        if now.hour >= start_time:
            start = now.strftime('%H:%M:%S')
            # watering
            print(f'{get_current_time()} watering...')
            logging.info(f'watering...')
            water.water_pwm(water_duration, pin=pin, duty=duty)
            # finish, writing data
            finish_time = datetime.now()
            finish = finish_time.strftime('%H:%M:%S')
            new_date = now.strftime('%Y-%m-%d')
            duration = (finish_time - now).seconds
            new_df = pd.DataFrame([[
                new_date,
                start,
                finish,
                duration
                ]],
                columns=[
                    'date',
                    'start',
                    'finish',
                    'duration'
                    ]
                )
            #print(new_df)
            #print(new_date, start, finish, duration)
            logging.info(f'writing data...\n{new_df}')
            #df.append(new_df)
            new_df.to_csv(csv_file, mode='a', header=False, index=False)
            # upload csv here
            s3.upload_csv()
        else:
            print(f'{get_current_time()} too early to water for today')
            logging.info(f'too early to water for today')
            return
    else:
        print(f'{get_current_time()} already watered')
        logging.info(f'already watered')


try:
    while True:
        df = pd.read_csv(csv_file)
        last_date = df.iloc[-1].date
        process_last_date(last_date)
        #upload log here
        s3.upload_log()
        time.sleep(check_interval)
except Exception as e:
    print(e)
    logging.error(f'{e}')
except KeyboardInterrupt as e:
    print('Interrupted')
    logging.error(f'KeyboardInterrupt')
except:
    print("Unexpected error:", sys.exc_info()[0])
    logging.error(f'{sys.exc_info()[0]}')
