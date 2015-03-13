# from direct.showbase import DirectObject
# ********  pygame must be in the Main.py directory
# THIS FILE MUST BE IN THE MAIN.PY DIRECTORY BECAUSE SOME PATH ISSUES
print "Importing pygame"
import pygame

mappingDict = {"axes": [["arrow_left", "arrow_right"], ["arrow_down", "arrow_up"]],
               "buttons": ["z", "x"]}
# mappingDict={"axis":[axis0List[neg,pos],axis1List[neg,pos]....],
# "buttons":[button0,button1...]}
class HJoystickSensor():
    def __init__(self, joystickId=0):
        # print os.getcwd()
        print "Starting Joystick"
        pygame.init()
        pygame.joystick.init()
        c = pygame.joystick.get_count()
        self.id = 0
        if c > 0:
            self.id = joystickId
            self.joy = pygame.joystick.Joystick(self.id)
            self.joy.init()
            self.numButtons = self.joy.get_numbuttons()
            self.numAxes = self.joy.get_numaxes()
            self.eventName = "Joystick_" + str(self.id) + "_"
            self.buttonEventName = self.eventName + "button_"
            self.axisEventName = self.eventName + "axis_"
            base.taskMgr.add(self._task, "taskForJoystick_" + str(self.id))
        else:
            print "No Joystick"

    def _task(self, t):
        pygame.event.pump()
        for b in range(self.numButtons):
            if self.joy.get_button(b):
                messenger.send(self.buttonEventName + str(b))
        for a in range(self.numAxes):
            axisValue = self.joy.get_axis(a) * -1  # to make Up positive
            if axisValue != 0:
                messenger.send(self.axisEventName + str(a), sentArgs[axisValue])
        return t.cont
        # #Hats y otras cosas que no uso ahorita


class HJoyKeySensor(HJoystickSensor):
    def __init__(self, mappingDict, joystickId=0):
        HJoystickSensor.__init__(self, joystickId)
        self.eventName = "JoyKey_" + str(self.id) + "_"

        # #This event sends the value every frame
        self.buttonEventName = self.eventName + "button_"
        self.axisEventName = self.eventName + "axis_"

        # #Value has changed events
        self.axisChangeEventName = self.axisEventName + "changed_"
        self.buttonChangeEventName = self.buttonEventName + "changed_"

        # Up events
        self.axisUpEventName = self.axisEventName + "-up_"
        self.buttonUpEventName = self.buttonEventName + "-up_"

        #Down Events
        self.axisDownEventName = self.axisEventName + "-down_"
        self.buttonDownEventName = self.buttonEventName + "-down_"

        self.mapping = mappingDict
        self.buttonKeyStates = []
        self.buttonKeyStates_last = []
        self.axesKeyStates = []
        self.axesKeyStates_last = []
        self.axesLastValue = []
        self.buttonsLastValue = []

        #Buttons
        for i in range(len(self.mapping["buttons"])):
            base.accept(self.mapping["buttons"][i], self._setKey,
                        extraArgs=[i])  # #Will send to _setButton the pressed button number
            base.accept(self.mapping["buttons"][i] + "-up", self._unsetKey,
                        extraArgs=[i])  # #Will send to _setButton the unpressed button number
            self.buttonKeyStates.append(False)
            self.buttonKeyStates_last.append(False)
            self.buttonsLastValue.append(False)
            print "Event handler for ", self.mapping["buttons"][i]

        ##Axes
        for o in range(len(self.mapping["axes"])):
            self.axesKeyStates.append(list())
            self.axesKeyStates_last.append(list())
            self.axesLastValue.append(0)
            for p in range(len(self.mapping["axes"][o])):
                base.accept(self.mapping["axes"][o][p], self._setArrow, extraArgs=[o, p])
                base.accept(self.mapping["axes"][o][p] + "-up", self._unsetArrow, extraArgs=[o, p])
                self.axesKeyStates[o].append(False)
                self.axesKeyStates_last[o].append(False)
        base.taskMgr.add(self._task, "taskForJoystick_" + str(self.id))

        print "Axes state keys:", self.axesKeyStates

    def _setArrow(self, o, p):
        self.axesKeyStates_last[o][p] = self.axesKeyStates[o][p]
        self.axesKeyStates[o][p] = True
        # print "_setArrow: ",o,",",p,"\n Last:",self.axesKeyStates_last[o][p]," New:",self.axesKeyStates[o][p]
        # print "Pressed axis:",self.mapping["axes"][o][p]

    def _unsetArrow(self, o, p):
        self.axesKeyStates_last[o][p] = self.axesKeyStates[o][p]
        self.axesKeyStates[o][p] = False
        # print "_unsetArrow: ",o,",",p,"\n Last:",self.axesKeyStates_last[o][p]," New:",self.axesKeyStates[o][p]

    def _setKey(self, k):
        self.axesKeyStates_last[k] = self.axesKeyStates[k]
        self.buttonKeyStates[k] = True
        # print "Pressed key:",k

    def _unsetKey(self, k):
        self.axesKeyStates_last[k] = self.axesKeyStates[k]
        self.buttonKeyStates[k] = False
        # print "Freed key: ",k

    def _task(self, t):
        pygame.event.pump()
        for nb in range(len(self.mapping["buttons"])):
            try:
                joyButtonValue = self.joy.get_button(nb)
                messenger.send(self.buttonEventName + str(nb), sentArgs=[joyButtonValue])
                if joyButtonValue != self.buttonsLastValue[nb]:
                    messenger.send(self.buttonChangeEventName + str(nb),
                                   sentArgs=[self.buttonsLastValue[nb], joyButtonValue])
                    if joyButtonValue is True and self.buttonsLastValue[nb] is False:
                        messenger.send(self.buttonDownEventName + str(nb))
                    elif joyButtonValue is False and self.buttonsLastValue[nb] is True:
                        messenger.send(self.buttonUpEventName + str(nb))
                self.buttonsLastValue[nb] = joyButtonValue
            except:
                buttonValue = self.buttonKeyStates[nb]
                messenger.send(self.buttonEventName + str(nb), sentArgs=[buttonValue])
                # print self.mapping["buttons"][nb], "- pressed"
                if buttonValue != self.buttonsLastValue[nb]:
                    messenger.send(self.buttonChangeEventName + str(nb),
                                   sentArgs=[self.buttonsLastValue[nb], buttonValue])
                    if buttonValue is True and self.buttonsLastValue[nb] is False:
                        messenger.send(self.buttonDownEventName + str(nb))
                    elif buttonValue is False and self.buttonsLastValue[nb] is True:
                        messenger.send(self.buttonUpEventName + str(nb))
                        # print "Button: ",nb,"-up"
                self.buttonsLastValue[nb] = buttonValue
        for na in range(len(self.mapping["axes"])):
            try:
                axisValue = self.joy.get_axis(na) * -1
                messenger.send(self.axisEventName + str(na), sentArgs=[axisValue])
                if axisValue != self.axesLastValue[na]:
                    messenger.send(self.axisChangeEventName + str(na),
                                   sentArgs=[self.axesLastValue[na], axisValue])  # [last,new]
                    if abs(self.axesLastValue[na]) > 0 and axisValue == 0:
                        messenger.send(self.axisUpEventName + str(na))
                    elif self.axesLastValue[na] == 0 and abs(axisValue) > 0:
                        messenger.send(self.axisDownEventName + str(na), sentArgs=[axisValue])
                self.axesLastValue[na] = axisValue

            except:
                if self.axesKeyStates[na][0]:
                    value = -1
                elif self.axesKeyStates[na][1]:
                    value = 1
                else:
                    value = 0
                messenger.send(self.axisEventName + str(na), sentArgs=[value])
                if value != self.axesLastValue[na]:
                    messenger.send(self.axisChangeEventName + str(na),
                                   sentArgs=[self.axesLastValue[na], value])  # [last,new]
                    # print "Changed:",self.axesLastValue[na],",",value
                    if abs(self.axesLastValue[na]) > 0 and value == 0:
                        messenger.send(self.axisUpEventName + str(na))
                        # print "Axis:", na, " -up"
                    elif self.axesLastValue[na] == 0 and abs(value) > 0:
                        messenger.send(self.axisDownEventName + str(na), sentArgs=[value])
                self.axesLastValue[na] = value
        return t.cont
        ##Agregar un Enet Handler para cada evento enviado y ahi ver el UP y DOWN