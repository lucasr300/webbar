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

"""this dialog adjusts values in the preferences dictionary

requirements:
in module preferences: defaults[key] has a value
self.builder.get_object(key) is a suitable widget to adjust value
widget_methods[key] provides method names for the widget
each widget calls set_preference(...) when it has adjusted value
"""

import gtk
import logging
logger = logging.getLogger('webbar_lib')

from . helpers import get_builder, show_uri, get_help_uri
from . preferences import preferences

class PreferencesDialog(gtk.Dialog):
    __gtype_name__ = "PreferencesDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated PreferencesDialog object.
        """
        builder = get_builder('PreferencesWebbarDialog')
        new_object = builder.get_object("preferences_webbar_dialog")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initalizing should be called after parsing the ui definition
        and creating a PreferencesDialog object with it in order to
        finish initializing the start of the new PerferencesWebbarDialog
        instance.
        
        Put your initialization code in here and leave __init__ undefined.
        """

        # Get a reference to the builder and set up the signals
        self.builder = builder
        self.ui = builder.get_ui(self, True)

        # code for other initialization actions should be added here
        self.widget_methods = []
        
    def set_core_instance(self,core_instance):
        self.core_instance = core_instance
        self.populate_widgets_from_settings()
        
    def populate_widgets_from_settings(self):
        container = self.get_children()[0].get_children()
        entry_container = container[0].get_children()
        checkbuttons_container = container[1].get_children()[:3]

        entry_container[1].set_text(self.core_instance.settings.get_config('video_device'))
        for checkbutton in checkbuttons_container:
            name = gtk.Buildable.get_name(checkbutton)
            checkbutton.set_state(self.core_instance.settings.get_boolean_config(name))
    
    def toggle_setting(self,widget):
        if widget.get_state() == 0: #automatically triggered by GTK
            return
            
        name = gtk.Buildable.get_name(widget)
        self.core_instance.settings.toggle_boolean_config(name)
        
    def entry_changed(self,widget):
        self.core_instance.settings.set_config('video_device',widget.get_text())
        
    def on_btn_close_clicked(self, widget, data=None):
        self.destroy()

    def on_btn_help_clicked(self, widget, data=None):
        show_uri(self, "ghelp:%s" % get_help_uri('preferences'))

