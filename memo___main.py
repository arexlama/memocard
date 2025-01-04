import json
from random import choice, shuffle
from time import sleep
from PyQt5.QtWidgets import QApplication


app = QApplication([])

from memo___app import *
from memo___card_layout import *

answers = 0
answers_got_right = 0


class Question:
    def __init__(self, obj):
        self.question = obj['q']
        self.answer = obj['a']
        self.wrong_answer1 = obj['w1']
        self.wrong_answer2 = obj['w2']
        self.wrong_answer3 = obj['w3']
        # self.isAsking = False
        # self.count_asked = obj.get('ca', 0)
        # self.count_right = obj.get('cr', 0)

    def serialize(self):
        return {
            'q': self.question,
            'a': self.answer,
            'w1': self.wrong_answer1,
            'w2': self.wrong_answer2,
            'w3': self.wrong_answer3,
            # 'ca': self.count_asked,
            # 'cr': self.count_right
            }

    @staticmethod
    def got_right():
        global answers, answers_got_right
        answers += 1
        answers_got_right += 1

    @staticmethod
    def got_wrong():
        global answers
        answers += 1

popup = QMessageBox()

radio_buttons = [rb_ans1, rb_ans2, rb_ans3, rb_ans4]
questions = []

with open('memo___questions', 'r', encoding="utf-8") as qs:
    records = json.loads(qs.read())
    for record in records:
        questions.append(Question(record))

def new_questions():
    global current_question
    current_question = choice(questions)
    lb_question.setText(current_question.question)
    lb_right_answer.setText(current_question.answer)

    shuffle(radio_buttons)

    radio_buttons[0].setText(current_question.answer)
    radio_buttons[1].setText(current_question.wrong_answer1)
    radio_buttons[2].setText(current_question.wrong_answer2)
    radio_buttons[3].setText(current_question.wrong_answer3)


new_questions()

def check_result():
    RadioGroup.setExclusive(False)
    answer = [x for x in radio_buttons if x.isChecked()]
    if not len(answer):
        current_question.got_wrong()
        lb_result.setText("Не вірно!")
        return
    answer = answer[0]
    answer.setChecked(False)
    RadioGroup.setExclusive(True)
    if answer.text() == current_question.answer:
        current_question.got_right()
        lb_result.setText("Вірно!")
        return
    current_question.got_wrong()
    lb_result.setText("Не вірно!")

def click_ok():

    match btn_next.text():
        case "Відповісти":
            check_result()
            gb_question.hide()
            gb_answer.show()
            btn_next.setText("Наступне питання")

        case "Наступне питання":
            new_questions()
            gb_question.show()
            gb_answer.hide()
            btn_next.setText("Відповісти")

def eep():
    window.hide()
    sleep(60 * sp_rest.value())
    window.show()

def menu_generation():
    global answers, answers_got_right
    window.hide()
    display_answers = f'Разів відповіли: {answers}'
    display_answers_right = f'Вірних відповідей: {answers_got_right}'
    ratio = answers_got_right / answers if answers else 0
    lb_statistic.setText(display_answers + '\n' + display_answers_right + '\n' + f'Успішність: {ratio:.2%}' + '\n')
    # answers = sum([x.count_asked for x in questions])
    # answers_got_right = sum([x.count_right for x in questions])
    menu_win.show()

def back_menu():
    window.show()
    menu_win.hide()
    
def clear_lines():
    le_question.clear()
    le_right_ans.clear()
    le_wrong_ans1.clear()
    le_wrong_ans2.clear()
    le_wrong_ans3.clear()

def add_question():
    questions.append(Question({
        "q": le_question.text(),
        "a": le_right_ans.text(), 
        "w1": le_wrong_ans1.text(),
        "w2": le_wrong_ans2.text(),
        "w3": le_wrong_ans3.text()
    }))
    save_questions()
    clear_lines()
    popup.information(menu_win, 'Success', 'Question added')

def save_questions():
    with open('memo___questions', 'w') as qs:
        qs_list = [x.serialize() for x in questions]
        qs.write(json.dumps(qs_list))

btn_next.clicked.connect(click_ok)
btn_rest.clicked.connect(eep)
btn_menu.clicked.connect(menu_generation)
btn_back.clicked.connect(back_menu)
btn_clear.clicked.connect(clear_lines)
btn_add_question.clicked.connect(add_question)

window.show()
app.exec()
