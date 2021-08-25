#!/usr/bin/python3

import speech_recognition as sr
import time
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

# TODO: Package as a self-contained app
# TODO: Add a radio feed as audio input to the GUI (select mic or radio)
# TODO: Add an SDR as a possible input to the GUI


class Listener:
    def __init__(self):
        self.recogniser = sr.Recognizer()
        self.microphone = sr.Microphone()
        self._decoded_text = ""
        self._callbacks = []

    def _audio_callback(self, recogniser, audio):
        """
        Received audio data, now we'll recognize it using Google Speech Recognition
        This is called from the background listen() function
        """
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            self.decoded_text = recogniser.recognize_google(audio, language="en-GB")
            print(f"{time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)}: {self.decoded_text}")
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
            mic, callback=self._audio_callback, phrase_time_limit=10
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

    @property
    def decoded_text(self):
        return self._decoded_text

    @decoded_text.setter
    def decoded_text(self, new_text):
        """Update the private variable with the new value and notify observers"""
        old_text = self._decoded_text
        self._decoded_text = new_text
        self._notify_observers(old_text, new_text)

    def _notify_observers(self, old_text, new_text):
        """Notify any callbacks registered with the new value"""
        for callback in self._callbacks:
            callback(old_text, new_text)

    def register_callback(self, callback):
        """Register a callback to be notified when decoded_text is updated"""
        self._callbacks.append(callback)


class MainFrame(Frame):
    """The main GUI class. Inherits from a TkInter frame"""
    # keywords to trigger an alarm if detected from decoded text
    KEYWORDS = [
        "bomb",
        "kill",
        "execute",
        "murder",
        "assassinate",
        "strike",
        "purge",
    ]

    def __init__(self, master):
        """Initialise the object with a frame and GUI widgets"""
        super().__init__(master)  # inherit properties from the original Frame class
        # place the frame itself before the other objects within it
        self.pack(side="top", fill="both", expand=True)
        self.listen = Listener()    # declare the listener object
        self.listen.register_callback(self.update_text)

        # create a label
        self.label = Label(self, text="Listen")
        self.label.place(x=350, y=0)
        # start listening button
        self.start_button = Button(self, text="Start", width=30, command=self.listen.listen)
        self.start_button.place(x=0, y=450)
        self.pause_button = Button(self, text="Pause", width=30, command=self.listen.stop_listening)
        self.pause_button.place(x=250, y=450)
        # create button, link to clickExitButton
        self.exit_button = Button(self, text="Exit", width=30, command=self.exit_program)
        self.exit_button.place(x=500, y=450)
        self.output_text = "Press start to begin. Decoded text will be displayed here.\n\n"
        self.output_box = Label(
            self, width=100, height=20,
            bg='#000', fg='#fff',
            justify="left", anchor="nw",
            wraplength=750,
            text=self.output_text
        )
        self.output_box.place(x=0, y=475, width=750)

        # Load a logo and resize it to 50%
        load = Image.open("img/RAFAC.jpg")
        scale = 0.5
        load = load.resize([int(scale * s) for s in load.size])
        render = ImageTk.PhotoImage(load)
        self.img = Label(self, image=render)
        self.img.image = render
        self.img.place(x=100, y=0)

    def sound_alarm(self, word, phrase):
        """Sound the alarm when word is said in a decoded phrase"""
        messagebox.showwarning(
            "Malicious phrase detected!",
            f"Word:\n\n '{word}' \n\ndetected in phrase: \n\n'{phrase}'"
        )

    def check_for_keywords(self, phrase):
        """Check for any keywords in a phrase"""
        for keyword in self.KEYWORDS:
            if phrase is not None and keyword in phrase:
                return keyword

    def update_text(self, old_text, new_text):
        """Update the text box with a new line of text and check for keywords"""
        keyword_found = self.check_for_keywords(new_text)
        if keyword_found is not None:
            self.sound_alarm(keyword_found, new_text)
            self.output_text += f"\nMALICIOUS PHRASE -->> {new_text} <<--"
        else:
            self.output_text += f"\n{new_text}"
        self.output_box.config(text=self.output_text)

    def exit_program(self):
        """Exit the program with status 0"""
        exit()


class SpeechApp(Tk):
    """Parent class of the application"""
    def __init__(self):
        super().__init__()
        self.geometry("750x750")
        self.wm_title("2004 Speech Analyser")
        self.frame = MainFrame(self)

    def start_app(self):
        self.mainloop()


def main():
    app = SpeechApp()
    app.start_app()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
