# -*- coding: utf-8 -*-
"""
************************************************************************************
programme : CalcAlGUIMenu
Auteur : Thierry Maillard (TMD)
Date : 12/3/2016 - 11/10/2016

Role : Menu bar for CalcAl Food Calculator project.

Licence : GPLv3
Copyright (c) 2016 - Thierry Maillard


This file is part of CalcAl project.

CalcAl project is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CalcAl project is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CalcAl project.  If not, see <http://www.gnu.org/licenses/>.
************************************************************************************
"""
import logging
import os.path
import shutil

from tkinter import *
from tkinter import filedialog

class CalcAlGUIMenu(Menu):
    """ Menu definition class """

    def __init__(self, master):
        """ Constructor : Define menu bar GUIs widgets """
        Menu.__init__(self, master)
        self.master = master
        self.configApp = self.master.getConfigApp()
        self.logger = logging.getLogger(self.configApp.get('Log', 'LoggerName'))

        self.databaseMenu = Menu(self, tearoff=0)
        self.databaseMenu.add_command(label=_("New"),
                                      command=self.master.getStartFrame().newDB)
        self.databaseMenu.add_command(label=_("Info"),
                                      state=DISABLED,
                                      command=self.master.getStartFrame().infoDB)
        self.databaseMenu.add_command(label=_("Delete"),
                                      state=DISABLED,
                                      command=self.master.getStartFrame().deleteDB)
        self.databaseMenu.add_command(label=_("Join"),
                                      command=self.master.getStartFrame().joinDB)
        self.add_cascade(label=_("Database"), menu=self.databaseMenu)


        self.selectionMenu = Menu(self, tearoff=0)
        self.selectionMenu.add_command(label=_("Modify"),
                                       state=DISABLED,
                                       command=self.master.getCalculatorFrame().copySelectionInDefinitionFrame)
        self.selectionMenu.add_command(label=_("Group"),
                                       state=DISABLED,
                                       command=self.master.getCalculatorFrame().groupFood)
        self.selectionMenu.add_command(label=_("Ungroup"),
                                       state=DISABLED,
                                       command=self.master.getCalculatorFrame().UngroupFood)
        self.selectionMenu.add_command(label=_("Erase line"),
                                       state=DISABLED,
                                       command=self.master.getCalculatorFrame().eraseFood)
        self.selectionMenu.add_command(label=_("Delete in database"),
                                       state=DISABLED,
                                       command=self.master.getCalculatorFrame().deleteFood)
        self.selectionMenu.add_command(label=_("Clipboard"),
                                       state=DISABLED,
                                       command=self.master.getCalculatorFrame().copyInClipboard)
        self.selectionMenu.add_command(label=_("Info"),
                                       state=DISABLED,
        command=self.master.getCalculatorFrame().infoFood)
        self.selectionMenu.add_command(label=_("Save portion"),
                                       state=DISABLED,
        command=self.master.getCalculatorFrame().savePortion)
        self.add_cascade(label=_("Selection"), menu=self.selectionMenu)

        self.pluginsMenu = Menu(self, tearoff=0)
        listPlugins = ["Ciqual_2013_Reader", "USDA_28_Reader"]
        for plugin in listPlugins:
            self.pluginsMenu.add_command(label=plugin,
                                         command=lambda plug=plugin:self.installReader(plug+".py"))
        self.add_cascade(label=_("Plugins"), menu=self.pluginsMenu)

        otherMenu = Menu(self, tearoff=0)
        otherMenu.add_command(label=_("About"), command=self.master.about)
        self.isLoglevelDebug = BooleanVar()
        self.isLoglevelDebug.set(False)
        # Observer self.setLogLevel on self.isLoglevelDebug called if modified : 'w'
        self.isLoglevelDebug.trace_variable('w', self.setLogLevel)
        otherMenu.add_checkbutton(label='Debug log', variable=self.isLoglevelDebug,
                                  onvalue=True, offvalue=False)
        self.add_cascade(label="?", menu=otherMenu)

    def setLogLevel(self, *args):
        """ Set logging level """

        # Get handler to write on console
        streamHandler = self.logger.handlers[1]

        if self.isLoglevelDebug.get():
            self.logger.setLevel(logging.DEBUG)
            streamHandler.setLevel(logging.DEBUG)
            self.logger.info(_("Debug logging mode : all messages in file and on console."))
        else:
            self.logger.setLevel(logging.INFO)
            streamHandler.setLevel(logging.WARNING)
            self.logger.info(_("Logging in file with mode INFO and on console in mode WARNING."))

    def enableDatabaseMenu(self, isEnabled):
        """ Autorise ou non les options de configuration du menu Fichier """
        if isEnabled:
            etat = NORMAL
        else:
            etat = DISABLED
        last = self.databaseMenu.index("end")
        for itemMenu in range(last+1):
            self.databaseMenu.entryconfigure(itemMenu, state=etat)

    def enableSelectionMenu(self, isEnabled):
        """ Autorise ou non les options de configuration du menu Fichier """
        if isEnabled:
            etat = NORMAL
        else:
            etat = DISABLED
        last = self.selectionMenu.index("end")
        for itemMenu in range(last+1):
            self.selectionMenu.entryconfigure(itemMenu, state=etat)

    def installReader(self, pluginName):
        """ Install a plugin whose name is given in parameter """
        try:
            pluginPath = os.path.join(self.master.getDirProject(),
                                      self.configApp.get("Resources", "ReadersDir"),
                                      pluginName)
            if os.path.isfile(pluginPath):
                raise ValueError(_("Plugin") + " " + pluginName + " " +
                                 _("has already been installed"))
            filename = filedialog.askopenfilename(filetypes=(("Py File", "*.py"),
                                                             ("All Files","*.*")),
                                                  title = _("Choose a file"))
            if not filename:
                raise ValueError(_("Installation canceled"))
            shutil.copy2(filename, pluginPath)
            self.master.setStatusText(_("Plugin") + " " + pluginName + " " + _("installed"))
            self.logger.info(_("Plugin") + " " + pluginName + " " + _("installed"))
        except ValueError as exc:
            self.master.setStatusText(_("Error") + " : " + str(exc) + " !", True)

