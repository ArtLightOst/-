from time import monotonic
from re import findall
import Config
from PySimpleGUI import Multiline, InputText, Button, Col, Window


def timing_of_method_execution(function):
    def wrapper(*args):
        start_time = monotonic()
        function(*args)
        print(monotonic() - start_time)
        return
    return wrapper


def search_for_group_domens(list_references: str) -> list[str] | None:
    result = findall(r"https://vk.com/(.*)", list_references)
    return [x.replace(Config.DOMEN_VK, '') for x in result] if result else None


layout_left = [
    [Multiline(tooltip = 'Вставьте ссылки на страницы',
               key = '-GROUPS_REFERENCES-',
               right_click_menu = ['', ['Скопировать', 'Вставить', 'Выделить всё', 'Вырезать']],
               pad = (10, 10),
               size = (45, 5),
               font = ('roman', 16, 'normal'))],

    [InputText(tooltip = 'Вставьте ключевое слово',
               key = '-KEYWORD-',
               pad = (10, 10),
               font = ('roman', 16, 'normal'))],

    [Button(button_text = 'Получить данные',
            pad = (10, 10),
            font = ('roman', 16, 'normal'),
            key = '-REQUEST_BUTTON-')],
]
layout_middle = [
    [Button(button_text = 'От какой даты',
            pad = (10, 5),
            font = ('roman', 16, 'normal'),
            size = (15, 2),
            key = '-LEFT_DATE-')],

    [InputText(readonly = True,
               key = '-LEFT_DATE_DISPLAY-',
               size = (22, 2),
               pad = (10, 5),
               justification = 'center')]
]
layout_right = [
    [Button(button_text = 'До какой даты',
            pad = (10, 5),
            font = ('roman', 16, 'normal'),
            size = (15, 2),
            key = '-RIGHT_DATE-')],

    [InputText(readonly = True,
               key = '-RIGHT_DATE_DISPLAY-',
               size = (22, 2),
               pad = (10, 5),
               justification = 'center')]

]
layout = [
    [Col(layout_left,
         vertical_alignment = 'top'),
     Col(layout_middle,
         vertical_alignment = 'top'),
     Col(layout_right,
         vertical_alignment = 'top')]

]

main_window = Window(title = 'Парсер Вконтакте',
                     layout = layout,
                     margins = (10, 10),
                     resizable = False,
                     finalize = True)
