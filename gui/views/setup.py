from core.db import create_database
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class SetupView(Gtk.Frame):
    def __init__(self, window):
        super().__init__()
        self.set_border_width(175)
        self.set_shadow_type(Gtk.ShadowType.NONE)

        self.window = window

        title = Gtk.Label()
        title.set_markup("<span font='24' weight='bold'>pm</span>")

        description = Gtk.Label("Set a master password.")

        self.p1 = Gtk.Entry()
        self.p1.set_margin_start(250)
        self.p1.set_margin_end(250)
        self.p1.set_visibility(False)

        self.p2 = Gtk.Entry()
        self.p2.set_margin_start(250)
        self.p2.set_margin_end(250)
        self.p2.set_visibility(False)

        self.password_strength = Gtk.ProgressBar()
        self.password_strength.set_fraction(0.0)
        self.password_strength.set_margin_start(250)
        self.password_strength.set_margin_end(250)
        self.p1.connect("changed", self.update_strength)

        confirm = Gtk.Button(label="Confirm")
        confirm.set_margin_start(250)
        confirm.set_margin_end(250)
        confirm.connect("clicked", self.password_confirmed)

        self.error = Gtk.Label(label="")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        box.pack_start(title, False, False, 10)
        box.pack_start(description, False, False, 0)
        box.pack_start(self.p1, False, False, 0)
        box.pack_start(self.p2, False, False, 0)
        box.pack_start(self.password_strength, False, False, 10)
        box.pack_start(confirm, False, False, 10)
        box.pack_start(self.error, False, False, 10)

        self.add(box)

    def calculate_strength(self, password):
        length_strength = min(len(password) / 8.0, 1.0)
        digit_strength = 1.0 if any(char.isdigit() for 
            char in password) else 0.0
        uppercase_strength = 1.0 if any(char.isupper() for 
            char in password) else 0.0
        other_strength = 1.0 if any(not char.isalnum() for 
            char in password) else 0.0

        overall_strength = (length_strength + digit_strength +
            uppercase_strength + other_strength) / 4.0
        return overall_strength

    def update_strength(self, p1):
        password = p1.get_text()
        strength = self.calculate_strength(password)
        self.password_strength.set_fraction(strength)

    def password_confirmed(self, widget):
        p1 = self.p1.get_text()
        p2 = self.p2.get_text()
        if p1 != p2:
            self.error.set_text("Passwords do not match.")
            return
        if self.calculate_strength(p1) < 1:
            self.error.set_text("Password is not strong enough.")
            return

        create_database()
        self.window.settings.create_settings()
        self.window.mp.create_master_password(p1)
        self.window.stack.set_visible_child_name("unlocker")
