import sys
import threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                            QTextEdit, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QIcon

from modules.transcriber import transcribe
from modules.searcher import web_search
from modules.llm import ask_ai
from modules.speaker import speak, stop_speaking
from modules.recorder import record_audio

class WorkerSignals(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    status = pyqtSignal(str)

class Worker(threading.Thread):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("兒童 AI 問答系統")
        self.setMinimumSize(800, 600)
        
        # 建立主視窗部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 建立主佈局
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # 標題
        title = QLabel("兒童 AI 問答系統")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 狀態顯示
        self.status_label = QLabel("準備就緒")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 錄音按鈕
        self.record_button = QPushButton("🎙️ 開始錄音")
        self.record_button.setMinimumHeight(50)
        self.record_button.clicked.connect(self.start_recording)
        layout.addWidget(self.record_button)
        
        # 問題顯示區
        self.question_display = QTextEdit()
        self.question_display.setReadOnly(True)
        self.question_display.setPlaceholderText("問題將顯示在這裡...")
        layout.addWidget(self.question_display)
        
        # 回答顯示區
        self.answer_display = QTextEdit()
        self.answer_display.setReadOnly(True)
        self.answer_display.setPlaceholderText("AI 的回答將顯示在這裡...")
        layout.addWidget(self.answer_display)
        
        # 按鈕區域
        button_layout = QHBoxLayout()
        
        self.speak_button = QPushButton("🔊 播放回答")
        self.speak_button.clicked.connect(self.speak_answer)
        self.speak_button.setEnabled(False)
        button_layout.addWidget(self.speak_button)

        self.stop_speak_button = QPushButton("⏹️ 強制停止AI說話")
        self.stop_speak_button.clicked.connect(self.force_stop_speaking)
        self.stop_speak_button.setEnabled(True)
        button_layout.addWidget(self.stop_speak_button)
        
        self.clear_button = QPushButton("🗑️ 清除")
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # 設定樣式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                color: #666;
            }
        """)

    def start_recording(self):
        self.record_button.setEnabled(False)
        self.status_label.setText("正在錄音...")
        
        # 開始錄音
        worker = Worker(record_audio, "input.wav")
        worker.signals.finished.connect(self.on_recording_finished)
        worker.signals.error.connect(self.on_error)
        worker.start()

    def on_recording_finished(self, _):
        self.status_label.setText("正在處理語音...")
        
        # 轉錄語音
        worker = Worker(transcribe, "input.wav")
        worker.signals.finished.connect(self.on_transcription_finished)
        worker.signals.error.connect(self.on_error)
        worker.start()

    def on_transcription_finished(self, question):
        if not question.strip():
            self.status_label.setText("沒有辨識到語音內容")
            self.record_button.setEnabled(True)
            return
            
        self.question_display.setText(question)
        self.status_label.setText("正在搜尋相關資訊...")
        
        # 搜尋相關資訊
        worker = Worker(web_search, question)
        worker.signals.finished.connect(lambda result: self.on_search_finished(question, result))
        worker.signals.error.connect(self.on_error)
        worker.start()

    def on_search_finished(self, question, search_result):
        self.status_label.setText("正在生成回答...")
        
        # 生成 AI 回答
        worker = Worker(ask_ai, question, search_result)
        worker.signals.finished.connect(self.on_answer_finished)
        worker.signals.error.connect(self.on_error)
        worker.start()

    def on_answer_finished(self, answer):
        self.answer_display.setText(answer)
        self.status_label.setText("回答完成！")
        self.record_button.setEnabled(True)
        self.speak_button.setEnabled(True)
        self.speak_answer()

    def speak_answer(self):
        if self.answer_display.toPlainText():
            worker = Worker(speak, self.answer_display.toPlainText())
            worker.signals.error.connect(self.on_error)
            worker.start()

    def clear_all(self):
        self.question_display.clear()
        self.answer_display.clear()
        self.status_label.setText("準備就緒")
        self.speak_button.setEnabled(False)

    def on_error(self, error_msg):
        self.status_label.setText(f"錯誤：{error_msg}")
        self.record_button.setEnabled(True)

    def force_stop_speaking(self):
        stop_speaking()
        self.status_label.setText("AI說話已強制停止！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())