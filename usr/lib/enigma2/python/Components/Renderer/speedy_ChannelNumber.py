# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/ChannelNumber.py
from Components.VariableText import VariableText
from enigma import eLabel, iPlayableService
from Components.Renderer.Renderer import Renderer

class speedy_ChannelNumber(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.text = '---'

    GUI_WIDGET = eLabel

    def changed(self, what):
        if what == True or what[0] == self.CHANGED_SPECIFIC and what[1] == iPlayableService.evStart:
            service = self.source.serviceref
            num = service and service.getChannelNum() or None
            if num:
                self.text = str(num)
            else:
                self.text = '---'
        return
