#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from flask import Flask, request
import pygame
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
import time

soundhandle = SoundClient()

app = Flask(__name__)

@app.route('/sound_alarm', methods=['GET'])
def sound_alarm():
    # Publish a message to trigger the alarm
    pub.publish("play_alarm")
    return "Alarm triggered"


@app.route('/sound_ohayo', methods=['GET'])
def sound_ohayo():
    # Publish a message to trigger the alarm
    pub.publish("play_ohayo")
    return "Ohayo triggered"

@app.route('/sound_song', methods=['GET'])
def sound_song():
    # Publish a message to trigger the alarm
    pub.publish("play_song")
    return "Song triggered"


@app.route('/speak', methods=['GET'])
def speech():
    text_value = request.args.get('text', 'no message')
    soundhandle.say(text_value)
    return ("speak text :"+text_value)



def alarm_callback(msg):
    print(msg.data)
    if msg.data == "play_alarm":
        import pygame
        pygame.init()
        pygame.mixer.music.load('sound1.mp3')
        pygame.mixer.music.play()

        # Wait for 10 seconds
        time.sleep(2)

        # Stop the playback
        pygame.mixer.music.stop()

    elif msg.data == "play_ohayo":
        import pygame
        pygame.init()
        pygame.mixer.music.load('sound2.mp3')
        pygame.mixer.music.play()

        # Wait for 10 seconds
        time.sleep(2)

        # Stop the playback
        pygame.mixer.music.stop()

    elif msg.data == "play_song":
        import pygame
        pygame.init()
        pygame.mixer.music.load('sound3.mp3')
        pygame.mixer.music.play()

        # Wait for 10 seconds
        time.sleep(2)

        # Stop the playback
        pygame.mixer.music.stop()


def main():
    rospy.init_node('alarm_node', anonymous=True)
    global pub
    pub = rospy.Publisher('alarm_trigger', String, queue_size=10)
    rospy.Subscriber('alarm_trigger', String, alarm_callback)

    app.run(host='0.0.0.0', port=8000, threaded=True)

if __name__ == '__main__':
    main()
