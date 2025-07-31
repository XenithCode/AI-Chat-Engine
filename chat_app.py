from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QMessageBox, QShortcut, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, pyqtSlot, QTimer, QPropertyAnimation
from PyQt5.QtGui import QFont, QTextCursor, QColor, QTextBlockFormat, QTextCharFormat, QKeySequence, QPixmap
from chat_thread import ChatThread


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.zhipuai_api_key = 'sk-97264bca492046bbae9999747b1a3188'
        self.conversation_history = []  # 对话历史
        self.current_context = []  # 当前上下文
        self.is_streaming = False  # 流式回复状态
        self.is_dark_mode = False  # 当前主题模式
        self.initUI()
        self.setupShortcuts()

    def initUI(self):
        self.setWindowTitle("AI 聊天窗口")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet(self.get_window_style())

        layout = QVBoxLayout()

        # 主题与历史按钮
        theme_layout = QHBoxLayout()
        self.theme_button = QPushButton("黑夜模式")
        self.theme_button.setFont(QFont("Segoe UI", 12))
        self.theme_button.clicked.connect(self.toggle_theme)

        self.history_button = QPushButton("查看历史记录")
        self.history_button.setFont(QFont("Segoe UI", 12))
        self.history_button.clicked.connect(self.show_history)

        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_button)
        theme_layout.addWidget(self.history_button)

        # 聊天显示框
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 12))
        self.update_chat_display_style()
        self.chat_display.setMinimumHeight(600)

        # 加载提示
        self.loading_label = QLabel("正在加载...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet(self.get_loading_style())
        self.loading_label.hide()

        # 输入框
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("在这里输入您的问题...")
        self.input_box.setFont(QFont("Segoe UI", 12))
        self.input_box.setStyleSheet(self.get_input_style())
        self.input_box.returnPressed.connect(self.send_message)

        # 发送按钮
        self.send_button = QPushButton("发送")
        self.send_button.setFont(QFont("Segoe UI", 12))
        self.send_button.setStyleSheet(self.get_send_button_style())
        self.send_button.clicked.connect(self.send_message)

        layout.addLayout(theme_layout)
        layout.addWidget(self.chat_display)
        layout.addWidget(self.loading_label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def setupShortcuts(self):
        self.send_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.send_shortcut.activated.connect(self.send_message)

    def append_chat_text(self, text, is_user=False, format_text=True):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.chat_display.setTextCursor(cursor)

        block_format = QTextBlockFormat()
        char_format = QTextCharFormat()

        if is_user:
            block_format.setAlignment(Qt.AlignRight)
            char_format.setBackground(QColor(self.get_user_bubble_color()))
            char_format.setForeground(QColor(self.get_text_color(is_user=True)))
        else:
            block_format.setAlignment(Qt.AlignLeft)
            char_format.setBackground(QColor(self.get_assistant_bubble_color()))
            char_format.setForeground(QColor(self.get_text_color()))

        block_format.setTopMargin(8)
        block_format.setBottomMargin(8)
        block_format.setLeftMargin(15)
        block_format.setRightMargin(15)

        cursor.insertBlock(block_format)
        cursor.setCharFormat(char_format)
        cursor.insertText(text)

        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()

    @pyqtSlot()
    def send_message(self):
        user_input = self.input_box.text().strip()
        if user_input:
            self.is_streaming = False
            self.append_chat_text(f"用户: {user_input}", is_user=True, format_text=True)
            self.conversation_history.append({"role": "user", "content": user_input})
            self.current_context = self.conversation_history[-2:]  # 仅发送最近两轮上下文
            self.chat_thread = ChatThread(self.zhipuai_api_key, self.current_context)
            self.chat_thread.response_signal.connect(self.update_chat_display)
            self.chat_thread.error_signal.connect(self.display_error)
            self.chat_thread.finalize_signal.connect(self.finalize_response)
            self.chat_thread.start_signal.connect(self.show_loading)
            self.chat_thread.start()
            self.input_box.clear()
            self.input_box.setEnabled(False)

    @pyqtSlot(str)
    def update_chat_display(self, content):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.chat_display.setTextCursor(cursor)

        if not self.is_streaming:
            self.append_chat_text("助手:", is_user=False, format_text=True)
            self.is_streaming = True

        cursor.insertText(content)
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    @pyqtSlot(str)
    def display_error(self, error_message):
        self.append_chat_text(f"错误: {error_message}", is_user=False)
        self.input_box.setEnabled(True)
        self.loading_label.hide()

    @pyqtSlot()
    def finalize_response(self):
        self.input_box.setEnabled(True)
        self.is_streaming = False
        self.loading_label.hide()

    @pyqtSlot()
    def show_loading(self):
        self.loading_label.show()
        self.opacity_effect = QGraphicsOpacityEffect()
        self.loading_label.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_button.setText("白天模式" if self.is_dark_mode else "黑夜模式")
        self.update_styles()

    def update_styles(self):
        self.update_chat_display_style()
        self.input_box.setStyleSheet(self.get_input_style())
        self.send_button.setStyleSheet(self.get_send_button_style())
        self.loading_label.setStyleSheet(self.get_loading_style())
        self.setStyleSheet(self.get_window_style())

    def update_chat_display_style(self):
        bg_color = "#2D2D2D" if self.is_dark_mode else "#F5F5F5"
        self.chat_display.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg_color};
                border: 1px solid #CCCCCC;
                border-radius: 10px;
                padding: 10px;
            }}
        """)

    def get_input_style(self):
        bg_color = "#333333" if self.is_dark_mode else "#FFFFFF"
        text_color = self.get_text_color(is_user=True)
        border_color = "#6B6B6B" if self.is_dark_mode else "#CCCCCC"
        return f"""
            QLineEdit {{
                background-color: {bg_color};
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 15px;
                padding: 8px 16px;
                font-family: 'Segoe UI';
            }}
        """

    def get_send_button_style(self):
        bg_color = "#0078D7" if self.is_dark_mode else "#0078D7"
        hover_color = "#005BB5" if self.is_dark_mode else "#0066CC"
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 15px;
                padding: 8px 20px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    def get_loading_style(self):
        text_color = self.get_text_color()
        return f"color: {text_color}; font-size: 14px;"

    def get_window_style(self):
        bg_color = "#2D2D2D" if self.is_dark_mode else "#F5F5F5"
        return f"QWidget {{ background-color: {bg_color}; }}"

    def get_text_color(self, is_user=False):
        return "white" if self.is_dark_mode else "black"

    def get_user_bubble_color(self):
        return "#4CAF50" if self.is_dark_mode else "#4CAF50"

    def get_assistant_bubble_color(self):
        return "#404040" if self.is_dark_mode else "#E8E8E8"

    def show_history(self):
        history_text = "\n".join([f"{entry['role']}: {entry['content']}" for entry in self.conversation_history])
        QMessageBox.information(self, "对话历史记录", history_text)