from core import pm, mp
from core.settings import Settings
from gui.views.unlocker import UnlockerView
from gui.views.create import CreateView
from gui.views.main import MainView
from gui.views.update import UpdateView
from gui.views.setup import SetupView
from gui.views.settings import SettingsView
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="pm")

        self.set_border_width(10)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        self.mp = mp.MasterPassword()
        self.pm = pm.PasswordManager()
        self.settings = Settings()

        if self.mp.master_password_setup_required():
            setup = SetupView(self)
            self.stack.add_named(setup, "setup")

        unlocker = UnlockerView(self)
        main     = MainView(self)
        create   = CreateView(self)
        update   = UpdateView(self)
        settings = SettingsView(self)

        self.stack.add_named(unlocker, "unlocker")
        self.stack.add_named(main,     "main")
        self.stack.add_named(create,   "create")
        self.stack.add_named(update,   "update")
        self.stack.add_named(settings, "settings")
        self.add(self.stack)
