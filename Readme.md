# AirCopy: Copy files from one PC to another with hand gestures

## Hand Gesture Recognition: Forked from https://github.com/kinivi/hand-gesture-recognition-mediapipe

## Networking and file transfer implementation:

The sender machine waits for a UDP datagram. The receiver broadcasts the UDP. The sender, on receiving, gets the IP Address of the receiver. The receiver opens a TCP socket and the Sender sends the files through that. The receiver first stores it into a Buffer and then processes it and writes to respective files in the downloads folder.

## Video
https://youtu.be/v0T0SydoO_U?si=8NdRQOHBqOtWeZML
