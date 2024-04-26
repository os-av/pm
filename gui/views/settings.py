import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from core.settings import Settings

class SettingsView(Gtk.Grid):
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
        title_label.set_hexpand(True)
        title_label.set_halign(Gtk.Align.FILL)

        frame = Gtk.Frame()
        frame.set_border_width(60)
        frame.set_shadow_type(Gtk.ShadowType.NONE)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)

        ##### PASSWORD GENERATOR #####
        # Password length
        pwgen_label = Gtk.Label()
        pwgen_label.set_markup("<span font='18' style='italic' \
                                 >Password Generator</span>")
        pwgen_label.set_halign(Gtk.Align.START)
        pwgen_label.set_margin_left(10)

        pwlen_label = Gtk.Label()
        pwlen_label.set_markup("<span font='14' style='italic' \
                                 >Length</span>")
        pwlen_label.set_halign(Gtk.Align.START)
        pwlen_label.set_margin_left(10)
        pwlen_label.set_margin_top(10)
        pwlen_label.set_margin_left(40)

        self.pwlen_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL, 20, 32, 1)
        self.pwlen_scale.set_margin_left(40)
        self.pwlen_scale.set_margin_right(500)
        
        # Password upper checkbox
        pw_upper_label = Gtk.Label()
        pw_upper_label.set_markup("<span font='14' style='italic' \
                                 >Use uppercase     </span>")
        pw_upper_label.set_halign(Gtk.Align.START)
        pw_upper_label.set_margin_left(10)

        self.pw_upper = Gtk.CheckButton()

        pw_upper_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        pw_upper_box.set_margin_top(20)
        pw_upper_box.pack_start(pw_upper_label, False, False, 0)
        pw_upper_box.pack_start(self.pw_upper,  False, False, 0)
        pw_upper_box.set_margin_left(40)

        # Password special checkbox
        pw_special_label = Gtk.Label()
        pw_special_label.set_markup("<span font='14' style='italic' \
                                 >Use special            </span>")
        pw_special_label.set_halign(Gtk.Align.START)
        pw_special_label.set_margin_left(10)

        self.pw_special = Gtk.CheckButton()

        pw_special_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        pw_special_box.set_margin_top(20)
        pw_special_box.pack_start(pw_special_label, False, False, 0)
        pw_special_box.pack_start(self.pw_special,  False, False, 0)
        pw_special_box.set_margin_left(40)

        ##### UI #####
        ui_label = Gtk.Label()
        ui_label.set_markup("<span font='18' style='italic' \
                                 >UI</span>")
        ui_label.set_halign(Gtk.Align.START)
        ui_label.set_margin_left(10)
        ui_label.set_margin_top(20)

        # Use images
        images_label = Gtk.Label()
        images_label.set_markup("<span font='14' style='italic' \
                                 >Use Images</span>")
        images_label.set_halign(Gtk.Align.START)
        images_label.set_margin_left(10)
        images_label.set_margin_top(10)

        self.images_check = Gtk.CheckButton()
        self.images_check.set_margin_top(10)
        self.images_check.set_margin_left(46)

        images_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        images_box.pack_start(images_label,      False, False, 0)
        images_box.pack_start(self.images_check, False, False, 0)
        images_box.set_margin_left(40)

        ##### NAVIGATION #####
        confirm = Gtk.Button.new_from_icon_name("gtk-apply",
                                                   Gtk.IconSize.BUTTON)
        confirm.connect("clicked", self.on_confirm_clicked)
        back = Gtk.Button.new_from_icon_name("go-previous",
                                                   Gtk.IconSize.BUTTON)
        back.connect("clicked", self.on_back_clicked)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_margin_top(150)
        button_box.pack_start(back,     False, False, 0)
        button_box.pack_start(confirm,  False, False, 0)

        box.pack_start(pwgen_label,      False, False, 0)
        box.pack_start(pwlen_label,      False, False, 0)
        box.pack_start(self.pwlen_scale, False, False, 0)
        box.pack_start(pw_upper_box,     False, False, 0)
        box.pack_start(pw_special_box,   False, False, 0)
        box.pack_start(ui_label,         False, False, 0)
        box.pack_start(images_box,       False, False, 0)
        box.pack_start(button_box,       False, False, 0)

        frame.add(box)

        self.attach(title_label, 0, 0, 2, 1)
        self.attach(frame,       0, 1, 2, 1)

    def set_fields(self):
        settings = Settings()
        length  = settings.read_setting("pw_gen", "len")
        upper   = settings.read_boolean_setting("pw_gen", "upper")
        special = settings.read_boolean_setting("pw_gen", "other")
        images  = settings.read_boolean_setting("ui", "use_images")

        self.pwlen_scale.set_value(int(float(length))) 
        self.pw_upper.set_active(upper)
        self.pw_special.set_active(special)
        self.images_check.set_active(images)

    def on_confirm_clicked(self, button):
        settings = Settings()

        new_gen_settings = {
            "len": str(self.pwlen_scale.get_value()),
            "upper": str(self.pw_upper.get_active()),
            "other": str(self.pw_special.get_active()),
        }
        for setting, value in new_gen_settings.items():
            settings.update_setting("pw_gen", setting, value)

        settings.update_setting("ui", "use_images",
                                str(self.images_check.get_active()))
        self.window.stack.set_visible_child_name("main")

    def on_back_clicked(self, button):
        self.window.stack.set_visible_child_name("main")
