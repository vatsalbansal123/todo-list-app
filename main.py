# Imports
from kivymd.uix.button import MDIconButton
from settings import *
from database.db_functions import (
    add_record,
    c,
    conn,
    delete_record,
    fetch_records,
    update_record,
)

# Set window dimensions and resizability
set_window()

# Content in the dialog
class DialogContent(BoxLayout):
    pass


# Content in the edit dialog
class DialogContentEdit(BoxLayout):
    pass


# Right Container
class Container(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


# creates a dialog
def create_dialog(title, buttons, type=None, content_cls=None):
    if type:
        return MDDialog(
            title=title,
            type=type,
            content_cls=content_cls,
            size_hint=(0.8, 0.5),
            buttons=buttons,
        )
    return MDDialog(title=title, buttons=buttons, size_hint=(0.8, 0.5))


# Custom Checkbox
class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    def on_state(self, instance, obj):
        if self.state == "down":
            instance.parent.parent.markup = True
            if instance.parent.parent.text[-3:] == "/s]":
                pass
            else:
                instance.parent.parent.text = f"[s]{instance.parent.parent.text}[/s]"
            self.check_anim_in.cancel(self)
            self.check_anim_out.start(self)
            self.update_icon()
            self.active = True
            update_record(
                "todo_db",
                instance.parent.parent.text[3:-4],
                instance.parent.parent.text,
                c,
                conn,
            )
            for index, btn in enumerate(
                instance.parent.parent.children[0].children[0].children
            ):
                if btn.icon == "pencil":
                    self.backup_btn = (
                        instance.parent.parent.children[0].children[0].children[index]
                    )
                    instance.parent.parent.children[0].children[0].remove_widget(
                        instance.parent.parent.children[0].children[0].children[index]
                    )

        else:
            instance.parent.parent.markup = False
            update_record(
                "todo_db",
                instance.parent.parent.text,
                instance.parent.parent.text[3:-4],
                c,
                conn,
            )
            instance.parent.parent.text = f"{instance.parent.parent.text[3:-4]}"
            self.check_anim_in.cancel(self)
            self.check_anim_out.start(self)
            self.update_icon()
            self.active = False
            instance.parent.parent.children[0].children[0].add_widget(self.backup_btn)


# Main App Class
class TODO_List_App(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (window_width, window_height)
        self.theme_cls.primary_palette = "Indigo"
        self.title = "Todo List App"
        self.screen = Builder.load_file("main.kv")
        self.custom_checkbox = LeftCheckbox()

    # runs when the app starts
    def on_start(self, **kwargs):
        with open("theme.json", "r") as f:
            data = json.load(f)
        self.theme_cls.theme_style = data["theme"]
        tasks = fetch_records("todo_db", c, conn)
        if tasks:
            self.root.ids.no_task_label.pos_hint = {"center_x": 2}
            for i in range(len(tasks)):
                task = OneLineAvatarIconListItem(text=f"{tasks[i][0]}")
                self.custom_checkbox = LeftCheckbox()
                task.add_widget(self.custom_checkbox)
                btn_two = MDIconButton(
                    icon="pencil",
                    on_release=self.edit,
                )
                btn_one = MDIconButton(icon="delete", on_release=self.delete)
                container = Container()
                container.add_widget(btn_one)
                if tasks[i][0][-3:] == "/s]":
                    pass
                else:
                    container.add_widget(btn_two)
                task.add_widget(container)
                self.root.ids.rv.add_widget(task)
                if tasks[i][0][-3:] == "/s]":
                    task.children[1].children[0].state = "down"
                    self.custom_checkbox.backup_btn = btn_two

    build = lambda self: self.screen

    def edit(self, instance):
        self.edit_dialog = create_dialog(
            "Edit",
            [
                MDFlatButton(text="Cancel", on_release=self.close_edit_dialog),
                MDRaisedButton(
                    text="Save",
                    on_release=lambda x: self.update_changes(instance),
                ),
            ],
            type="custom",
            content_cls=DialogContentEdit(),
        )
        self.edit_dialog.content_cls.ids.edit_task.text = (
            instance.parent.parent.parent.text
        )
        self.edit_dialog.open()

    def update_changes(self, task):
        update_record(
            "todo_db",
            task.parent.parent.parent.text,
            self.edit_dialog.content_cls.ids.edit_task.text,
            c,
            conn,
        )
        task.parent.parent.parent.text = self.edit_dialog.content_cls.ids.edit_task.text
        self.edit_dialog.dismiss()

    def delete(self, instance):
        instance.parent.parent.parent.parent.remove_widget(
            instance.parent.parent.parent
        )
        if instance.parent.parent.parent.text[-3:] == "/s]":
            delete_record("todo_db", instance.parent.parent.parent.text[3:-4], c, conn)
            delete_record("todo_db", instance.parent.parent.parent.text, c, conn)
        else:
            delete_record("todo_db", instance.parent.parent.parent.text, c, conn)

    def open_theme_dialog(self):
        self.theme_dialog = create_dialog(
            "Change Theme",
            [
                MDFlatButton(
                    text="Dark Theme", on_release=lambda x: self.change_theme("Dark")
                ),
                MDRaisedButton(
                    text="Light Theme",
                    on_release=lambda x: self.change_theme("Light"),
                ),
            ],
        )
        self.theme_dialog.open()

    def change_theme(self, theme):
        self.theme_cls.theme_style = theme
        self.theme_dialog.dismiss()
        with open("theme.json", "r") as f:
            data = json.load(f)
            data["theme"] = theme
        with open("theme.json", "w") as f:
            json.dump(data, f)

    def open_dialog(self):
        self.dialog = create_dialog(
            "Add A New Task:",
            [
                MDFlatButton(
                    text="Cancel",
                    on_release=self.close_dialog,
                ),
                MDRaisedButton(
                    text="Add",
                    on_release=self.add_task,
                ),
            ],
            type="custom",
            content_cls=DialogContent(),
        )

        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def close_edit_dialog(self, *args):
        self.edit_dialog.dismiss()

    def add_task(self, *args):
        self.root.ids.no_task_label.pos_hint = {"center_x": 2}
        self.dialog.dismiss()
        add_record("todo_db", self.dialog.content_cls.ids.add_task_text.text, c, conn)
        task = OneLineAvatarIconListItem(
            text=f"{self.dialog.content_cls.ids.add_task_text.text}"
        )
        self.custom_checkbox = LeftCheckbox()
        task.add_widget(self.custom_checkbox)
        btn_two = MDIconButton(icon="pencil", on_release=self.edit)
        btn_one = MDIconButton(icon="delete", on_release=self.delete)
        container = Container()
        container.add_widget(btn_one)
        container.add_widget(btn_two)
        task.add_widget(container)
        self.root.ids.rv.add_widget(task)


# Runnning the app
if __name__ == "__main__":
    TODO_List_App().run()