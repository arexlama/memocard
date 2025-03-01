from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout

app = QApplication([])

import json


# notes = {
#     "Ласкаво просимо" : {
#         "текст" : "Це найкращий додаток для заміток у світі",
#         "теги" : ["добро" ,"інструкція"]
#     }
# }

# with open ("notes_data.json", "w", encoding="utf-8") as file:
#     json.dump(notes, file, ensure_ascii=False, indent=4)
with open("notes_data.json", "r", encoding="utf-8") as file:
    notes = json.load(file)

# window
main_window = QWidget()
main_window.resize(900, 600)
main_window.setWindowTitle("Розумні додатки")

# віджети вікна програми

list_notes = QListWidget()
list_tags = QListWidget()

list_notes.addItems(notes)

lb_list_notes = QLabel("Список заміток")
lb_list_tags = QLabel("Список тегів")

btn_note_create = QPushButton("Створити замітку")
btn_note_del = QPushButton("Видалити замітку")
btn_note_save = QPushButton("Зберегти замітку")

le_field_tag = QLineEdit(" ")
le_field_tag.setPlaceholderText("Введіть тег")
te_text = QTextEdit()

btn_tag_add = QPushButton("Додати тег")
btn_tag_del = QPushButton("Видалити тег")
btn_tag_search = QPushButton("Шукати замітку по тегу")

# розташування віджетів на макетах

layout_notes = QHBoxLayout()

col_left = QVBoxLayout()
col_left.addWidget(te_text)

col_right = QVBoxLayout()
col_right.addWidget(lb_list_notes)
col_right.addWidget(list_notes)

row_upper_right = QHBoxLayout()
row_upper_right.addWidget(btn_note_create)
row_upper_right.addWidget(btn_note_del)
row_upper_right_down = QHBoxLayout()
row_upper_right_down.addWidget(btn_note_save)

col_right.addLayout(row_upper_right)
col_right.addLayout(row_upper_right_down)

col_right.addWidget(lb_list_tags)
col_right.addWidget(list_tags)
col_right.addWidget(le_field_tag)

row_lower_right = QHBoxLayout()
row_lower_right.addWidget(btn_tag_add)
row_lower_right.addWidget(btn_tag_del)

#####

col_right.addLayout(row_lower_right)
col_right.addWidget(btn_tag_search)

layout_notes.addLayout(col_left, stretch=2)
layout_notes.addLayout(col_right, stretch=1)

main_window.setLayout(layout_notes)


def dump():
    with open('notes_data.json', 'w', encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)


def get_note():
    keys = list_notes.selectedItems()
    if keys:
        return keys[0].text()


def show_note():
    key = list_notes.selectedItems()[0].text()
    # print(key)
    te_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])


def add_note():
    note_name, ok = QInputDialog().getText(main_window, 'Додати замітку', 'Назва замітки:')

    if ok and note_name:
        notes[note_name] = {"текст": '', 'теги': []}
        list_notes.addItem(note_name)

    if ln := len(notes):
        list_notes.setCurrentRow(ln - 1)


def del_note():
    key = get_note()

    if key is not None:
        te_text.clear()
        list_tags.clear()
        list_notes.clear()
        del notes[key]
        list_notes.addItems(notes)

    dump()


def save_note():
    key = get_note()

    if key is not None:
        notes[key]['текст'] = te_text.toPlainText()

    dump()


def add_tag():
    tag = le_field_tag.text()
    list_tags.addItem(tag)
    key = get_note()


list_notes.itemClicked.connect(show_note)
btn_note_create.clicked.connect(add_note)
btn_note_del.clicked.connect(del_note)
btn_note_save.clicked.connect(save_note)
btn_tag_add.clicked.connect(add_tag)

main_window.show()

app.exec_()