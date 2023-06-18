#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import socket
from flask import Flask, Response

app = Flask(__name__)
bridge = CvBridge()
image_pub = rospy.Publisher('video_stream', Image, queue_size=10)
video_capture = cv2.VideoCapture(2)


def get_ip_address():
    # Create a socket to get the IP address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    ip_address = sock.getsockname()[0]
    sock.close()
    return ip_address


def video_stream_generator():
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        image_msg = bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        image_pub.publish(image_msg)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_data = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    rospy.init_node('video_publisher', anonymous=True)
    ip_address = get_ip_address()
    print("Open this URL in your browser on the same network: http://{}:5000/video_feed".format(ip_address))
    app.run(host='0.0.0.0', port=5000)
