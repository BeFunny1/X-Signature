import json

from dataclasses import dataclass
from json import JSONDecodeError
from typing import List, Dict

from PyQt5 import QtCore, QtWidgets


@dataclass
class Geometry:
    x: int
    y: int
    width: int
    height: int


class Window:
    def __init__(self, trigger_for_button_click) -> None:
        self.central_widget: QtWidgets.QWidget = None
        self.request_method_choices: QtWidgets.QComboBox = None
        self.lines_edits: Dict[str, QtWidgets.QLineEdit] = {}
        self.texts_edits: Dict[str, QtWidgets.QTextEdit] = {}
        self.generate_button: QtWidgets.QPushButton = None
        self.x_datetime_flag: QtWidgets.QRadioButton = None
        self.error_message: QtWidgets.QErrorMessage = None
        self.trigger_for_button_click = trigger_for_button_click

    def create_window(self, main_window: QtWidgets.QMainWindow) -> None:
        self.central_widget = QtWidgets.QWidget(main_window)
        main_window.setFixedSize(400, 625)
        main_window.setWindowTitle('X-Signature Generator')
        main_window.setCentralWidget(self.central_widget)

        labels_data = [
            {'geometry': Geometry(20, 20, 101, 16), 'text': 'API_SECRET'},
            {'geometry': Geometry(120, 60, 131, 16), 'text': 'Request to:'},
            {'geometry': Geometry(50, 80, 55, 16), 'text': 'Method'},
            {'geometry': Geometry(180, 80, 131, 16), 'text': 'Canonical URL:'},
            {'geometry': Geometry(160, 150, 171, 16), 'text': 'Example: /api/auth/login'},
            {'geometry': Geometry(30, 180, 141, 16), 'text': 'Query-params(json):'},
            {'geometry': Geometry(30, 300, 141, 16), 'text': 'Headers-params(json):'},
            {'geometry': Geometry(20, 530, 71, 16), 'text': 'X-Datetime:'},
            {'geometry': Geometry(20, 560, 81, 16), 'text': 'X-Signature:'},
        ]
        for label_data in labels_data:
            self._create_label(
                parent=self.central_widget,
                geometry=label_data['geometry'],
                text=label_data['text']
            )

        combo_box_data = ['GET', 'POST', 'PUT', 'DELETE']
        self.request_method_choices = self._create_combo_box(
            parent=self.central_widget,
            geometry=Geometry(30, 100, 91, 41),
            items=combo_box_data
        )

        lines_edits_data = [
            {'key': 'API_SECRET', 'geometry': Geometry(130, 10, 241, 41)},
            {'key': 'canonical_url', 'geometry': Geometry(130, 100, 241, 41)},
            {'key': 'x-datetime', 'geometry': Geometry(100, 530, 271, 22)},
            {'key': 'x-signature', 'geometry': Geometry(100, 560, 271, 22)},
        ]
        for line_edit_data in lines_edits_data:
            self.lines_edits[line_edit_data['key']] = self._create_line_edit(
                parent=self.central_widget,
                geometry=line_edit_data['geometry']
            )

        texts_edits_data = [
            {'key': 'query', 'geometry': Geometry(30, 200, 341, 87)},
            {'key': 'headers', 'geometry': Geometry(30, 320, 341, 87)},
        ]
        for text_edit_data in texts_edits_data:
            self.texts_edits[text_edit_data['key']] = self._create_text_edit(
                parent=self.central_widget,
                geometry=text_edit_data['geometry']
            )

        self.x_datetime_flag = self._create_radio_button(
            parent=self.central_widget,
            geometry=Geometry(120, 420, 131, 20),
            text='With X-Datetime:'
        )

        self.generate_button = self._create_push_button(
            parent=self.central_widget,
            geometry=Geometry(80, 450, 221, 61),
            text='Generate',
            method_for_connect=self.transfer_data
        )

        self.error_message = QtWidgets.QErrorMessage()

    def output_headers(self, x_datetime: str, x_signature: str) -> None:
        self.lines_edits['x-datetime'].setText(x_datetime)
        self.lines_edits['x-signature'].setText(x_signature)

    def transfer_data(self) -> None:
        data = self.collect_all_data()
        # If returns error
        if not data:
            return
        self.trigger_for_button_click(data, self.output_headers)

    def collect_all_data(self) -> Dict[str, str]:
        query, headers = {}, {}
        try:
            query = json.loads(self.texts_edits['query'].toPlainText()) \
                if self.texts_edits['query'].toPlainText() \
                else query
            headers = json.loads(self.texts_edits['headers'].toPlainText()) \
                if self.texts_edits['headers'].toPlainText() \
                else headers
        except JSONDecodeError as err:
            self.show_error_message(str(err))
            return
        api_secret = self.lines_edits['API_SECRET'].text()
        method = self.request_method_choices.currentText()
        url = self.lines_edits['canonical_url'].text()
        with_x_datetime = self.x_datetime_flag.isChecked()
        return dict(
            api_secret=api_secret,
            method=method,
            url=url,
            query=query,
            headers=headers,
            with_x_datetime=with_x_datetime
        )

    def show_error_message(self, message: str) -> None:
        self.error_message.showMessage(message)

    @staticmethod
    def _create_label(parent: QtWidgets.QWidget, geometry: Geometry, text: str) -> QtWidgets.QLabel:
        label = QtWidgets.QLabel(parent)
        label.setGeometry(QtCore.QRect(geometry.x, geometry.y, geometry.width, geometry.height))
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText(text)
        return label

    @staticmethod
    def _create_combo_box(parent: QtWidgets.QWidget, geometry: Geometry, items: List[str]):
        combo_box = QtWidgets.QComboBox(parent)
        combo_box.setGeometry(QtCore.QRect(geometry.x, geometry.y, geometry.width, geometry.height))
        combo_box.addItems(items)
        return combo_box

    @staticmethod
    def _create_line_edit(parent: QtWidgets.QWidget, geometry: Geometry):
        line_edit = QtWidgets.QLineEdit(parent)
        line_edit.setGeometry(QtCore.QRect(geometry.x, geometry.y, geometry.width, geometry.height))
        return line_edit

    @staticmethod
    def _create_text_edit(parent: QtWidgets.QWidget, geometry: Geometry):
        text_edit = QtWidgets.QTextEdit(parent)
        text_edit.setGeometry(QtCore.QRect(geometry.x, geometry.y, geometry.width, geometry.height))
        return text_edit

    @staticmethod
    def _create_push_button(parent: QtWidgets.QWidget, geometry: Geometry, text: str, method_for_connect):
        push_button = QtWidgets.QPushButton(parent)
        push_button.setGeometry(QtCore.QRect(geometry.x, geometry.y, geometry.width, geometry.height))
        push_button.setText(text)
        push_button.clicked.connect(method_for_connect)
        return push_button

    @staticmethod
    def _create_radio_button(parent: QtWidgets.QWidget, geometry: Geometry, text: str, checked: bool = True):
        radio_button = QtWidgets.QRadioButton(parent)
        radio_button.setGeometry(QtCore.QRect(geometry.x, geometry.y, geometry.width, geometry.height))
        radio_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        radio_button.setChecked(checked)
        radio_button.setText(text)
        return radio_button


if __name__ == "__main__":
    pass
