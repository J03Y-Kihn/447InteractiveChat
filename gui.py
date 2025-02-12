import PySimpleGUI as sg
import TwitchPlays_InteractiveChat as twitchPlays
import InputManager
import threading

mappings = {}
Twitch_Channel = ""
Youtube_Channel = ""

savedFile = False
defaultFilename = "key-pairs.ini"

large_font = ("Consolas Bold", 21)

sg.theme('DarkGrey13')

"""MAXIMIZE SCREEN"""
MAXIMIZE_SCREEN = True

layout = [
    [sg.Image('interactive_chat_banner_black.png')],
    [sg.Button("Map Buttons to Phrases", key= 'map')],
    [sg.Button("Map Scripts to Phrases", key= 'Script')],
    [sg.Text("Load Buttons From File"), sg.Input(key="IN-"), sg.FileBrowse()],
    [sg.Button("Load From File", key="Load-")],
    [sg.Button("See Current Mappings", key="View")],
    [sg.Button("Save Key-Pairs to File", key="Save")],
    [sg.Button("Start Program", key= "Start-"), sg.Exit()],
]

if MAXIMIZE_SCREEN:
  window = sg.Window("Interactive Chat", layout, font=large_font, finalize=True)
  window.maximize()
else:
  window = sg.Window("Interactive Chat", layout, font=large_font)



#Opens a new window in order to add new phrase-key pairings to the dictionary
def MapWindow():
  layout2 = [
    [sg.Text("Add Key or Keys")],
    [sg.Input(key="HKey-"), sg.Text("As a held key")],
    [sg.Input(key="RKey-"), sg.Text("As a released key")],
    [sg.Input(key="HRKey-"), sg.Text("As a held and released key")],
    [sg.Text("With Phrase"), sg.Input(key="Phrase-")],
    [sg.Button("Add", key= "ADD"), sg.Button("Remove", key= "REMOVE")],
    [sg.Exit()],
  ]
  if MAXIMIZE_SCREEN:
    newWindow = sg.Window("Mapping", layout2, font=large_font, finalize=True)
    newWindow.maximize()
  else:
    newWindow = sg.Window("Mapping", layout2, font=large_font)


  while True:
    event, values = newWindow.read()

    #exit the window
    if event in (sg.WINDOW_CLOSED, "Exit"):
      break

    #add a new key-phrase pair
    if event == "ADD" and values["Phrase-"] != "":

      #new key-phrase contains a Hold
      if values["HKey-"] != "":
        for indices in values["HKey-"]:
            InputManager.addCommand(mappings, values["Phrase-"].lower(), "H", indices.upper())

      #new key-phrase contains a Release
      if values["RKey-"] != "":
        for indices in values["RKey-"]:
          InputManager.addCommand(mappings, values["Phrase-"].lower(), "R", indices.upper())
      
      #new key-phrase contains a Hold and Release
      if values["HRKey-"] != "":
        for indices in values["HRKey-"]:
          InputManager.addCommand(mappings, values["Phrase-"].lower(), "HR", indices.upper())


    #Removing a key from a pair or removing a pair
    if event == "REMOVE" and values["Phrase-"] != "":
      removedKey = False

      if values["HKey-"] != "":
        for indices in values["HKey-"]:
            InputManager.removeCommand(mappings, values["Phrase-"].lower(), "H", indices.upper())
        removedKey = True    

      #new key-phrase contains a Release
      if values["RKey-"] != "":
        for indices in values["RKey-"]:
          InputManager.removeCommand(mappings, values["Phrase-"].lower(), "R", indices.upper())
        removedKey = True
      
      #new key-phrase contains a Hold and Release
      if values["HRKey-"] != "":
        for indices in values["HRKey-"]:
          InputManager.removeCommand(mappings, values["Phrase-"].lower(), "HR", indices.upper())
        removedKey = True

      if(not removedKey):
        InputManager.removeCommand(mappings, values["Phrase-"].lower(), "HR", None)

  newWindow.close()

def ScriptWindow():
  layout2 = [
    [sg.Text("Add Scripts to phrase")],
    [sg.Text("Load Script From File"), sg.Input(key="IN-"), sg.FileBrowse()],
    [sg.Text("With Phrase"), sg.Input(key="Phrase-")],
    [sg.Button("Add", key= "ADD"), sg.Button("Remove", key= "REMOVE")],
    [sg.Exit()],
  ]
  if MAXIMIZE_SCREEN:
    newWindow = sg.Window("Script Mapping", layout2, font=large_font, finalize=True)
    newWindow.maximize()
  else:
    newWindow = sg.Window("Mapping", layout2, font=large_font)


  while True:
    event, values = newWindow.read()

    #exit the window
    if event in (sg.WINDOW_CLOSED, "Exit"):
      break

    #add a new script-phrase pair
    if event == "ADD" and values["IN-"] != "":
      sg.popup("Not implemented!")
      #InputManager.addCommand(mappings, values["Phrase-"].lower(), "S", values["IN-"])

    #Removing a script from a pair or removing a pair
    if event == "REMOVE" and values["IN-"] != "":
      sg.popup("Not implemented!")
      """
      removedKey = False

      if values["IN-"] != "":
        InputManager.removeCommand(mappings, values["Phrase-"].lower(), "H", values["IN-"])
        removedKey = True    

      if(not removedKey):
        InputManager.removeCommand(mappings, values["Phrase-"].lower(), "HR", None)
      """

  newWindow.close()


#call python program to start listening to the designated channel's chat
#loads a new window to interact with the user
def startWatching():
  chatLayout = [
    [sg.Text("Enter a channel name then select the Type of Channel")],
    [sg.Text("Twitch/YouTube Channel Name"), sg.Input(key="Channel_Name")],
    [sg.Text("YouTube Channel Live URL"), sg.Input(key="URL")],
    [sg.Text("Channel Type:")],
    [sg.Button("Twitch", key="Twitch"), sg.Button("YouTube", key="YouTube"), sg.Button("Both", key="Twitch and Youtube")],
    [sg.Exit()]
  ]

  if MAXIMIZE_SCREEN:
    newWindow = sg.Window("Chat name", chatLayout, font=large_font, finalize=True)
    newWindow.maximize()
  else:
    newWindow = sg.Window("Chat name", chatLayout, font=large_font)

  while True:
    event, values = newWindow.read()

    #Exiting window
    if event in (sg.WINDOW_CLOSED, "Exit"):
      break

    # user chose to stream on twitch
    if event == "Twitch" and values["Channel_Name"] != "":
      newWindow.close()
      twitchPlays.TwitchPlaysStart(mappings, values["Channel_Name"])

    # user chose to stream on youtube
    if event == "YouTube" and values["Channel_Name"] != "":
      newWindow.close()
      twitchPlays.TwitchPlaysStart(mappings, "", False, values["Channel_Name"], values["URL"])


    # user chose to stream on twitch and youtube
    if event == "Twitch and Youtube" and values["Channel_Name"] != "":
      #fork then call both youtube and twitch chats?
      t1 = threading.Thread(target=twitchPlays.TwitchPlaysStart, args=(mappings, values["Channel_Name"],))
      
      newWindow.close()
      t1.start()

      if(t1):
        twitchPlays.TwitchPlaysStart(mappings, "", False, values["Channel_Name"], values["URL"])

      t1.join()


  newWindow.close()


#after inputting a name for the file, calls InputManager.writeFile with the input filename + ".ini"
def saveFile():
  save_layout = [
    [sg.Text("Filename"), sg.Input(key="Filename-")],
    [sg.Button("Save", key= "SAVE")],
    [sg.Exit()],
  ]
  if MAXIMIZE_SCREEN:
    newWindow = sg.Window("Save File", save_layout, font=large_font, finalize=True)
    newWindow.maximize()
  else:
    newWindow = sg.Window("Save File", save_layout, font=large_font)

  while True:
    event, values = newWindow.read()

    #exit the window
    if event in (sg.WINDOW_CLOSED, "Exit"):
      break

    #add a new key-phrase pair
    if event == "SAVE" and values["Filename-"] != "":      
      filenametxt = values["Filename-"] + ".ini"
      InputManager.writeFile(filenametxt, mappings)
      savedFile = True
      break

  newWindow.close()

if __name__=="__main__": 
  while True:
    event, values = window.read()

    #Exiting program
    if event in (sg.WINDOW_CLOSED, "Exit"):
      break
    
    # user chose the map buttons to phrases
    if event == 'map':
      MapWindow()

    # user chose to map scripts to phrases
    if event == 'Script':
      ScriptWindow()
    
    # user chose to get keybinds from a saved file
    if values["IN-"] != "" and event == "Load-":
      mappings = InputManager.readFile(values["IN-"])

    # user chose to view all current key-phrase mappings
    if event == "View":
      currstr = ""
      for inputName, inputCommand in mappings.items():
        currstr += str(inputName) + " " + str(inputCommand) + "\n"
      if currstr == "":
        sg.popup("No key-pairings made")
      else:
        sg.popup(currstr)
    
    # user chose to begin the chat process
    if event == "Start-" and mappings != {}:
      window.close()
      if not savedFile:
        InputManager.writeFile(defaultFilename, mappings)
      startWatching()
    else:
      if event == "Start-" and mappings == {}:
        sg.popup("Must have key-pairs before running the program")
      
    if event == "Save" and mappings != {}:
      saveFile()
    else:
      if event == "Save" and mappings == {}:
        sg.popup("Must have key-pairs before saving them as a file")

window.close()