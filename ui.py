import PySimpleGUI as sg
import speech_recognition as sr

r = sr.Recognizer()


sg.theme('SandyBeach')
layout = [[sg.Text("Browse for the .wav file")],
          [sg.Input(), sg.FileBrowse()],
          [sg.Text("What word are you looking for?")],
          [sg.Input(key='-IN-')],
          [sg.Button("Search")], [sg.Button("Exit")]]
window = sg.Window(title="Audio Searcher", layout=layout)

while True:
    event, values = window.read()
    values_list = list(values.values())

    try:
        destination = values_list[0]
        file = sr.AudioFile(destination)
        with file as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)

        transcription = r.recognize_google(audio)
    except ValueError:
        error_layout = [[sg.Text("File type not supported")]]
        error_window = sg.Window(
            title='Error', layout=error_layout, size=(300, 50)).read()
        break

    if (event == 'Search'):

        if(transcription.find(values_list[2]) != -1):
            suc_layout = [[sg.Text("Found the word:")],
                          [sg.Text(transcription[transcription.find(values_list[2]):])]]
            suc_window = sg.Window(
                title="Audio Searcher Success", layout=suc_layout).read()

        else:
            fail_layout = [
                [sg.Text("Oops, I cannot find the word you asked for!")]]
            fail_window = sg.Window(
                title="Audio Searcher Fail", layout=fail_layout).read()

    elif (event == sg.WINDOW_CLOSED or event == 'Exit'):
        break

window.close()
