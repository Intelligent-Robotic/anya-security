#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from flask import Flask
import pygame

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


def alarm_callback(msg):
    print(msg.data)
    if msg.data == "play_alarm":
        import pygame
        pygame.init()
        pygame.mixer.music.load('sound1.mp3')
        pygame.mixer.music.play()

        # Wait for 10 seconds
        time.sleep(10)

        # Stop the playback
        pygame.mixer.music.stop()
    elif msg.data == "play_ohayo":
        import pygame
        pygame.init()
        pygame.mixer.music.load('sound2.mp3')
        pygame.mixer.music.play()

        # Wait for 10 seconds
        time.sleep(10)

        # Stop the playback
        pygame.mixer.music.stop()

    elif msg.data == "play_song":
        import pygame
        pygame.init()
        pygame.mixer.music.load('sound3.mp3')
        pygame.mixer.music.play()

        # Wait for 10 seconds
        time.sleep(10)

        # Stop the playback
        pygame.mixer.music.stop()


def main():
    rospy.init_node('alarm_node', anonymous=True)
    global pub
    pub = rospy.Publisher('alarm_trigger', String, queue_size=10)
    rospy.Subscriber('alarm_trigger', String, alarm_callback)

    # pub = rospy.Publisher('song_trigger', String, queue_size=10)
    # rospy.Subscriber('song_trigger', String, song_callback)
    app.run(host='0.0.0.0', port=8000, threaded=True)

if __name__ == '__main__':
    main()
