import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango
import webbrowser
import os
import platform

class MainView(Gtk.Grid):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.credential_list = []
        self.visibility = False

        title_label = Gtk.Label()
        title_label.set_markup("<span font='24' \
        weight='bold'>pm</span>")
        title_label.set_margin_top(10)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_bottom(10)
        separator.set_margin_top(10)

        button_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        create_button = Gtk.Button.new_from_icon_name("document-new",
                                              Gtk.IconSize.BUTTON)
        create_button.connect("clicked", self.on_create_clicked)
        create_button.set_margin_left(15)

        update_button = Gtk.Button.new_from_icon_name("document-edit",
                                              Gtk.IconSize.BUTTON)
        update_button.connect("clicked", self.on_update_clicked)

        go_button = Gtk.Button.new_from_icon_name("media-playback-start",
                                                   Gtk.IconSize.BUTTON)
        go_button.connect("clicked", self.on_go_clicked)

        delete_button = Gtk.Button.new_from_icon_name("edit-delete",
                                                   Gtk.IconSize.BUTTON)
        delete_button.connect("clicked", self.on_delete_clicked)

        settings_button = Gtk.Button.new_from_icon_name("preferences-system",
                                                   Gtk.IconSize.BUTTON)
        settings_button.connect("clicked", self.on_settings_clicked)

        visibility_button = Gtk.Button.new_from_icon_name("face-wink",
                                                   Gtk.IconSize.BUTTON)
        visibility_button.connect("clicked", self.on_visibility_clicked)

        about_button = Gtk.Button.new_from_icon_name("help-about",
                                                   Gtk.IconSize.BUTTON)

        search_bar = Gtk.SearchEntry()
        search_bar.connect("activate", self.on_search_changed)
        search_bar.set_margin_left(50)
        search_bar.set_margin_right(50)

        button_bar.pack_start(create_button,     False, False, 0)
        button_bar.pack_start(update_button,     False, False, 0)
        button_bar.pack_start(go_button,         False, False, 0)
        button_bar.pack_start(delete_button,     False, False, 0)
        button_bar.pack_start(settings_button,   False, False, 0)
        button_bar.pack_start(visibility_button, False, False, 0)
        button_bar.pack_start(about_button,      False, False, 0)
        button_bar.pack_start(search_bar,        True,  True,  0)

        separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator2.set_margin_bottom(10)
        separator2.set_margin_top(10)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_shadow_type(Gtk.ShadowType.OUT)
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)

        self.liststore = Gtk.ListStore(int, str, str, str, str, str)
        self.listbox = Gtk.ListBox()
        scrolled_window.add(self.listbox)

        self.attach(title_label,              0, 0, 1, 1)
        self.attach(separator,                0, 1, 1, 1)
        self.attach(button_bar,               0, 2, 1, 1)
        self.attach(separator2,               0, 3, 1, 1)
        self.attach(scrolled_window,          0, 4, 1, 1)

    def on_visibility_clicked(self, button):
        if self.visibility is True:
            self.visibility = False
        else:
            self.visibility = True
        self.update_credential_listbox()

    def on_go_clicked(self, button):
        selected_row = self.listbox.get_selected_row()
        if not selected_row:
            return
        
        account_text = selected_row.get_child().get_children()[1].get_text()
        account = self.window.pm.read_credential_by_account(account_text)
        password = account[3]
        
        url = account[4]
        if len(url) > 0:
            if url[:8] != 'https://':
                url = 'https://' + url
            webbrowser.open(url)

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(password, -1)
        
    def on_create_clicked(self, button):
        self.window.stack.set_visible_child_name("create")

    def on_update_clicked(self, button):
        selected_row = self.listbox.get_selected_row()
        if selected_row is None:
            return

        account = selected_row.get_child().get_children()[1].get_text()

        data = []
        for cred in self.credential_list:
            if cred[1] == account:
                data = cred
                break

        update = self.window.stack.get_child_by_name("update")
        update.credential = data
        update.set_fields()
        self.window.stack.set_visible_child_name("update")

    def on_settings_clicked(self, button):
        settings = self.window.stack.get_child_by_name("settings")
        settings.set_fields()
        self.window.stack.set_visible_child_name("settings")

    def on_delete_clicked(self, button):
        selected_row = self.listbox.get_selected_row()
        if selected_row is None:
            return
        account = selected_row.get_child().get_children()[1].get_text()

        dialog = Gtk.MessageDialog(
            parent = self.get_toplevel(),
            flags = 0,
            message_type = Gtk.MessageType.QUESTION,
            buttons = Gtk.ButtonsType.YES_NO,
            text = "CONFIRM"
        )
        dialog.format_secondary_text("Are you sure? This action cannot be undone.")

        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            id = self.window.pm.read_credential_by_account(account)[0]
            self.window.pm.delete_credential_by_id(id)
            self.update_credential_listbox()

    def get_credential_list(self):
        self.credential_list = self.window.pm.read_all_credentials()

    def on_search_changed(self, search_entry):
        search = search_entry.get_text()
        self.search_credential_list(search)

    def search_credential_list(self, search):
        self.liststore.clear()
        for row in self.listbox.get_children():
            self.listbox.remove(row)

        for cred in self.credential_list:
            if search.lower() in cred[1].lower():
                self.liststore.append(cred[:-1])

        for row in self.liststore:
            self.create_listbox_row(row)
        self.listbox.show_all()

    def update_credential_listbox(self):
        self.liststore.clear()
        self.credential_list = self.window.pm.read_all_credentials()

        for row in self.listbox.get_children():
            self.listbox.remove(row)

        for cred in self.credential_list:
            self.liststore.append(cred[:-1])

        for row in self.liststore:
            self.create_listbox_row(row)
        self.listbox.show_all()

    def create_listbox_row(self, row):
        listbox_row = Gtk.ListBoxRow()
        listbox_row.set_margin_top(5)
        listbox_row.set_margin_bottom(5)
        row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        grid = Gtk.Grid(column_homogeneous=True,
                         row_spacing=10)
        grid.set_hexpand(False)
        grid.set_vexpand(False)

        image_file = self.get_image(row[4])
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_file)
        scaled = pixbuf.scale_simple(50, 50, GdkPixbuf.InterpType.BILINEAR)
        image = Gtk.Image.new_from_pixbuf(scaled)
        image.set_margin_left(20)

        account_label = Gtk.Label()
        account_label.set_width_chars(30)
        account_label.set_ellipsize(Pango.EllipsizeMode.END)
        account_label.set_markup(f"<span font='20' \
        weight='bold' style='italic'>{row[1]}</span>")

        username_label = Gtk.Label(label=row[2])
        username_label.set_halign(Gtk.Align.START)

        if self.visibility is True:
            password_label = Gtk.Label(label=row[3])
        else:
            password_label = Gtk.Label(label="*"*len(row[3]))
        password_label.set_halign(Gtk.Align.START) 

        website_label = Gtk.Label(label=row[4])
        website_label.set_halign(Gtk.Align.START)

        email_label = Gtk.Label(label=row[5])
        email_label.set_halign(Gtk.Align.START)

        details_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        details_box.pack_start(username_label, False, False, 0)
        details_box.pack_start(password_label, False, False, 0)
        details_box.pack_start(website_label, False, False, 0)
        details_box.pack_start(email_label, False, False, 0)

        row_box.pack_start(image,  False, False, 0)
        row_box.pack_start(account_label, False, False, 20)
        row_box.pack_start(details_box, False, False, 0)

        listbox_row.add(row_box)
        self.listbox.add(listbox_row)

    def get_image(self, file_name):
        directory = {
            "Linux": os.path.expanduser("~/.local/share/pm/images/"),
            "Windows": os.path.expanduser("~\\AppData\\pm\\images\\"),
        }
        dir = directory.get(platform.system())

        if not os.path.exists(dir):
            return "assets/default.png"

        for file in os.listdir(dir):
            if file == file_name:
                return os.path.join(dir, file_name)
        return "assets/default.png"
