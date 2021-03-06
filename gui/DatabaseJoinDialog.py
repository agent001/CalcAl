# -*- coding: utf-8 -*-
"""
************************************************************************************
Name : DatabaseJoinDialog
Role : Window used to join two Databases
Date  : 26/8/2016 - 18/12/2016

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
import tkinter
from tkinter import messagebox
from tkinter.ttk import Combobox

from . import TkSimpleDialog

class DatabaseJoinDialog(TkSimpleDialog.TkSimpleDialog):
    """ Dialog box to choose a food name and family """
    def __init__(self, parent, configApp, databaseManager, dbNameMaster, title=None):
        self.configApp = configApp
        self.databaseManager = databaseManager
        self.dbNameMaster = dbNameMaster
        self.dbName = ""
        self.delaymsTooltips = int(self.configApp.get('Limits', 'delaymsTooltips'))
        super(DatabaseJoinDialog, self).__init__(parent, title)
        self.dbNameResult = ""
        self.isUpdate = False

    def body(self, master):
        """ Body content of this dialog """
        tkinter.Label(master,
                      text=_("Please choose secondary database") + " :").pack(side=tkinter.TOP)
        listOtherDatabase = [databaseName
                             for databaseName in self.databaseManager.getListDatabaseInDir()
                             if databaseName != self.dbNameMaster]
        self.secondaryDatabaseCombobox = Combobox(master, exportselection=0,
                                                  state="readonly", values=listOtherDatabase)
        self.secondaryDatabaseCombobox.current(0)
        self.secondaryDatabaseCombobox.pack(side=tkinter.TOP)

        tkinter.Label(master, text=_("Enter a result database name") + " :").pack(side=tkinter.TOP)
        self.dbNameResultVar = tkinter.StringVar()
        dbNameEntry = tkinter.Entry(master, textvariable=self.dbNameResultVar)
        dbNameEntry.pack(side=tkinter.TOP)

        # V0.45 : Add or update radio buttons frame
        operationTypeFrame = tkinter.Frame(master)
        operationTypeFrame.pack(side=tkinter.TOP)
        self.operationTypeVar = tkinter.StringVar()
        tkinter.Radiobutton(operationTypeFrame, text=_("Add only"),
                            variable=self.operationTypeVar,
                            value="Add").pack(side=tkinter.LEFT)
        tkinter.Radiobutton(operationTypeFrame, text=_("Update and add"),
                            variable=self.operationTypeVar,
                            value="Update").pack(side=tkinter.LEFT)
        self.operationTypeVar.set("Add")
        dbNameEntry.focus_set()

        return dbNameEntry # initial focus

    def validate(self):
        """ Check Data entered by user
            if OK return True
        """
        isOK = False
        try:
            self.dbNameResult = self.dbNameResultVar.get().lower().strip()
            if self.dbNameResult == "":
                raise ValueError(_("Please give a name for your new database"))
            if not self.dbNameResult.isalnum():
                raise ValueError(_("Invalid database name"))
            # Check if database exists
            if self.databaseManager.existsDatabase(self.dbNameResult):
                raise ValueError(_("this database already exists") + " : " + self.dbNameResult)
            self.isUpdate = self.operationTypeVar.get() == "Update"
            isOK = True
        except ValueError as exc:
            self.bell()
            messagebox.showwarning(_("Bad input"), message=_("Error") + " : " + str(exc) + " !")
        return isOK

    def apply(self):
        self.setResult([self.secondaryDatabaseCombobox.get(), self.dbNameResult, self.isUpdate])
