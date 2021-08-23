#!/usr/bin/python3

import speech_recognition as sr
import time
from tkinter import *
from PIL import ImageTk, Image

# TODO: Add keyword check in the loop
# TODO: Add an alarm function with text to speech
# TODO: Package as a self-contained app
# TODO: Add a radio feed as audio input to the GUI (select mic or radio)
# TODO: Add an SDR as a possible input to the GUI


class Listener:
    def __init__(self):
        self.recogniser = sr.Recognizer()
        self.microphone = sr.Microphone()

    def audio_callback(self, recogniser, audio):
        """
        Received audio data, now we'll recognize it using Google Speech Recognition
        This is called from the background listen() function
        """
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
        """Begin listening and performing speech to text"""
        # open up the mic and adjust for the ambient noise
        with self.microphone as mic:
            self.recogniser.adjust_for_ambient_noise(mic, duration=0.2)
        # start listening and create a method to stop listening at the same time
        self.stop_listening = self.recogniser.listen_in_background(
            mic, callback=self.audio_callback, phrase_time_limit=10
        )

    def stop_listening(self):
        """Stop listening and wait until the process exits"""
        try:
            print("Stopping")
            self.stop_listening(wait_for_stop=False)  # stop listening in the background
            time.sleep(5)  # wait a few seconds before exiting
            print("Stopped listening")
        except TypeError:
            print("Not currently listening")


class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)  # inherit properties from the original Frame class
        self.listen = Listener()
        # place the frame itself before the other objects within it
        self.pack(side="top", fill="both", expand=True)

        # create a label
        self.label = Label(self, text="Listen")
        self.label.place(x=350, y=0)
        # start listening button
        self.start_button = Button(self, text="Start", width=30, command=self.start_listening)
        self.start_button.place(x=0, y=450)
        self.stop_button = Button(self, text="Stop", width=30, command=self.stop_listening)
        self.stop_button.place(x=250, y=450)
        # create button, link to clickExitButton
        self.exit_button = Button(self, text="Exit", width=30, command=self.exit_program)
        self.exit_button.place(x=500, y=450)
        self.textbox = Text(self)
        self.textbox.place(x=0, y=475, width=750)

        # Load a logo and resize it to 50%
        load = Image.open("img/RAFAC.jpg")
        scale = 0.5
        load = load.resize([int(scale * s) for s in load.size])
        render = ImageTk.PhotoImage(load)
        self.img = Label(self, image=render)
        self.img.image = render
        self.img.place(x=100, y=0)

        self.pack()

    def exit_program(self):
        exit()

    def start_listening(self):
        self.listen.listen()

    def stop_listening(self):
        self.listen.stop_listening()


class SpeechApp(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("750x750")
        self.wm_title("2004 Speech Analyser")


def main():
    app = SpeechApp()
    frame = MainFrame(app)
    app.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
