from PyQt5.QtWidgets import QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QTextCursor, QTextBlockFormat, QTextCharFormat


class ChatDisplay(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Arial", 12))

    def append_left(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

        block_format = QTextBlockFormat()
        char_format = QTextCharFormat() 

        block_format.setAlignment(Qt.AlignLeft)
        char_format.setBackground(QColor("#FFFFFF"))
        char_format.setForeground(QColor("black"))

        block_format.setTopMargin(10)
        block_format.setBottomMargin(10)
        block_format.setLeftMargin(20)
        block_format.setRightMargin(20)

        cursor.insertBlock(block_format)
        cursor.setCharFormat(char_format)
        cursor.insertHtml(text)

        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def append_right(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

        block_format = QTextBlockFormat()
        char_format = QTextCharFormat()

        block_format.setAlignment(Qt.AlignRight)
        char_format.setBackground(QColor("#DCF8C6"))
        char_format.setForeground(QColor("black"))

        block_format.setTopMargin(10)
        block_format.setBottomMargin(10)
        block_format.setLeftMargin(20)
        block_format.setRightMargin(20)

        cursor.insertBlock(block_format)
        cursor.setCharFormat(char_format)
        cursor.insertHtml(text)

        self.setTextCursor(cursor)
        self.ensureCursorVisible()


class InputBox(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("在这里输入您的问题...")
        self.setFont(QFont("Arial", 12))


class SendButton(QPushButton):
    def __init__(self):
        super().__init__("发送")
        self.setFont(QFont("Arial", 12))


class LoadingLabel(QLabel):
    def __init__(self):
        super().__init__("正在加载...")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color: gray; font-size: 14px;")
        self.hide()