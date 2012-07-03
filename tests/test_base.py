#!/usr/bin/python

import sys
import os.path
from mock import Mock,MagicMock
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
from lib.app_core import AppCore
from lib.scanner import Scanner

class TestBase():
    def _mocked_core_instance(self):
        cls = AppCore()
        cls.notify = MagicMock()
        cls.main_window = Mock()
        cls.clipboard = Mock()
        cls.main_window.on_barcode_decoded = MagicMock()
        return cls
    
    def test_should_import_libs(self):
        assert __import__('zbar')
        assert __import__('zbarpygtk')
        assert __import__('ConfigParser')
        
    def test_should_instance_classes(self):
        assert AppCore()
        assert Scanner(self)
        
    def test_scanner_widget_getter_should_return_a_gtk_object(self):
        scanner = Scanner(self)
        widget = scanner.get_widget()
        assert 'ZBarGtk' in str(widget)
        
    def test_on_barcode_detected_should_update_main_window(self):
        cls = self._mocked_core_instance()
        cls.on_barcode_decoded('12345')
        cls.main_window.on_barcode_decoded.assert_called_with('12345')
        
    def test_on_barcode_detected_should_notify(self):
        cls = self._mocked_core_instance()
        cls.on_barcode_decoded('12345')
        cls.notify.assert_called()
        
    def test_on_barcode_detected_should_copy_to_clipboard(self):
        cls = self._mocked_core_instance()
        cls.on_barcode_decoded('EAN13:12345')
        cls.clipboard.assert_called_with('12345')
        
    def test_on_set_config_value_should_write_config_file(self):
	cls = self._mocked_core_instance()
	cls.settings.write_config_file = Mock()
	cls.settings.set_config('test',True)
	cls.settings.write_config_file.assert_called()
        

if __name__ == '__main__':   
    print 'to run all tests, you must install pytest and python-mock'
