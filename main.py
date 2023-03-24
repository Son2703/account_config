from consumer import MessageConsumer
from flask import jsonify


import os
import json
import requests
broker = 'localhost:9092'
topic = 'test-topic'
group_id = 'consumer-1'





if __name__ == '__main__':
    while True:
        received = MessageConsumer(broker, topic, group_id).activate_listener()
        print (received)
        # MessageConsumer.get_data(received)
        # if received != None:
        #     print('vao day')
        #     function(received.value["function"], received, User)


        #     # match received.value["function"]:
        #     #     case 'create':
        #     #         User(received.value["username"], received.value["email"], received.value["password"]).create()
        #     #         # return jsonify({"success": True, "message": "User has been registered"})
        #     #
        #     #     case default:
        #     #         print('haha')
        #     # print('1111')




