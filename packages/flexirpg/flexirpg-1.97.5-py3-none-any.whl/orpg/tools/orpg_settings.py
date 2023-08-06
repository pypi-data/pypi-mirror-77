# Copyright (C) 2000-2001 The OpenRPG Project
#
#   openrpg-dev@lists.sourceforge.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# --
#
# File: orpg_settings.py
# Author: Dj Gilcrease
# Maintainer:
# Version:
#   $Id: orpg_settings.py,v 1.51 2007/07/15 14:25:12 digitalxero Exp $
#
# Description: classes for orpg settings
#

from orpg.orpg_windows import *
import orpg.dirpath
from orpg.orpg_version import PRODUCT
from orpg.tools.rgbhex import *
import sys
import os

class setting_string(object):
    def __init__(self, xml_dom):
        self.xml_dom = xml_dom
        self._value = self.xml_dom.getAttribute('value')

    def __get_string(self):
        return self._value

    def __set_string(self, s):
        self._value = s
        self.xml_dom.setAttribute('value', s)

    string = property(__get_string, __set_string)

    def __str__(self):
        return self._value

class setting_bool(setting_string):
    def __init__(self, xml_dom):
        setting_string.__init__(self, xml_dom)

        val = self.string.lower()
        if val == "true" or val == "1" or val == "on":
            self._bool = True
        else:
            self._bool = False

    def __get_bool(self):
        return self._bool

    def __set_bool(self, b):
        self._bool = b
        if b:
            self.string = "True"
        else:
            self.string = "False"

    bool = property(__get_bool, __set_bool)

    def __bool__(self):
        return self._bool

class orpgSettings:
    def __init__(self):
        self.validate = open_rpg.get_component("validate")
        self.xml = open_rpg.get_component("xml")
        self.log = open_rpg.get_component("log")
        self.changes = []
        self.validate.config_file("settings.xml","default_settings.xml")
        self.filename = orpg.dirpath.dir_struct["user"] + "settings.xml"
        temp_file = open(self.filename)
        txt = temp_file.read()
        temp_file.close()
        self.xml_doc = self.xml.parseXml(txt)

        if self.xml_doc is None:
            self.rebuildSettings()
        self.xml_dom = self.xml_doc.documentElement

    def rebuildSettings(self):
        self.log.log("Settings file has be corrupted, rebuilding settings.", ORPG_INFO, True)
        try:
            os.remove(self.filename)
        except:
            pass

        self.validate.config_file("settings.xml","default_settings.xml")
        temp_file = open(self.filename)
        txt = temp_file.read()
        temp_file.close()
        self.xml_doc = self.xml.parseXml(txt)
        self.xml_dom = self.xml_doc.documentElement

    def get_setting(self, name):
        try:
            return self.xml_dom.getElementsByTagName(name)[0].getAttribute("value")
        except:
            return None

    def get_setting_keys(self):
        keys = []
        tabs = self.xml_dom.getElementsByTagName("tab")
        for i in range(0, len(tabs)):
            if tabs[i].getAttribute("type") == 'grid':
                children = tabs[i].childNodes
                for c in children:
                    keys.append(c.tagName)
        return keys

    def set_setting(self, name, value):
        self.xml_dom.getElementsByTagName(name)[0].setAttribute("value", value)

    def add_setting(self, tab, setting, value, options, help):
        if len(self.xml_dom.getElementsByTagName(setting)) > 0:
            return None
        new = self.xml_doc.createElement(setting)
        new.setAttribute("help", help)
        new.setAttribute("options", options)
        new.setAttribute("value", value)

        for t in self.xml_dom.getElementsByTagName("tab"):
            if t.getAttribute("name").lower() == tab and t.getAttribute("type") == "grid":
                t.appendChild(new)
                return new
        return None

    def lookup(self, tab, setting, type_, default, help):
        try:
            setting_node = self.xml_dom.getElementsByTagName(setting)[0]
        except:
            setting_node = self.add_setting(tab, setting, default, type_, help)
        if type_ == str or type_ == "string":
            return setting_string(setting_node)
        if type_ == bool or type_ == "bool":
            return setting_bool(setting_node)
        else:
            return None

    def add_tab(self, parent, tabname, tabtype):
        tab_xml = '<tab '
        if tabtype == 'text':
            tab_xml += 'name="' + tabname + '" type="text" />'
        else:
            tab_xml += 'name="' + tabname + '" type="' + tabtype + '"></tab>'
        newtab = self.xml.parseXml(tab_xml).documentElement
        if parent != None:
            tabs = self.xml_dom.getElementsByTagName("tab")
            for i in range(0, len(tabs)):
                if tabs[i].getAttribute("name") == parent and tabs[i].getAttribute("type") == 'tab':
                    children = tabs[i].childNodes
                    for c in children:
                        if c.getAttribute("name") == tabname:
                            return False
                    tabs[i].appendChild(newtab)
                    return True
        else:
            children = self.xml_dom.childNodes
            for c in children:
                if c.getAttribute("name") == tabname:
                    return False
            self.xml_dom.appendChild(newtab)
            return True
        return False

    def updateIni(self):
        defaultFile = orpg.dirpath.dir_struct['template'] + 'default_settings.xml'
        temp_file = open(defaultFile)
        txt = temp_file.read()
        temp_file.close()
        default_dom = self.xml.parseXml(txt).documentElement
        for child in default_dom.getChildren():
            if child.tagName == 'tab' and child.hasChildNodes():
                self.proccessChildren(child)
        default_dom.unlink()

    def proccessChildren(self, dom, parent=None):
        if dom.tagName == 'tab':
            self.add_tab(parent, dom.getAttribute("name"), dom.getAttribute("type"))

        for child in dom.getChildren():
            if child.tagName == 'tab' and child.hasChildNodes():
                self.proccessChildren(child, dom.getAttribute("name"))
            else:
                self.add_setting(dom.getAttribute("name"), child.tagName, child.getAttribute("value"), child.getAttribute("options"), child.getAttribute("help"))

    def save(self):
        temp_file = open(self.filename, "w")
        temp_file.write(self.xml.toxml(self.xml_dom,1))
        temp_file.close()

class orpgSettingsWnd(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, PRODUCT + " Preferences",
                           wx.DefaultPosition, size = wx.Size(-1,-1),
                           style=wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION)
        self.Freeze()
        self.validate = open_rpg.get_component("validate")
        self.settings = open_rpg.get_component("settings")
        self.chat = open_rpg.get_component("chat")
        self.changes = []
        self.SetMinSize((545,500))
        self.tabber = orpgTabberWnd(self, style=FNB.FNB_NO_X_BUTTON)
        self.build_gui()
        self.tabber.SetSelection(0)
        winsizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.Button(self, wx.ID_OK, "OK"), 1, wx.EXPAND)
        sizer.Add(wx.Size(10,10))
        sizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 1, wx.EXPAND)
        winsizer.Add(self.tabber, 1, wx.EXPAND)
        winsizer.Add(sizer, 0, wx.EXPAND)
        self.winsizer = winsizer
        self.SetSizer(self.winsizer)
        self.SetAutoLayout(True)
        self.Fit()
        self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
        self.Thaw()

    def on_size(self,evt):
        (w,h) = self.GetClientSizeTuple()
        self.winsizer.SetDimension(0,0,w,h-25)

    def build_gui(self):
        self.validate.config_file("settings.xml","default_settings.xml")
        filename = open_rpg.get_component("dir_struct")["user"] + "settings.xml"
        temp_file = open(filename)
        temp_file.close()
        children = self.settings.xml_dom.childNodes
        for c in children:
            self.build_window(c,self.tabber)

    def build_window(self, xml_dom, parent_wnd):
        name = xml_dom.nodeName
        #container = 0
        if name=="tab":
            temp_wnd = self.do_tab_window(xml_dom,parent_wnd)
        return temp_wnd

    def do_tab_window(self, xml_dom, parent_wnd):
        type = xml_dom.getAttribute("type")
        name = xml_dom.getAttribute("name")

        if type == "grid":
            temp_wnd = self.do_grid_tab(xml_dom, parent_wnd)
            parent_wnd.AddPage(temp_wnd, name, False)
        elif type == "tab":
            temp_wnd = orpgTabberWnd(parent_wnd, style=FNB.FNB_NO_X_BUTTON)
            children = xml_dom.childNodes
            for c in children:
                if c.nodeName == "tab":
                    self.do_tab_window(c, temp_wnd)
            temp_wnd.SetSelection(0)
            parent_wnd.AddPage(temp_wnd, name, False)
        elif type == "text":
            temp_wnd = wx.TextCtrl(parent_wnd,-1)
            parent_wnd.AddPage(temp_wnd, name, False)
        else:
            temp_wnd = None
        return temp_wnd

    def do_grid_tab(self, xml_dom, parent_wnd):
        settings = []
        children = xml_dom.childNodes
        for c in children:
            name = c.nodeName
            value = c.getAttribute("value")
            help = c.getAttribute("help")
            options = c.getAttribute("options")
            settings.append([name, value, options, help])
        temp_wnd = settings_grid(parent_wnd, settings, self.changes)
        return temp_wnd

    def onOk(self, evt):
        #This will write the settings back to the XML
        self.session = open_rpg.get_component("session")

        for i in range(0,len(self.changes)):
            self.settings.set_setting(self.changes[i][0], self.changes[i][1])
            top_frame = open_rpg.get_component('frame')

            if self.changes[i][0] == 'bgcolor' or self.changes[i][0] == 'textcolor':
                self.chat.chatwnd.SetPage(self.chat.ResetPage())
                self.chat.chatwnd.scroll_down()
                if self.settings.get_setting('ColorTree') == '1':
                    top_frame.tree.SetBackgroundColour(self.settings.get_setting('bgcolor'))
                    top_frame.tree.SetForegroundColour(self.settings.get_setting('textcolor'))
                    top_frame.tree.Refresh()
                    top_frame.players.SetBackgroundColour(self.settings.get_setting('bgcolor'))
                    top_frame.players.SetForegroundColour(self.settings.get_setting('textcolor'))
                    top_frame.players.Refresh()
                else:
                    top_frame.tree.SetBackgroundColour('white')
                    top_frame.tree.SetForegroundColour('black')
                    top_frame.tree.Refresh()
                    top_frame.players.SetBackgroundColour('white')
                    top_frame.players.SetForegroundColour('black')
                    top_frame.players.Refresh()

            if self.changes[i][0] == 'ColorTree':
                if self.changes[i][1] == '1':
                    top_frame.tree.SetBackgroundColour(self.settings.get_setting('bgcolor'))
                    top_frame.tree.SetForegroundColour(self.settings.get_setting('textcolor'))
                    top_frame.tree.Refresh()
                    top_frame.players.SetBackgroundColour(self.settings.get_setting('bgcolor'))
                    top_frame.players.SetForegroundColour(self.settings.get_setting('textcolor'))
                    top_frame.players.Refresh()
                else:
                    top_frame.tree.SetBackgroundColour('white')
                    top_frame.tree.SetForegroundColour('black')
                    top_frame.tree.Refresh()
                    top_frame.players.SetBackgroundColour('white')
                    top_frame.players.SetForegroundColour('black')
                    top_frame.players.Refresh()

            if self.changes[i][0] == 'GMWhisperTab' and self.changes[i][1] == '1':
                self.chat.parent.create_gm_tab()
            self.toggleToolBars(self.chat, self.changes[i])
            try:
                self.toggleToolBars(self.chat.parent.GMChatPanel, self.changes[i])
            except:
                pass
            for panel in self.chat.parent.whisper_tabs:
                self.toggleToolBars(panel, self.changes[i])
            for panel in self.chat.parent.group_tabs:
                self.toggleToolBars(panel, self.changes[i])
            for panel in self.chat.parent.null_tabs:
                self.toggleToolBars(panel, self.changes[i])

            if self.changes[i][0] == 'player':
                self.session.name = self.changes[i][1]

        self.settings.save()
        self.Destroy()

    def toggleToolBars(self, panel, changes):
        if changes[0] == 'AliasTool_On':
            panel.toggle_alias(changes[1])
        elif changes[0] == 'DiceButtons_On':
            panel.toggle_dice(changes[1])
        elif changes[0] == 'FormattingButtons_On':
            panel.toggle_formating(changes[1])

class settings_grid(wx.grid.Grid):
    """grid for gen info"""
    def __init__(self, parent, settings, changed = []):
        wx.grid.Grid.__init__(self, parent, -1, style=wx.SUNKEN_BORDER | wx.WANTS_CHARS)
        self.setting_data = changed
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.on_cell_change)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_left_click)
        self.CreateGrid(len(settings),3)
        self.SetRowLabelSize(0)
        self.SetColLabelValue(0,"Setting")
        self.SetColLabelValue(1,"Value")
        self.SetColLabelValue(2,"Available Options")
        self.settings = settings
        for i in range(len(settings)):
            self.SetCellValue(i,0,settings[i][0])
            self.SetCellValue(i,1,settings[i][1])
            if settings[i][1] and settings[i][1][0] == '#':
                self.SetCellBackgroundColour(i,1,settings[i][1])
            self.SetCellValue(i,2,settings[i][2])

    def on_left_click(self,evt):
        row = evt.GetRow()
        col = evt.GetCol()
        if col == 2:
            return
        elif col == 0:
            name = self.GetCellValue(row,0)
            str = self.settings[row][3]
            msg = wx.MessageBox(str,name)
            return
        elif col == 1:
            setting = self.GetCellValue(row,0)
            value = self.GetCellValue(row,1)
            if value and value[0] == '#':
                hexcolor = orpg.tools.rgbhex.RGBHex().do_hex_color_dlg(self)
                if hexcolor:
                    self.SetCellValue(row,2, hexcolor)
                    self.SetCellBackgroundColour(row,1,hexcolor)
                    self.Refresh()
                    setting = self.GetCellValue(row,0)
                    self.setting_data.append([setting, hexcolor])
            else:
                evt.Skip()

    def on_cell_change(self,evt):
        row = evt.GetRow()
        col = evt.GetCol()
        if col != 1:
            return
        setting = self.GetCellValue(row,0)
        value = self.GetCellValue(row,1)
        self.setting_data.append([setting, value])

    def get_h(self):
        (w,h) = self.GetSize()
        rows = self.GetNumberRows()
        minh = 0
        for i in range (0,rows):
            minh += self.GetRowSize(i)
        minh += 120
        return minh

    def on_size(self,evt):
        (w,h) = self.GetSize()
        cols = self.GetNumberCols()
        col_w = w/(cols)
        for i in range(0,cols):
            self.SetColSize(i,col_w)
        self.Refresh()
