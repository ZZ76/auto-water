from aws.iot import mqtt_receiver
import config
import os
import time
import pandas as pd
import logging
import s3
from datetime import datetime
import json
import water
from watering_device import WateringDevice


log = config.LOG_FILE
csv_file = config.CSV_FILE
duty = config.DUTY
pin = config.PIN
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log, encoding='utf-8', level=logging.INFO)
water_topic = 'sdk/auto-water/water'
update_topic = 'sdk/auto-water/update'

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def water_and_write_data(topic, payload, dup, qos, retain, **kwargs):
    try:
        data = json.loads(payload)
        water_duration = int(data['duration'])
        now = datetime.now()
        start = now.strftime('%H:%M:%S')
        # watering
        print(f'{get_current_time()} Starting unscheduled task')
        logging.info('Starting unscheduled task')
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
    except Exception as e:
        print(e)
    finally:
        s3.upload_log()

def update_parameters(topic, payload, dup, qos, retain, **kwargs):
    try:
        data = json.loads(payload)
        print('Update parameters...')
        print(f'{data}')
        logging.info('Update parameters...')
        logging.info(f'{data}')
        if 'start_time' in data.keys():
            WateringDevice.start_time = int(data['start_time'])
        if 'gap_days' in data.keys():
            WateringDevice.gap_days = int(data['gap_days'])
        if 'duration' in data.keys():
            WateringDevice.water_duration = int(data['duration'])
    except Exception as e:
        print(e)
    finally:
        s3.upload_log()

def check_parameters(topic, payload, dup, qos, retain, **kwargs):
    try:
        print(f'''Checking parameters:
        start_time: {WateringDevice.start_time}
        duration: {WateringDevice.water_duration}
        gap_days: {WateringDevice.gap_days}
        ''')
        logging.info(f'''Checking parameters:
        start_time: {WateringDevice.start_time}
        duration: {WateringDevice.water_duration}
        gap_days: {WateringDevice.gap_days}
        ''')
    except Exception as e:
        print(e)
        logging.error(f'{e}')
    finally:
        s3.upload_log()

def print_message(topic, payload, dup, qos, retain, **kwargs):
    try:
        print(f"Received message from topic '{topic}': {payload}")
        print(payload)
        data = json.loads(payload)
        for k in  data.keys():
            print(f'{k} : {data[k]}')
            print(f'{type(data[k])}')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    try:
        MqttReceiver = mqtt_receiver.MqttReceiver()
        MqttReceiver.subscribe(config.IOT_WATER_TOPIC, water_and_write_data)
        MqttReceiver.subscribe(config.IOT_UPDATE_TOPIC, print_message)
        MqttReceiver.subscribe(config.IOT_CHECK_TOPIC, print_message)
        while True:
            print('receiveing')
            time.sleep(5)
    except:
        MqttReceiver.disconnect()
        print('exception')
