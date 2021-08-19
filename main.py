#!/usr/bin/python3

import speech_recognition as sr
import pyttsx3
import time
from tkinter import *
from PIL import ImageTk, Image

# TODO: Add a button to start and stop listening
# TODO: Add keyword check in the loop
# TODO: Add an alarm function with text to speech
# TODO: Package as a self-contained app
# TODO: Add a radio feed as audio input to the GUI (select mic or radio)
# TODO: Add an SDR as a possible input to the GUI


class Listener:
    def __init__(self):
        self.recogniser = sr.Recognizer()
        self.microphone = sr.Microphone()

    # this is called from the background thread
    def audio_callback(self, recogniser, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = recogniser.recognize_google(audio, language="en-GB")
            print(f"{time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)}: {text}")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def listen(self):
        with self.microphone as mic:
            self.recogniser.adjust_for_ambient_noise(mic, duration=0.2)
        self.stop_listening = self.recogniser.listen_in_background(
            mic, callback=self.audio_callback, phrase_time_limit=10
        )

    def stop_listening(self):
        self.stop_listening(wait_for_stop=False)  # stop listening in the background
        time.sleep(5)  # wait a few seconds before exiting


class Window(Frame):
    def __init__(self, master=None):
        # Speech to text component
        self.listen = Listener()

        Frame.__init__(self, master)
        self.master = master
        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        # create button, link to clickExitButton
        exit_button = Button(self, text="Exit", command=self.exit_program)
        exit_button.pack(side=BOTTOM)

        # create a label
        label = Label(master, text="Listen")
        label.pack(side=TOP)

        # start listening button
        start_button = Button(self, text="Start", command=self.start_listening)
        start_button.pack(side=LEFT)
        stop_button = Button(self, text="Stop", command=self.stop_listening)
        start_button.pack(side=RIGHT)

        # Load a logo and resize it to 50%
        load = Image.open("img/RAFAC.jpg")
        scale = 0.5
        load = load.resize([int(scale * s) for s in load.size])
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.pack(side=TOP)

    def exit_program(self):
        exit()

    def start_listening(self):
        self.listen.listen()

    def stop_listening(self):
        self.listen.stop_listening()


def gui():
    root = Tk()
    app = Window(root)
    root.geometry("1200x800")
    root.wm_title("Title")
    root.mainloop()


def main():
    gui()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
