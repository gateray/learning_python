#!/usr/bin/env python
# coding: utf-8

class AudioFile:
    def __init__(self, filename):
        if not filename.endswith(self.ext):
            raise Exception("Invalid file format")
        self.filename = filename

class MP3File(AudioFile):
    ext = "mp3"
    def play(self):
        print("playing {} as mp3".format(self.filename))

class WavFile(AudioFile):
    ext = "wav"
    def play(self):
        print("playing {} as wav".format(self.filename))

class OggFile(AudioFile):
    ext = "ogg"
    def play(self):
        print("playing {} as ogg".format(self.filename))

if __name__ == '__main__':
    MP3File("play.mp3").play()
    WavFile("play.wav").play()
    OggFile("play.ogg").play()
    MP3File("play.mp4").play()