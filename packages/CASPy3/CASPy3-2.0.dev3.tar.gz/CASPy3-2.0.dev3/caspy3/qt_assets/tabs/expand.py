from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QCursor
from PyQt5.uic import loadUi

from worker import CASWorker

class ExpandTab(QWidget):
    display_name = "Expand"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/expand.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.ExpExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.expand_exp()
                        return True

        return super(ExpandTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.ExpPrev.clicked.connect(self.prev_expand_exp)
        self.ExpCalc.clicked.connect(self.expand_exp)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        self.ExpOut.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
            self.main_window.latex_text = ""
        else:
            self.main_window.latex_text = input_dict["latex"]
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.ExpOut.setText(self.main_window.exact_ans)

    def prev_expand_exp(self):
        self.ExpOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        self.WorkerCAS = CASWorker("prev_expand_exp", [
            self.ExpExp.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def expand_exp(self):
        self.ExpOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        self.WorkerCAS = CASWorker("expand_exp", [
            self.ExpExp.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)