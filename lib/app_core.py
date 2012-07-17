import os
import gtk
import zbarpygtk
import pynotify
import ConfigParser
from lib.scanner import Scanner

class Clipboard():
    def __init__(self,core_instance):
        self.core_instance = core_instance
        
    def __call__(self,text):
        if self.core_instance.settings.get_boolean_config('copy_automatically_to_clipboard'):
            clipboard = gtk.Clipboard(selection='CLIPBOARD')
            clipboard.set_text(text)

class Notify():
    def __init__(self,core_instance):
        self.core_instance = core_instance
        pynotify.init('webbar')
        
    def __call__(self,title,text):
        if self.core_instance.settings.get_boolean_config('show_desktop_notify'):
            notification = pynotify.Notification(title, text, 'webbar')
            notification.show()

class TrayIcon():
    def __init__(self,core_instance):
        self.core_instance = core_instance
        self.icon = gtk.StatusIcon()
        self.icon.set_from_stock(gtk.STOCK_INDEX)
        self.icon.set_tooltip('Webbar')
        self.icon.set_visible(self.core_instance.settings.get_boolean_config('show_tray_icon'))
        self.icon.connect('activate',self.on_clicked)
        
    def on_clicked(self,icon):
        self.core_instance.main_window.set_visible(True)
        
class Settings():
    def __init__(self):
	self._config = ConfigParser.ConfigParser()
	self.config_file = os.path.expanduser('~/.webbar.conf')
	
	#Fix Bug #1021329 
	try:
            file_for_reading = open(self.config_file,'r')
        except IOError:
            file_for_writing = open(self.config_file,'w')
            
            defaults = [
                '[webbar]',
                'video_device = /dev/video0',
                'copy_automatically_to_clipboard = True',
                'show_tray_icon = True',
                'show_desktop_notify = True',
            ]
            
            for item in defaults:
                file_for_writing.write("%s\n" % item)
                
            file_for_writing.close()

        else:
            file_for_reading.close()
            
	self._config.read(['data/defaults.conf',self.config_file])

    def get_config(self,name):
        try:
            return self._config.get('webbar',name)
        except:
            return '/dev/video0'
	
    def get_boolean_config(self,name):
        try:
            return self._config.getboolean('webbar',name)
        except:
            return True
	
    def set_config(self,name,value):
	self._config.set('webbar',name,str(value))
	self.write_config_file()
	
    def toggle_boolean_config(self,name):
        current_value = self.get_boolean_config(name)
        current_value = not current_value
        self.set_config(name,current_value)
	
    def write_config_file(self):
	with open(self.config_file, 'wb') as config_file:
	  self._config.write(config_file)

class AppCore():
    def __init__(self):
	self.settings = Settings()
        self.notify = Notify(self)
        self.clipboard = Clipboard(self)
        self.scanner = Scanner(self)
        self.tray_icon = TrayIcon(self)

    def on_barcode_decoded(self,barcode):
        self.main_window.on_barcode_decoded(barcode)
        if ':' in barcode:
            barcode = barcode.split(':')[1]
        self.clipboard(barcode)
        self.notify('Webbar','Your barcode was scanned and copied to clipboard')
