import pandas as pd
import time
from datetime import datetime, timedelta
import logging
import sys
import s3
import water
import config
import iot
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

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log, encoding='utf-8', level=logging.INFO)
logging.info('Start')

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
            print(f'{get_current_time()} Watering...')
            logging.info('Watering...')
            water.water_pwm(water_duration, pin=pin, duty=duty)
            # finish, writing data
            print(f'{get_current_time()} Watering completed')
            logging.info('Watering completed')
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
            logging.info(f'Writing data...\n{new_df}')
            #df.append(new_df)
            new_df.to_csv(csv_file, mode='a', header=False, index=False)
            # upload csv here
            s3.upload_csv()
        else:
            print(f'{get_current_time()} Not the right time to water yet today')
            logging.info('Not the right time to water yet today')
            return
    else:
        next_day = last_day + timedelta(gap_days)
        next_day_string = next_day.strftime('%Y-%m-%d')
        print(f'{get_current_time()} Watering already completed. Next scheduled watering: {next_day_string}, after {start_time}, for {water_duration}s')
        logging.info(f'Watering already completed. Next scheduled watering: {next_day_string}, after {start_time}, for {water_duration}s')


class WateringDevice():
    log = config.LOG_FILE
    csv_file = config.CSV_FILE
    start_time = config.START_TIME
    water_duration = config.WATER_DURATION
    check_interval = config.CHECK_INTERVAL
    gap_days = config.GAP_DAYS
    duty = config.DUTY
    pin = config.PIN

    def __init__():
        pass

    def start():
        while True:
            df = pd.read_csv(csv_file)
            last_date = df.iloc[-1].date
            process_last_date(last_date)
            #upload log here
            s3.upload_log()
            time.sleep(check_interval)

if __name__ == '__main__':
    try:
        device = WateringDevice()
        # Start mqtt and subscribe
        MqttReceiver = mqtt_receiver.MqttReceiver()
        MqttReceiver.subscribe(water_topic, iot.water_and_write_data)
        MqttReceiver.subscribe(update_topic, iot.print_message)

        # Start watering device
        device.start()
        #while True:
        #    df = pd.read_csv(csv_file)
        #    last_date = df.iloc[-1].date
        #    process_last_date(last_date)
        #    #upload log here
        #    s3.upload_log()
        #    time.sleep(check_interval)
    except Exception as e:
        print(e)
        logging.error(f'{e}')
    except KeyboardInterrupt as e:
        print('Interrupted')
        logging.error('KeyboardInterrupt')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        logging.error(f'{sys.exc_info()[0]}')
