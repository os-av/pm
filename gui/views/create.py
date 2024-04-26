import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from core.generator import Generator
from core.fetchimage import fetch_image

class CreateView(Gtk.Grid):
    """
    View for creating new credentials.
    """
    def __init__(self, window):
        super().__init__()
        
        self.window = window

        title_label = Gtk.Label()
        title_label.set_markup("<span font='24' \
        weight='bold'>pm</span>")
        title_label.set_margin_top(10)

        frame = Gtk.Frame()
        frame.set_border_width(60)
        frame.set_shadow_type(Gtk.ShadowType.NONE)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)

        account_label = Gtk.Label()
        account_label.set_markup("<span font='18' style='italic' \
                                 >Account (required)</span>")
        account_label.set_halign(Gtk.Align.START)
        account_label.set_margin_left(10)
        self.account = Gtk.Entry()

        username_label = Gtk.Label()
        username_label.set_markup("<span font='18' style='italic' \
                                  >Username (required)</span>")
        username_label.set_halign(Gtk.Align.START)
        username_label.set_margin_left(10)
        self.username = Gtk.Entry()

        password_label = Gtk.Label()
        password_label.set_markup("<span font='18' style='italic' \
                                  >Password (required)</span>")
        password_label.set_halign(Gtk.Align.START)
        password_label.set_margin_left(10)

        pw_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.password = Gtk.Entry()
        gen_pass_button = Gtk.Button.new_from_icon_name("view-refresh",
                                                   Gtk.IconSize.BUTTON)
        gen_pass_button.connect("clicked", self.on_gen_pass_clicked)
        visibility_button = Gtk.Button.new_from_icon_name("face-wink",
                                                   Gtk.IconSize.BUTTON)
        visibility_button.connect("clicked", self.on_visibility_clicked)

        pw_box.pack_start(self.password, True, True, 0)
        pw_box.pack_start(gen_pass_button, False, False, 0)
        pw_box.pack_start(visibility_button, False, False, 0)

        url_label = Gtk.Label()
        url_label.set_markup("<span font='18' style='italic'>Website</span>")
        url_label.set_halign(Gtk.Align.START)
        url_label.set_margin_left(10)
        self.url = Gtk.Entry()

        email_label = Gtk.Label()
        email_label.set_markup("<span font='18' style='italic'>Email</span>")
        email_label.set_halign(Gtk.Align.START)
        email_label.set_margin_left(10)
        self.email = Gtk.Entry()

        notes_label = Gtk.Label()
        notes_label.set_markup("<span font='18' style='italic'>Notes</span>")
        notes_label.set_halign(Gtk.Align.START)
        notes_label.set_margin_left(10)
        self.notes = Gtk.TextView()
        notes_window = Gtk.ScrolledWindow()
        notes_window.set_vexpand(True)
        notes_window.add(self.notes)

        confirm = Gtk.Button.new_from_icon_name("gtk-apply",
                                                   Gtk.IconSize.BUTTON)
        confirm.connect("clicked", self.on_confirm_clicked)
        back = Gtk.Button.new_from_icon_name("go-previous",
                                                   Gtk.IconSize.BUTTON)
        back.connect("clicked", self.on_back_clicked)
        clear = Gtk.Button.new_from_icon_name("user-trash",
                                                   Gtk.IconSize.BUTTON)
        clear.connect("clicked", self.on_clear_clicked)
        self.error = Gtk.Label(label="")
        self.error.set_margin_left(10)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_margin_top(20)
        button_box.pack_start(back,       False, False, 0)
        button_box.pack_start(confirm,    False, False, 0)
        button_box.pack_start(clear,      False, False, 0)
        button_box.pack_start(self.error, False, False, 0)

        box.pack_start(account_label,  False, False, 0)
        box.pack_start(self.account,   False, False, 0)
        box.pack_start(username_label, False, False, 0)
        box.pack_start(self.username,  False, False, 0)
        box.pack_start(password_label, False, False, 0)
        box.pack_start(pw_box,         False, False, 0)
        box.pack_start(url_label,      False, False, 0)
        box.pack_start(self.url,       False, False, 0)
        box.pack_start(email_label,    False, False, 0)
        box.pack_start(self.email,     False, False, 0)
        box.pack_start(notes_label,    False, False, 0)
        box.pack_start(notes_window,   True,  True,  0)
        box.pack_start(button_box,     False, False, 0)

        frame.add(box)

        self.attach(title_label, 0, 0, 2, 1)
        self.attach(frame,       0, 1, 2, 1)

        title_label.set_hexpand(True)
        title_label.set_halign(Gtk.Align.FILL)

    def on_confirm_clicked(self, button):
        account = self.account.get_text()
        username = self.username.get_text()
        password = self.password.get_text()

        if len(account) == 0 or len(username) == 0 or len(password) == 0:
            self.error.set_text("A required field is empty.")
            return

        if self.window.pm.read_credential_by_account(account):
            self.error.set_text("An account using this name already exists.")
            return

        website = self.url.get_text()
        email = self.email.get_text()
        notes_buffer = self.notes.get_buffer()
        notes = notes_buffer.get_text(
            notes_buffer.get_start_iter(),
            notes_buffer.get_end_iter(),
            True
        )

        self.window.pm.create_new_credential(account, username, password,
                                      website, email, notes)
        try:
            fetch_image(website)
        except Exception as e:
            print(f"ERROR: {e}")

        self.account.set_text("")
        self.username.set_text("")
        self.password.set_text("")
        self.url.set_text("")
        self.email.set_text("")
        notes_buffer = self.notes.get_buffer()
        notes_buffer.set_text("")

        main = self.window.stack.get_child_by_name("main")
        main.get_credential_list()
        main.update_credential_listbox()
        self.window.stack.set_visible_child_name("main")

    def on_gen_pass_clicked(self, button):
        generator = Generator()
        password = generator.generate_password()
        self.password.set_text(password)

    def on_clear_clicked(self, button):
        self.account.set_text("")
        self.username.set_text("")
        self.password.set_text("")
        self.url.set_text("")
        self.email.set_text("")
        textbuffer = self.notes.get_buffer()
        textbuffer.set_text("")

    def on_visibility_clicked(self, button):
        if self.password.get_visibility() is True:
            self.password.set_visibility(False)
            self.password.set_invisible_char("*")
        else:
            self.password.set_visibility(True)

    def on_back_clicked(self, button):
        self.window.stack.set_visible_child_name("main")
