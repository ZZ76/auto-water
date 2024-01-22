from watering_device import WateringDevice
from aws.iot import mqtt_receiver
import config
import iot
import logging

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log, encoding='utf-8', level=logging.INFO)

if __name__ == '__main__':
    try:
        device = WateringDevice()
        # Start mqtt and subscribe
        MqttReceiver = mqtt_receiver.MqttReceiver()
        MqttReceiver.subscribe(config.IOT_WATER_TOPIC, iot.water_and_write_data)
        MqttReceiver.subscribe(config.IOT_UPDATE_TOPIC, iot.update_parameters)
        MqttReceiver.subscribe(config.IOT_CHECK_TOPIC, iot.check_parameters)

        # Start watering device
        device.start()
    except Exception as e:
        print(e)
        logging.error(f'{e}')
    except KeyboardInterrupt as e:
        print('Interrupted')
        logging.error(f'{e}')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        logging.error(f'{sys.exc_info()[0]}')
