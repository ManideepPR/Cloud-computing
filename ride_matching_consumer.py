# Code for Ride Matching Consumer
import os 
import requests
import pika
import time

#time.sleep(60)
server_ip = os.getenv('SERVER_IP',"localhost")
consumer_id = os.getenv('CONSUMER_ID',"default")
print("ready")
print("make request")
send_to = "http://{}/new_ride_matching_consumer".format(server_ip)
time.sleep(20)
r= requests.post(send_to,data={"consumer_id":consumer_id})#Format string server ip to localhost:
amqp_url = os.environ['AMQP_URL']
print('URL: %s' % (amqp_url,))
parameters = pika.URLParameters(amqp_url)
#connection = pika.SelectConnection(parameters, on_open_callback=on_open)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='ride-sharing')

def callback(ch,method,properties,body):
	sleep_time = int(body)
	print(sleep_time)
	time.sleep(sleep_time)
	print(consumer_id)#Also print task id ?

channel.basic_consume(queue='ride-sharing',auto_ack=True,on_message_callback=callback)
#connection.close()
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

