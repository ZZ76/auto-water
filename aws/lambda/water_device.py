import json
import boto3

client = boto3.client('iot-data', region_name='ap-northeast-1')
message = {}

def lambda_handler(event, context):
    '''
    TODO implement
    action: str
        water
        update
    if action is water:
        duration: int # seconds
    if action is update:
        duration: int # seconds
        gap-days: int # days
        start-time: int # time to start watering
    '''
    print(f'event:\n{event}')
    print(event.keys())

    try:
        parameters = event['queryStringParameters']
        action = parameters['action']
        if action == 'water':
            duration = parameters['duration']
            topic = 'sdk/auto-water/water'
            message = {'duration': duration}
        elif action == 'update':
            topic = 'sdk/auto-water/update'
            message = {k: parameters[k] for k in set(parameters.keys()) - {'action'}}
        elif action == 'check':
            topic = 'sdk/auto-water/check'
            message = {k: parameters[k] for k in parameters.keys()}
        else:
            pass
        print(f'message: {message}')
        response = client.publish(
            topic=topic,
            qos=1,
            payload=json.dumps(message)
        )
        print(f'response: {response}')

        return {
            'statusCode': 200,
            'body': json.dumps('Published to topic')
        }
    except Exception as e:
        return {
            'statusCode': 502,
            'body': f'{e}'
         }
