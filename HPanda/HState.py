# ###State Library

def emptyMethod():
    return None


class NoExistingState(Exception):
    def __init__(self, state):
        """

        :type state:str
        """
        self.message = "The *" + state + "* does not exists"


class DuplicatedState(Exception):
    def __init__(self, state):
        """

        :type state: str
        """
        self.message = "The *" + state + "* already exits in this manager"


class HState:
    def __init__(self, name, onInit, onFrame, onExit, enterCondition=None):
        """

        :type name:str
        :type onInit: func
        :type onFrame:  func
        :type onExit: func
        :type enterCondition: func
        """
        self.name = name
        self.onInit = onInit
        self.onFrame = onFrame
        self.onExit = onExit
        if enterCondition is None:
            self.enterCondition = self.alwaysTrue()
        else:
            self.enterCondition = enterCondition


    def alwaysTrue(self):
        return True


class EmptyState(HState):
    def __init__(self):
        HState.__init__(self, "EmptyState", emptyMethod, emptyMethod, emptyMethod)


class HStateManager:
    def __init__(self, Base, name):
        """
        :type self.lastState: str
        :type self.currentState: str
        :type self.states: dict{str:HState}
        :type self.name: str
        :type Base: direct.showbase.ShowBase.ShowBase
        :type name: str
        """
        self.Base = Base
        self.name = name
        self.currentState = "None"
        self.lastState = "None"
        self.states = {"None": EmptyState()}
        self.Base.taskMgr.add(self.tick, "HStateManager-" + self.name)


    def addState(self, state):
        """

        :type state: HState
        :raise DuplicatedState:
        """
        if state.name in self.states.keys():
            raise DuplicatedState(state.name)
        else:
            self.states[state.name] = state

    def setState(self, newState):
        """

        :param newState: str
        :type newState: str, new state name
        """
        r = False
        if newState in self.states.keys():
            if self.states[newState].enterCondition():
                r = True
                self.lastState = self.currentState
                self.currentState = newState
                if self.lastState != "None":
                    self.states[self.lastState].onExit()
                self.states[self.currentState].onInit()
            else:
                # print "Can't change to ", newState, "because state.enterCondition is FALSE"
                r = False
        else:
            raise NoExistingState(newState)
        return r

    def forceState(self, newState):
        r = False
        if newState in self.states.keys():
            self.lastState = self.currentState
            self.currentState = newState
            self.states[self.lastState].onExit()
            self.states[self.currentState].onInit()
        r = True
        return r

    def __call__(self, newState):
        return self.setState(newState)


    def tick(self, task):
        for s in self.states:
            if s == "None":
                continue
            else:
                if s == self.currentState:
                    self.states[s].onFrame()
        return task.cont