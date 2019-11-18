from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import random
import time
from datetime import date, datetime


host = "Replacewithyours.iot.eu-west-3.amazonaws.com"
topic = "temperature"
clientId = "Replacewithyours-awsiotpublish"

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials('Replacewithyours-root-CA.pem', 'Replacewithyours-private.pem.key', 'Replacewithyours-certificate.pem.crt')

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    message = {}
    now = datetime.utcnow()
    current = datetime.now().isoformat(timespec='milliseconds')
    current_str = now.strptime(current,'%Y-%m-%dT%H:%M:%S.%f')
    current_timestamp = current_str.timestamp()
    datetosend = datetime.fromtimestamp(current_timestamp + 0.02).strftime('%Y-%m-%dT%H:%M:%S.%f')

    messageJson = json.dumps(message)
    messageJson = '{ "timestamp": "' + datetosend + '","temperature": ' + str(random.uniform(1,70)) + '}'

    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    time.sleep(1)
myAWSIoTMQTTClient.disconnect()
