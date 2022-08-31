# Use this file to setup the database consumer that stores the ride information in the database
import requests
import pika
import sqlite3
import json
import time
import os  

conn = sqlite3.connect('ride.db')
print("Opened database successfully")
conn.execute('''CREATE TABLE  IF NOT EXISTS RIDE3
	(pickup TEXT,
	 destination TEXT,
	 time INT,
	 cost INT,
	 seats INT);''')
print("Table created successfully")

#time.sleep(60)
amqp_url = os.environ['AMQP_URL']
print('URL: %s' % (amqp_url,))
parameters = pika.URLParameters(amqp_url)
#connection = pika.SelectConnection(parameters, on_open_callback=on_open)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='database')

def callback(ch,method,properties,body):
	ride_details=json.loads(body)
	print(ride_details)
	conn.execute("INSERT INTO RIDE3 VALUES (?,?,?,?,?)", [ride_details["pickup"], ride_details["destination"], int(ride_details["time"]),int(ride_details["cost"]),int(ride_details["seats"])])
	conn.commit()
	cursor=conn.execute("SELECT * FROM RIDE3;")
	for row in cursor:
		print(row)
	conn.close()
	
	

channel.basic_consume(queue='database',auto_ack=True,on_message_callback=callback)
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

