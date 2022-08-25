from os.path import expanduser
from threading import Thread, active_count
from PySimpleGUI import PySimpleGUI
from pandas import DataFrame, ExcelWriter
import Tools
from SessionWithServiceKey import SessionWithServiceKey


class GUI(object):

    def __init__(self):
        self.Session = SessionWithServiceKey()
        self.left_date = tuple()
        self.right_date = tuple()
        self.data_frames: dict[str: DataFrame] = dict()
        self.window = Tools.main_window
        self.display_window = False

    def REQUEST_BUTTON_ACTION(self, values) -> None:
        self.Session.groups.clear()
        if values['-GROUPS_REFERENCES-'] and values['-KEYWORD-']:
            self.switch_element_activity(True)
            Thread(target = self.Session.get_posts_from_list_of_groups,
                   args = (values['-GROUPS_REFERENCES-'], values['-KEYWORD-'], self.left_date if self.left_date else None,
                           self.right_date if self.right_date else None),
                   daemon = True).start()
            Thread(target = self.check_for_end_of_work,
                   daemon = True).start()
        else:
            PySimpleGUI.Popup(PySimpleGUI.Text('Введите все необходимые данные').DisplayText,
                              title = 'Ошибка')

    def LEFT_DATE_ACTION(self) -> None:
        self.left_date = PySimpleGUI.popup_get_date(title = 'До какой даты',
                                                    month_names = ['Январь', 'Февраль', 'Март',
                                                                   'Апрель', 'Май', 'Июнь',
                                                                   'Июль', 'Август', 'Сентябрь',
                                                                   'Октябрь', 'Ноябрь', 'Декабрь'],
                                                    day_abbreviations = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'])
        if self.left_date:
            self.window['-LEFT_DATE_DISPLAY-'].update(f'{self.left_date[1]}.{self.left_date[0]}.{self.left_date[2]}')

    def RIGHT_DATE_ACTION(self) -> None:
        self.right_date = PySimpleGUI.popup_get_date(title = 'До какой даты',
                                                     month_names = ['Январь', 'Февраль', 'Март',
                                                                    'Апрель', 'Май', 'Июнь',
                                                                    'Июль', 'Август', 'Сентябрь',
                                                                    'Октябрь', 'Ноябрь', 'Декабрь'],
                                                     day_abbreviations = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'])
        if self.right_date:
            self.window['-RIGHT_DATE_DISPLAY-'].update(f'{self.right_date[1]}.{self.right_date[0]}.{self.right_date[2]}')

    def SELECT_ALL_ACTION(self) -> None:
        self.window['-GROUPS_REFERENCES-'].Widget.selection_clear()
        self.window['-GROUPS_REFERENCES-'].Widget.tag_add('sel', '1.0', 'end')

    def COPY_ACTION(self) -> None:
        try:
            text = self.window['-GROUPS_REFERENCES-'].Widget.selection_get()
            self.window.TKroot.clipboard_clear()
            self.window.TKroot.clipboard_append(text)
        except:
            pass

    def PASTE_ACTION(self):
        self.window['-GROUPS_REFERENCES-'].Widget.insert(PySimpleGUI.tk.INSERT, self.window.TKroot.clipboard_get() + '\n')

    def CUT_ACTION(self) -> None:
        try:
            text = self.window['-GROUPS_REFERENCES-'].Widget.selection_get()
            self.window.TKroot.clipboard_clear()
            self.window.TKroot.clipboard_append(text)
            self.window['-GROUPS_REFERENCES-'].update('')
        except:
            pass

    def create_representation_window(self):
        PySimpleGUI.theme('Default1')
        tables: list = []
        tabs: list = []
        data_for_table: list = []
        for group in self.Session.groups:
            data_for_table.clear()
            if group.error:
                PySimpleGUI.Popup(PySimpleGUI.Text(group.error).DisplayText,
                                  title = group.group_domen)
                continue
            else:
                if len(group.publications):
                    for publication in group.publications:
                        data_for_table.append([
                            str(publication.get_date()),
                            publication.get_str_time(),
                            publication.get_platform(),
                            publication.get_text(),
                            publication.get_photo_urls(),
                            publication.get_links_urls(),
                            publication.get_comments_count(),
                            publication.get_likes_count(),
                            publication.get_reposts_count(),
                            publication.get_views_count()
                        ])
                    tables.append([PySimpleGUI.Table(values =
                                                     [*data_for_table],
                                                     headings = [
                                                         'Дата',
                                                         'Время',
                                                         'Платформа устройства',
                                                         'Текст',
                                                         'Прикрепленные фото',
                                                         'Прикрепленные ссылки',
                                                         'Количество комментариев',
                                                         'Количество лайков',
                                                         'Количество репостов',
                                                         'Количество просмотров'
                                                     ],
                                                     display_row_numbers = True,
                                                     num_rows = len(group.publications),
                                                     expand_x = True,
                                                     expand_y = True,
                                                     justification = 'center',
                                                     border_width = 1,
                                                     pad = (10, 10)
                                                     )
                                   ])
                    self.data_frames[group.group_domen] = DataFrame({
                        'Дата': [x[0] for x in data_for_table],
                        'Время': [x[1] for x in data_for_table],
                        'Платформа устройства': [x[2] for x in data_for_table],
                        'Текст': [x[3] for x in data_for_table],
                        'Прикрепленные фото': [x[4] for x in data_for_table],
                        'Прикрепленные ссылки': [x[5] for x in data_for_table],
                        'Количество комментариев': [x[6] for x in data_for_table],
                        'Количество лайков': [x[7] for x in data_for_table],
                        'Количество репостов': [x[8] for x in data_for_table],
                        'Количество просмотров': [x[9] for x in data_for_table]
                    })

                    tabs.append([PySimpleGUI.Tab(title = group.group_domen,
                                                 layout = [tables[len(tables) - 1]],
                                                 expand_x = True,
                                                 expand_y = True,
                                                 pad = (10, 10)
                                                 )
                                 ])
                else:
                    continue
        tab_group = [PySimpleGUI.TabGroup(layout = tabs,
                                          tab_location = 'top',
                                          expand_x = True,
                                          expand_y = True,
                                          pad = (10, 10))]
        return PySimpleGUI.Window(title = 'Полученные данные',
                                  layout = [[PySimpleGUI.Button(button_text = 'Выгрузить в excel',
                                                                expand_x = True,
                                                                expand_y = True,
                                                                key = '-TO_EXCEL-')],
                                            tab_group],
                                  resizable = True,
                                  finalize = True)

    def representation_window_loop(self):
        if self.display_window:
            self.window.hide()
            representation_window = self.create_representation_window()
            while True:
                representation_event, representation_values = representation_window.read(timeout = 50)
                match representation_event:
                    case '-TO_EXCEL-':
                        filename = PySimpleGUI.popup_get_text(title = 'Имя файла', message = 'Выберите имя файла')
                        if filename:
                            writer = ExcelWriter(path = expanduser('~') + r'\Desktop' + '\\' + filename + '.xlsx')
                            for sheets_name in self.data_frames.keys():
                                self.data_frames[sheets_name].to_excel(writer, sheet_name = sheets_name)
                            writer.save()
                            self.data_frames.clear()
                            representation_window['-TO_EXCEL-'].update(disabled = True)
                    case PySimpleGUI.WIN_CLOSED:
                        self.display_window = False
                        representation_window.close()
                        break
            PySimpleGUI.theme('DarkBlue3')
            self.window.un_hide()

    def switch_element_activity(self, state: bool) -> None:
        self.window['-GROUPS_REFERENCES-'].update(disabled = state)
        self.window['-KEYWORD-'].update(disabled = state)
        self.window['-REQUEST_BUTTON-'].update(disabled = state)
        self.window['-LEFT_DATE-'].update(disabled = state)
        self.window['-RIGHT_DATE-'].update(disabled = state)

    def check_for_end_of_work(self) -> None:
        while active_count() > 2:
            continue
        else:
            self.switch_element_activity(False)
            self.display_window = True

    def mainloop(self) -> None:
        while True:
            event, values = self.window.read(timeout = 50)
            self.representation_window_loop()
            match event:
                case '-REQUEST_BUTTON-':
                    self.REQUEST_BUTTON_ACTION(values)
                case '-LEFT_DATE-':
                    self.LEFT_DATE_ACTION()
                case '-RIGHT_DATE-':
                    self.RIGHT_DATE_ACTION()
                case 'Выделить всё':
                    self.SELECT_ALL_ACTION()
                case 'Скопировать':
                    self.COPY_ACTION()
                case 'Вставить':
                    self.PASTE_ACTION()
                case 'Вырезать':
                    self.CUT_ACTION()
                case PySimpleGUI.WIN_CLOSED:
                    break


if __name__ == '__main__':
    example = GUI()
    example.mainloop()
