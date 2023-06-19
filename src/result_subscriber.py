import rospy
from std_msgs.msg import String
import sound_alarm
import urllib2
import socket



def get_current_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

current_ip = get_current_ip()
# Base URL
base_url = f'{current_ip}:8080/recorder/'
text=[]
recording=False
def result_callback(msg):
    print("Received result:", msg.data)
    
    if (msg.data=="record"):
        recording=True
    if (msg.data=="done"):
        # Query parameters
        params = {
            'text': ' '.join(text),
        }

        # Construct the URL with query parameters
        url = base_url + '?' + urllib2.urlencode(params)
        response = urllib2.urlopen(url)
        print(response.read())
        text=[]
        recording=False
    if recording:
        text.append(msg.data)

if __name__ == '__main__':
    rospy.init_node('result_subscriber')
    rospy.Subscriber('/result', String, result_callback)
    rospy.spin()
