# GUI Application automation and testing library
# Copyright (C) 2015 Intel Corporation
# Copyright (C) 2015 Zoya Maslova (Nizhny Novgorod State University)
# Copyright (C) 2010 Mark Mc Mahon
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
#    Free Software Foundation, Inc.,
#    59 Temple Place,
#    Suite 330,
#    Boston, MA 02111-1307 USA

"""Module showing how to work with the task bar

This module will likely change significantly in the future!"""

import warnings

from pywinauto import win32defines
from pywinauto import findwindows
from pywinauto import application

warnings.warn("The taskbar module is still very experimental", FutureWarning)

def TaskBarHandle():
    "Return the first window that has a class name 'Shell_TrayWnd'"
    return findwindows.find_windows(class_name = "Shell_TrayWnd")[0]


def _get_visible_button_index(reqd_button):
    return SystemTrayIcons.Button(reqd_button).index

def _click_hidden_tray_icon(reqd_button, is_left_click = True):
    #ShowHiddenIconsButton.ClickInput()
    popup_dlg = explorer_app.Window_(class_name='NotifyIconOverflowWindow')
    try:
        popup_toolbar = popup_dlg.OverflowNotificationAreaToolbar.Wait('visible')
        button_index = popup_toolbar.Button(reqd_button).index
    except:
        ShowHiddenIconsButton.ClickInput() # may fail from PythonWin when script takes long time
        popup_dlg = explorer_app.Window_(class_name='NotifyIconOverflowWindow')
        popup_toolbar = popup_dlg.OverflowNotificationAreaToolbar.Wait('visible')
        button_index = popup_toolbar.Button(reqd_button).index

    if is_left_click:
        popup_toolbar.Button(button_index).ClickInput()
    else:
        popup_toolbar.Button(button_index).ClickInput(button='right')

def ClickSystemTrayIcon(button):
    "Click on a visible tray icon given by button"
    button = _get_visible_button_index(button)
    r = SystemTrayIcons.GetButtonRect(button)
    SystemTrayIcons.ClickInput(coords = (r.left+2, r.top+2))

def RightClickSystemTrayIcon(button):
    "Right click on a visible tray icon given by button"
    SystemTrayIcons.Button(button).ClickInput(button='right')

def ClickHiddenSystemTrayIcon(button):
    "Click on a hidden tray icon given by button"
    _click_hidden_tray_icon(button, is_left_click = True)

def RightClickHiddenSystemTrayIcon(button):
    "Right click on a hidden tray icon given by button"
    _click_hidden_tray_icon(button, is_left_click = False)


# windows explorer owns all these windows so get that app
explorer_app = application.Application().connect_(handle = TaskBarHandle())

# Get the taskbar
TaskBar = explorer_app.window_(handle = TaskBarHandle())

# The Start button
StartButton = TaskBar.Start

# the system tray - contains various windows
SystemTray = TaskBar.TrayNotifyWnd

# the clock is in the system tray
Clock = TaskBar.TrayClockWClass

# the show desktop button
ShowDesktop = TaskBar.TrayShowDesktopButtonWClass

# these are the icons - what people normally think of
# as the system tray
SystemTrayIcons = TaskBar.Toolbar

# the toolbar with the running applications
RunningApplications = TaskBar.MSTaskListWClass

# the language bar
try:
    LangPanel = TaskBar.CiceroUIWndFrame.Wait('visible', 0.1) # Win7
except:
    LangPanel = TaskBar.TrayInputIndicatorWClass # Win8.1

# the hidden tray icons button (TODO: think how to optimize)
ShowHiddenIconsButton = [ch for ch in TaskBar.Children() if ch.FriendlyClassName() == 'Button'][-1] #TaskBar.Button #added