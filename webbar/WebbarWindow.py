# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Lucas R. Martins <lukasrms@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('webbar')

import gtk
import logging
logger = logging.getLogger('webbar')

from webbar_lib import Window
from webbar.AboutWebbarDialog import AboutWebbarDialog
from webbar.PreferencesWebbarDialog import PreferencesWebbarDialog

# See webbar_lib.Window.py for more details about how this class works
class WebbarWindow(Window):
    __gtype_name__ = "WebbarWindow"
    
    def _get_widget_by_name(self,parent,name):
        return filter(lambda x: x.get_name() == name,parent.get_children())[0]
    
    def on_barcode_decoded(self,barcode):
        label = self._get_widget_by_name(self.get_child(),'GtkLabel')
        label.set_text(barcode)
    
    def setup_barcode_widget(self,scanner):
        vbox = self.get_child()
        hbox = self._get_widget_by_name(self.get_child(),'GtkHBox')
        hbox.add(scanner.get_widget())

        self.show_all()
        
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(WebbarWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutWebbarDialog
        self.PreferencesDialog = PreferencesWebbarDialog

        # Code for other initialization actions should be added here.
        
    def on_mnu_minimize_activate(self,menu):
        self.set_visible(False)
        self.core_instance.notify('Webbar window hidden','Click on the system tray icon to show it again')


