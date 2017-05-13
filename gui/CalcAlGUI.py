#! /usr/bin/env python
# -*- coding: ISO-8859-1 -*-
"""
*********************************************************
Class : CalcAlGUI
Auteur : Thierry Maillard (TM)
Date : 7/5/2016 - 28/9/2016

Role : GUI for CalcAl Food Calculator project.

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
*********************************************************
"""
import logging
import os.path
import platform

from tkinter import *
from tkinter import ttk
from tkinter import font

from . import CalcAlGUIMenu
from . import StartFrame
from . import CalculatorFrame
from . import SearchFoodFrame
from . import PortionFrame

from model import CalculatorFrameModel


class CalcAlGUI(Tk):
    """ Main GUI class """

    def __init__(self, configApp, dirProject, databaseManager):
        """
        Constructor : Define all GUIs widgets
        parameters :
        - configApp : configuration properties read by ConfigParser
        - dirProject : local directory of th project to access resources
        """
        Tk.__init__(self, None)
        self.configApp = configApp
        self.dirProject = dirProject
        self.databaseManager = databaseManager

        ressourcePath = os.path.join(dirProject, self.configApp.get('Resources', 'ResourcesDir'))
        self.logger = logging.getLogger(self.configApp.get('Log', 'LoggerName'))
        self.logger.info(_("Starting GUI") + "...")

        # Adapt to screen size
        heightBigScreenInPixel = int(self.configApp.get('Limits', 'heightBigScreenInPixel'))
        screenheight = self.winfo_screenheight()
        self.bigScreen = (screenheight > heightBigScreenInPixel)
        self.logger.debug("heightBigScreenInPixel=" + str(heightBigScreenInPixel) +
                         ", screenheight=" + str(screenheight) +
                         ", bigScreen=" + str(self.bigScreen))

        # Set handler called when closing main window
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

        # Set application title
        self.setTitle()

        # Central panels notebook
        self.note = ttk.Notebook(self)
        self.currentTab = None
        self.note.bind_all("<<NotebookTabChanged>>", self.tabChangedEvent)

        # Create model for calculator Frame
        self.calculatorFrameModel = CalculatorFrameModel.CalculatorFrameModel(configApp)

        # Create panels contents
        self.startFrame = StartFrame.StartFrame(self.note, self, 'logoStartFrame',
                                                self.calculatorFrameModel)
        self.note.add(self.startFrame, text = _("Welcome"))
        self.calculatorFrame = CalculatorFrame.CalculatorFrame(self.note, self, 'logoCalculator',
                                                               self.calculatorFrameModel)
        self.note.add(self.calculatorFrame, text = _("Calculator"), state="disabled")

        self.searchFoodFrame = SearchFoodFrame.SearchFoodFrame(self.note, self, 'logoSearchFood')
        self.note.add(self.searchFoodFrame, text = _("Search"), state="disabled")
        self.note.pack(side=TOP)

        self.portionFrame = PortionFrame.PortionFrame(self.note, self, 'logoPortion',
                                                      self.calculatorFrameModel)
        self.note.add(self.portionFrame, text = _("Portions"), state="disabled")
        self.note.pack(side=TOP)

        # Add menu bar
        self.menuCalcAl = CalcAlGUIMenu.CalcAlGUIMenu(self, self.calculatorFrameModel)
        self.config(menu=self.menuCalcAl)

        # Create Status frame at the bottom of the sceen
        statusFrame = Frame(self)
        self.statusLabel = Label(statusFrame, text=_('Ready'))
        self.statusLabel.pack(side=LEFT)
        self.statusLabel.pack(side=TOP)
        statusFrame.pack(side=TOP)

    def getStartFrame(self):
        """Return start frame"""
        return self.startFrame

    def getCalculatorFrame(self):
        """Return calculator frame"""
        return self.calculatorFrame

    def setStatusText(self, text, isError=False):
        """ Display a text in status bar and log it """
        self.statusLabel['text'] = text
        if (isError):
            self.bell()
            self.logger.error(text)
        else:
            self.logger.info(text)

    def onClosing(self):
        """ Handler called at the end of main window """
        stopAppli = True
        self.closeDatabase()
        self.destroy()

    def setTitle(self, dbName=None):
        """ Set title bar. """
        title = self.configApp.get('Version', 'AppName') + ' - Version ' + \
        self.configApp.get('Version', 'Number') + ' - ' + \
        self.configApp.get('Version', 'Date')
        if dbName:
            title = title + ' - ' + dbName
        self.title(title)

    def getConfigApp(self):
        """ Return configuration resources of the project """
        return self.configApp

    def getDirProject(self):
        """ Return project main installation directory """
        return self.dirProject

    def getDataBaseManager(self):
        """ Return database manager of the project """
        return self.databaseManager

    def tabChangedEvent(self, event):
        """ Callback called when user changes tab """
        newTab = event.widget.tab(event.widget.index("current"), "text")
        if newTab != self.currentTab:
            self.currentTab = newTab
            self.logger.info(_("Tab") + " " + self.currentTab + " " + _("selected") + ".")
            self.menuCalcAl.enableDatabaseMenu(event.widget.index("current") == 0)
            self.menuCalcAl.enableSelectionMenu(event.widget.index("current") == 1)

    def closeDatabase(self):
        """ Close database """
        self.databaseManager.closeDatabase()
        self.enableTabCalculator(False)
        self.enableTabSearch(False)
        self.enableTabPortion(False)
        self.setTitle(None)

    def enableTabCalculator(self, isEnable, init=True):
        """ Activate or desactivate calculator tab """
        if isEnable:
            stateTab = 'normal'
            self.menuCalcAl.enableDatabaseMenu(False)
        else:
            stateTab='disabled'
        self.note.tab(1, state=stateTab)
        self.menuCalcAl.enableSelectionMenu(isEnable)
        if isEnable:
            self.note.select(1)

    def enableTabSearch(self, isEnable=True):
        """ Activate or desactivate search tab """
        if isEnable:
            stateTab = 'normal'
        else:
            stateTab='disabled'
        self.note.tab(2, state=stateTab)
        if isEnable:
            self.searchFoodFrame.init()
            self.note.select(2)

    def enableTabPortion(self, isEnable=True):
        """ Activate or desactivate portion tab """
        if isEnable:
            stateTab = 'normal'
        else:
            stateTab='disabled'
        self.note.tab(3, state=stateTab)
        if isEnable:
            self.note.select(3)

    def isBigScreen(self):
        return self.bigScreen

    def about(self):
        """ Display about box """
        window = Toplevel(self.master)

        appName = self.configApp.get('Version', 'AppName')
        helv36 = font.Font(family="Helvetica", size=36, weight="bold")
        Label(window, text=appName, font=helv36, fg="red").pack(side=TOP)

        version = _("Version") + " : " + self.configApp.get('Version', 'Number') + ' - ' + \
        self.configApp.get('Version', 'Date')
        Label(window, text=version).pack(side=TOP)

        labelLogo = self.createButtonImage(window,
                                           imageRessourceName='logoAboutBox',
                                           text4Image=self.configApp.get('Version', 'Author'))
        labelLogo.pack(side=TOP)

        emails = self.configApp.get('Version', 'EmailSupport1')  + ", " +\
                 self.configApp.get('Version', 'EmailSupport2')
        Label(window, text=emails).pack(side=TOP)
        Label(window, text=_(self.configApp.get('Ciqual', 'CiqualNote'))).pack(side=TOP)

        versionPython = "Python : " + platform.python_version() + ", Tk : " + str(TkVersion)
        Label(window, text=versionPython).pack(side=TOP)
        osMachine = _("On") + " : " + platform.system() + ", " + platform.release()
        Label(window, text=osMachine).pack(side=TOP)

    def createButtonImage(self, parent, imageRessourceName=None, text4Image=None):
        """ Create a button or label with an image and a text dipayed """
        compoundValue = 'image'
        if text4Image:
            compoundValue = 'top'
        ressourcePath = os.path.join(self.dirProject,
                                     self.configApp.get('Resources', 'ResourcesDir'))
        imagesDirPath = os.path.join(ressourcePath, self.configApp.get('Resources', 'ImagesDir'))
        imagePath = os.path.join(imagesDirPath, self.configApp.get('Resources', imageRessourceName))
        imgobj = PhotoImage(file=imagePath)
        buttonImage = ttk.Button(parent, image=imgobj, compound=compoundValue, text=text4Image)
        buttonImage.img = imgobj # store a reference to the image as an attribute of the widget
        return buttonImage

    def copyInClipboard(self, text):
        """Copy text in clipboard"""
        self.clipboard_clear()
        self.clipboard_append(text)
        self.setStatusText(str(len(text)) + " " + _("characters copied and available in clipboard"))

