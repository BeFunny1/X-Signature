import sys
from typing import Dict

from PyQt5 import QtWidgets

from window import Window
from logic import XSignatureGenerator


def make_answer(data: Dict[str, str], func_for_display_answer):
    generator = XSignatureGenerator()
    x_datetime, x_signature = generator.generate_headers(
        api_secret_key=data['api_secret'],
        method=data['method'],
        url=data['url'],
        query_params=data['query'],
        headers=data['headers'],
        with_x_datetime=data['with_x_datetime']
    )
    func_for_display_answer(x_datetime, x_signature)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    window = Window(make_answer)
    window.create_window(main_window)
    main_window.show()
    sys.exit(app.exec_())
