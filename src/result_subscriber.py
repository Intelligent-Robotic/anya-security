import rospy
from std_msgs.msg import String
import sound_alarm
import socket
import requests



current_ip="http://10.164.36.238"
# Base URL
base_url = str(current_ip)+':8080/recorder'
text=[]
recording=False
def result_callback(msg):
    print("Received result:", msg.data)
    text=""
    if (msg.data=="start"):
        recording=True
    if (msg.data=="complete"):
        # Query parameters
        params = {
            'text': ' '.join(text),
        }

        # Construct the URL with query parameters
        respond = requests.get(base_url,params=params)

        print(respond)
        text=[]
        recording=False
    if recording:
        text.append(msg.data)

if __name__ == '__main__':
    rospy.init_node('result_subscriber')
    rospy.Subscriber('/result', String, result_callback)
    rospy.spin()
