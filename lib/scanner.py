import gtk
import zbarpygtk

class Scanner():
    def __init__(self,core_instance):
        self._initialize_threads()
        self.core_instance = core_instance
        
    def _initialize_threads(self):
        gtk.gdk.threads_init()
        gtk.gdk.threads_enter()
        
    def barcode_decoded_callback(self,widget,barcode):
        self.core_instance.on_barcode_decoded(barcode)

    def get_widget(self):
        widget = zbarpygtk.Gtk()
        widget.set_video_device(self.core_instance.settings.get_config('video_device'))
        widget.set_video_enabled(True)
        widget.connect("decoded-text", self.barcode_decoded_callback)
        return widget
