import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class UnlockerView(Gtk.Frame):
    def __init__(self, window):
        super().__init__()
        self.set_border_width(250)
        self.set_shadow_type(Gtk.ShadowType.NONE)

        self.window = window

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        self.add(grid)

        title_label = Gtk.Label()
        title_label.set_markup("<span font='24' \
        weight='bold'>pm</span>")

        self.p = Gtk.Entry()
        self.p.set_visibility(False)
        self.p.set_margin_start(200)
        self.p.set_margin_end(200)

        confirm = Gtk.Button(label="Confirm")
        confirm.connect("clicked", self.confirm_clicked)
        confirm.set_margin_start(200)
        confirm.set_margin_end(200)

        self.error = Gtk.Label(label="")

        grid.attach(title_label, 0, 0, 1, 1)
        grid.attach(self.p,      0, 2, 1, 1)
        grid.attach(confirm,     0, 3, 1, 1)
        grid.attach(self.error,  0, 4, 1, 1)

    def confirm_clicked(self, widget):
        p = self.p.get_text()
        if self.window.mp.verify_master_password(p):
            self.window.pm.set_key(p.encode())
            main = self.window.stack.get_child_by_name("main")
            main.get_credential_list()
            main.update_credential_listbox()
            self.window.stack.set_visible_child_name("main")
            return
        self.error.set_text("Access denied.")
        self.p.set_text("")
