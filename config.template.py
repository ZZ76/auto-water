
CSV_FILE = './data.csv'
LOG_FILE = './log' 
START_TIME = 6 # what time start watering 0 to 23
WATER_DURATION = 5 # water how many seconds
GAP_DAYS = 0 # gap days that not to water, 0 means everyday
CHECK_INTERVAL = 1800 # wait how many seconds for checking, 1800s = 30mins
PIN = 17 # IO, GPIO 17 is low by default when boot up
DUTY = 35 # pwm duty cycle
FREQUENCY = 500
BUCKET_NAME = 's3-bucket-name'
AWS_REGION = 'ap-southeast-2'
AWS_KEY_ID = 'ASKEYIDKEYIDKEYIDKEY'
AWS_KEY_SECRET = 'keysecretKEYSECRETkeysecretKEYSECRETkeys'
FUNCTION_NAME = 'lambda-function-name'

# aws iot
IOT_INPUT_ENDPOINT = 'endpoint-of.iot.region.amazonaws.com'
IOT_INPUT_PORT = 8883
IOT_INPUT_CERT = 'path-to.cert.pem'
IOT_INPUT_KEY = 'path-to.private.key'
IOT_INPUT_CA = 'path-to-root-CA.crt'
IOT_INPUT_CLIENTID = 'basicPubSub'
IOT_WATER_TOPIC = 'topic for watering'
IOT_UPDATE_TOPIC = 'topic for updating parameters'
IOT_CHECK_TOPIC = 'topic for checking parameters'
