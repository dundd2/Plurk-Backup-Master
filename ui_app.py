import os
import sys
import subprocess
from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
    QEasingCurve,
    QPropertyAnimation,
    QUrl,
    QTimer,
    QSignalBlocker,
)
from PySide6.QtGui import QColor, QFont, QDesktopServices, QCursor, QTextOption
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QProgressBar,
    QCheckBox,
    QVBoxLayout,
    QWidget,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QComboBox,
)


VERSION = "v1.2.0"
GITHUB_URL = "https://github.com/dundd2"
GITHUB_OWNER = "dundd2"

TRANSLATIONS = {
    "zh-TW": {
        "window_title": "Plurk Backup - 液態玻璃 UI",
        "hero_title": "Plurk Backup 控制中心",
        "hero_subtitle": "以液態玻璃波紋包裹備份旅程，兼顧優雅與效率",
        "hero_description": "在視覺化控制台中檢查 API 金鑰、彙整多個使用者並即時掌握執行訊息。",
        "chips": ["即時日誌流", "多帳號同啟", "玻璃霧面質感"],
        "tips_title": "使用小提醒",
        "tips_content": "・請先於 .env 案中儲存 API 金鑰\n・多個帳號以空白分隔輸入\n・備份成功後可自動開啟輸出資料夾",
        "form_label_consumer_key": "Consumer Key",
        "form_label_consumer_secret": "Consumer Secret",
        "form_label_access_token": "Access Token",
        "form_label_access_token_secret": "Access Token Secret",
        "form_label_users": "Plurk 使用者",
        "form_helper": "帳號支援一次輸入多位，使用空格分隔即可。",
        "placeholder_users": "輸入欲備份的使用者帳號，以空白分隔",
        "option_auto_open": "備份完成後自動開啟資料夾",
        "button_reset": "重設欄位",
        "button_start": "開始備份",
        "status_idle": "等待操作…",
        "status_running": "正在啟動備份程序…",
        "status_success": "備份完成！",
        "status_warning": "備份結束（請檢查訊息）",
        "status_warning_detected": "偵測到警告訊息，請查看日誌。",
        "status_reset": "欄位已重設，準備開始新的備份。",
        "dialog_in_progress_title": "備份進行中",
        "dialog_in_progress_body": "目前備份尚未完成，請稍候。",
        "dialog_missing_user_title": "缺少資訊",
        "dialog_missing_user_body": "請至少輸入一個 Plurk 使用者名稱。",
        "dialog_missing_keys_title": "缺少金鑰",
        "dialog_missing_keys_body": "請填寫所有 Plurk API 金鑰與權杖欄位。",
        "log_header": "備份日誌",
        "log_missing_folder": "找不到資料夾：{path}",
        "language_label": "介面語言",
        "github_link": 'GitHub：<a href="{url}">{owner}</a>',
        "version_label": "版本：{version}",
    },
    "en": {
        "window_title": "Plurk Backup - Liquid Glass UI",
        "hero_title": "Plurk Backup Control Center",
        "hero_subtitle": "Wrap your backup journey in liquid glass waves for elegance and speed.",
        "hero_description": "Verify API keys, orchestrate multi-user runs, and watch live updates in one console.",
        "chips": ["Live Log Stream", "Multi-account Launch", "Glassmorphism Finish"],
        "tips_title": "Quick Reminders",
        "tips_content": "• Store your API keys in the .env file first\n• Separate multiple usernames with spaces\n• Auto-open the output folder after a successful run",
        "form_label_consumer_key": "Consumer Key",
        "form_label_consumer_secret": "Consumer Secret",
        "form_label_access_token": "Access Token",
        "form_label_access_token_secret": "Access Token Secret",
        "form_label_users": "Plurk Users",
        "form_helper": "You can enter multiple accounts at once, just separate them with spaces.",
        "placeholder_users": "Enter the Plurk usernames to back up, separated by spaces",
        "option_auto_open": "Open the folder automatically when the backup completes",
        "button_reset": "Reset Form",
        "button_start": "Start Backup",
        "status_idle": "Waiting for your next action…",
        "status_running": "Launching backup flow…",
        "status_success": "Backup complete!",
        "status_warning": "Backup finished (please review the log).",
        "status_warning_detected": "Warnings detected—check the log for details.",
        "status_reset": "Form cleared. Ready for a fresh backup.",
        "dialog_in_progress_title": "Backup in Progress",
        "dialog_in_progress_body": "A backup is already running. Please wait for it to finish.",
        "dialog_missing_user_title": "Missing Information",
        "dialog_missing_user_body": "Please enter at least one Plurk username.",
        "dialog_missing_keys_title": "Missing Keys",
        "dialog_missing_keys_body": "Please complete all Plurk API key and token fields.",
        "log_header": "Backup Log",
        "log_missing_folder": "Unable to locate folder: {path}",
        "language_label": "Language",
        "github_link": 'GitHub: <a href="{url}">{owner}</a>',
        "version_label": "Version: {version}",
    },
}


class BackupWorker(QThread):
    output = Signal(str)
    finished = Signal(int)

    def __init__(self, usernames, credentials, parent=None):
        super().__init__(parent)
        self.usernames = usernames
        self.credentials = credentials

    def run(self):
        command = [sys.executable, "main.py", *self.usernames]
        env = os.environ.copy()
        env.update(self.credentials)

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
            )

            for line in iter(process.stdout.readline, ""):
                cleaned = line.rstrip()
                if cleaned:
                    self.output.emit(cleaned)
            process.stdout.close()
            return_code = process.wait()
            self.finished.emit(return_code)
        except FileNotFoundError:
            self.output.emit("Unable to locate main.py. Please make sure you are running the UI from the project root.")
            self.finished.emit(-1)
        except Exception as exc:
            self.output.emit(f"Unexpected error: {exc}")
            self.finished.emit(-1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.last_usernames = []
        self.status_animation = None
        self.current_language = "zh-TW"
        self.form_label_widgets = []
        self.chip_labels = []
        self.translations = TRANSLATIONS
        self.setWindowTitle(self.translations[self.current_language]["window_title"])
        self.setMinimumSize(960, 640)
        self.current_status_key = "status_idle"
        self._build_ui()
        self.set_language(self.current_language)
        QTimer.singleShot(0, self.update_responsive_layout)

    def _build_ui(self):
        container = QWidget(objectName="CentralWidget")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(32)

        top_bar = QHBoxLayout()
        top_bar.setSpacing(16)

        self.version_label = QLabel(objectName="VersionLabel")
        top_bar.addWidget(self.version_label)

        top_bar.addStretch(1)

        self.github_link = QLabel(objectName="GitHubLink")
        self.github_link.setTextFormat(Qt.RichText)
        self.github_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.github_link.setOpenExternalLinks(False)
        self.github_link.setCursor(QCursor(Qt.PointingHandCursor))
        self.github_link.linkActivated.connect(self.open_link)
        top_bar.addWidget(self.github_link)

        self.language_label = QLabel(objectName="LanguageLabel")
        top_bar.addWidget(self.language_label)

        self.language_combo = QComboBox()
        self.language_combo.addItem("繁體中文", "zh-TW")
        self.language_combo.addItem("English", "en")
        initial_index = 0 if self.current_language == "zh-TW" else 1
        self.language_combo.setCurrentIndex(initial_index)
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        top_bar.addWidget(self.language_combo)

        layout.addLayout(top_bar)

        self.hero_card = QFrame(objectName="HeroCard")
        hero_layout = QHBoxLayout(self.hero_card)
        hero_layout.setSpacing(32)
        hero_layout.setContentsMargins(36, 32, 36, 32)

        hero_text_layout = QVBoxLayout()
        hero_text_layout.setSpacing(16)

        self.title_label = QLabel(objectName="TitleLabel")
        self.title_label.setFont(QFont("Noto Sans TC", 30, QFont.Bold))
        hero_text_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel(objectName="SubtitleLabel")
        self.subtitle_label.setWordWrap(True)
        hero_text_layout.addWidget(self.subtitle_label)

        self.hero_description = QLabel(objectName="HeroDescription")
        self.hero_description.setWordWrap(True)
        hero_text_layout.addWidget(self.hero_description)

        chip_row = QHBoxLayout()
        chip_row.setSpacing(12)
        for _ in range(3):
            chip = QLabel(objectName="GlassChip")
            self.chip_labels.append(chip)
            chip_row.addWidget(chip)
        chip_row.addStretch(1)
        hero_text_layout.addLayout(chip_row)

        hero_layout.addLayout(hero_text_layout, stretch=2)

        self.quote_card = QFrame(objectName="TipsCard")
        tips_layout = QVBoxLayout(self.quote_card)
        tips_layout.setSpacing(12)
        tips_layout.setContentsMargins(20, 20, 20, 20)

        self.tips_title = QLabel(objectName="TipsTitle")
        tips_layout.addWidget(self.tips_title)

        self.tips_content = QLabel(objectName="TipsContent")
        self.tips_content.setWordWrap(True)
        tips_layout.addWidget(self.tips_content)
        tips_layout.addStretch(1)

        hero_layout.addWidget(self.quote_card, stretch=1)
        layout.addWidget(self.hero_card)

        self.glass_card = QFrame(objectName="GlassCard")
        card_layout = QVBoxLayout(self.glass_card)
        card_layout.setSpacing(24)
        card_layout.setContentsMargins(32, 32, 32, 32)

        form_wrapper = QWidget()
        form_layout = QGridLayout(form_wrapper)
        form_layout.setHorizontalSpacing(18)
        form_layout.setVerticalSpacing(18)

        self.consumer_key = QLineEdit(os.getenv("CONSUMER_KEY", ""))
        self.consumer_secret = QLineEdit(os.getenv("CONSUMER_SECRET", ""))
        self.access_token = QLineEdit(os.getenv("ACCESS_TOKEN", ""))
        self.access_token_secret = QLineEdit(os.getenv("ACCESS_TOKEN_SECRET", ""))

        for edit in (self.consumer_secret, self.access_token, self.access_token_secret):
            edit.setEchoMode(QLineEdit.Password)

        self.usernames_edit = QLineEdit()
        self.usernames_edit.setPlaceholderText(
            self.translations[self.current_language]["placeholder_users"]
        )

        label_keys = [
            "form_label_consumer_key",
            "form_label_consumer_secret",
            "form_label_access_token",
            "form_label_access_token_secret",
            "form_label_users",
        ]
        form_inputs = [
            self.consumer_key,
            self.consumer_secret,
            self.access_token,
            self.access_token_secret,
            self.usernames_edit,
        ]

        for row, (key, widget) in enumerate(zip(label_keys, form_inputs)):
            label = QLabel(objectName="FormLabel")
            self.form_label_widgets.append((label, key))
            form_layout.addWidget(label, row, 0)
            form_layout.addWidget(widget, row, 1)

        self.form_helper = QLabel(objectName="FormHelper")
        self.form_helper.setWordWrap(True)
        form_layout.addWidget(self.form_helper, len(label_keys), 0, 1, 2)

        card_layout.addWidget(form_wrapper)

        option_row = QHBoxLayout()
        option_row.setSpacing(12)
        self.open_folder_checkbox = QCheckBox(
            self.translations[self.current_language]["option_auto_open"]
        )
        option_row.addWidget(self.open_folder_checkbox)
        option_row.addStretch(1)
        card_layout.addLayout(option_row)

        button_row = QHBoxLayout()
        button_row.setSpacing(16)
        button_row.addStretch(1)
        self.clear_button = QPushButton(
            self.translations[self.current_language]["button_reset"]
        )
        self.clear_button.clicked.connect(self.reset_form)
        button_row.addWidget(self.clear_button)
        self.start_button = QPushButton(
            self.translations[self.current_language]["button_start"]
        )
        self.start_button.clicked.connect(self.start_backup)
        button_row.addWidget(self.start_button)
        button_row.addStretch(1)
        card_layout.addLayout(button_row)

        self.status_label = QLabel(objectName="StatusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setProperty("state", "idle")
        self.status_effect = QGraphicsOpacityEffect(self.status_label)
        self.status_label.setGraphicsEffect(self.status_effect)
        card_layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("ProgressBar")
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        card_layout.addWidget(self.progress_bar)

        layout.addWidget(self.glass_card)

        self.log_card = QFrame(objectName="LogCard")
        log_layout = QVBoxLayout(self.log_card)
        log_layout.setSpacing(16)
        log_layout.setContentsMargins(28, 28, 28, 28)

        self.log_header = QLabel(objectName="LogHeader")
        log_layout.addWidget(self.log_header)

        self.log_output = QPlainTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setObjectName("LogOutput")
        log_layout.addWidget(self.log_output)

        layout.addWidget(self.log_card)
        self.setCentralWidget(container)

        for widget, blur, offset, alpha in (
            (self.hero_card, 60, 24, 150),
            (self.glass_card, 55, 28, 180),
            (self.log_card, 45, 24, 160),
        ):
            self._apply_shadow(widget, blur, offset, alpha)

        self._apply_styles()
        self.responsive_labels = [
            self.subtitle_label,
            self.hero_description,
            self.tips_content,
        ]
        self.log_output.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        default_option = self.log_output.document().defaultTextOption()
        default_option.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.log_output.document().setDefaultTextOption(default_option)

    def _apply_shadow(self, widget, blur, offset, alpha):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, offset)
        shadow.setColor(QColor(15, 23, 42, alpha))
        widget.setGraphicsEffect(shadow)

    def _apply_styles(self):
        self.setStyleSheet(
            """
            #CentralWidget {
                background: qradialgradient(cx:0.2, cy:0.2, radius:1.0,
                    fx:0.1, fy:0.1, stop:0 rgba(94, 234, 212, 28), stop:0.4 rgba(56, 189, 248, 18),
                    stop:1 rgba(15, 23, 42, 255));
            }
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(13, 15, 35, 255), stop:0.5 rgba(32, 40, 62, 255), stop:1 rgba(10, 18, 47, 255));
            }
            #HeroCard {
                background-color: rgba(255, 255, 255, 26);
                border: 1px solid rgba(255, 255, 255, 60);
                border-radius: 28px;
            }
            #TipsCard {
                background-color: rgba(15, 23, 42, 140);
                border: 1px solid rgba(148, 163, 184, 110);
                border-radius: 22px;
            }
            #GlassCard {
                background-color: rgba(255, 255, 255, 28);
                border: 1px solid rgba(255, 255, 255, 60);
                border-radius: 28px;
            }
            #LogCard {
                background-color: rgba(15, 23, 42, 150);
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 26px;
            }
            #TitleLabel {
                color: rgba(255, 255, 255, 230);
                letter-spacing: 4px;
            }
            #SubtitleLabel {
                color: rgba(255, 255, 255, 200);
                font-size: 16px;
            }
            #HeroDescription {
                color: rgba(226, 232, 240, 200);
                font-size: 14px;
            }
            #TipsTitle {
                color: rgba(226, 232, 240, 240);
                font-size: 16px;
                font-weight: bold;
            }
            #TipsContent {
                color: rgba(226, 232, 240, 210);
                font-size: 14px;
                line-height: 22px;
            }
            QLabel {
                color: rgba(255, 255, 255, 215);
                font-size: 14px;
            }
            #FormLabel {
                font-weight: 600;
            }
            #FormHelper {
                color: rgba(226, 232, 240, 180);
                font-size: 13px;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 70);
                border: 1px solid rgba(255, 255, 255, 120);
                border-radius: 18px;
                padding: 10px 16px;
                color: #0f172a;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(137, 196, 244, 220);
                background-color: rgba(255, 255, 255, 100);
            }
            QCheckBox {
                color: rgba(226, 232, 240, 210);
                font-size: 13px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 6px;
                border: 1px solid rgba(148, 163, 184, 200);
                background: rgba(255, 255, 255, 120);
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(96, 165, 250, 240), stop:1 rgba(59, 130, 246, 220));
                border: 1px solid rgba(191, 219, 254, 200);
            }
            #GlassChip {
                background: rgba(255, 255, 255, 40);
                border: 1px solid rgba(255, 255, 255, 70);
                border-radius: 16px;
                padding: 6px 14px;
                font-size: 13px;
                color: rgba(15, 23, 42, 220);
                font-weight: 600;
            }
            QPushButton {
                background-color: rgba(137, 196, 244, 200);
                color: #0f172a;
                border-radius: 22px;
                padding: 12px 32px;
                font-size: 15px;
                font-weight: 600;
                letter-spacing: 2px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(137, 196, 244, 230);
            }
            QPushButton:disabled {
                background-color: rgba(148, 163, 184, 160);
                color: rgba(15, 23, 42, 180);
            }
            #StatusLabel {
                margin-top: 6px;
                padding: 10px 18px;
                border-radius: 20px;
                background: rgba(148, 163, 184, 80);
                color: rgba(226, 232, 240, 220);
                font-size: 14px;
                letter-spacing: 1px;
            }
            #StatusLabel[state="busy"] {
                background: rgba(96, 165, 250, 90);
                color: rgba(15, 23, 42, 220);
            }
            #StatusLabel[state="success"] {
                background: rgba(16, 185, 129, 120);
                color: rgba(15, 23, 42, 220);
            }
            #StatusLabel[state="warning"] {
                background: rgba(248, 113, 113, 120);
                color: rgba(15, 23, 42, 220);
            }
            #ProgressBar {
                border: 1px solid rgba(255, 255, 255, 90);
                border-radius: 18px;
                background: rgba(255, 255, 255, 40);
                padding: 4px;
                height: 20px;
            }
            #ProgressBar::chunk {
                border-radius: 14px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(59, 130, 246, 230), stop:1 rgba(14, 165, 233, 220));
            }
            #LogHeader {
                color: rgba(226, 232, 240, 220);
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 2px;
            }
            #LogOutput {
                background-color: rgba(15, 23, 42, 160);
                border: 1px solid rgba(255, 255, 255, 60);
                border-radius: 18px;
                padding: 18px;
                color: rgba(248, 250, 252, 230);
                font-family: "JetBrains Mono", "Noto Sans Mono", monospace;
                font-size: 13px;
            }
            #LogOutput QScrollBar:vertical {
                background: transparent;
                width: 12px;
                margin: 12px;
            }
            #LogOutput QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 90);
                border-radius: 6px;
            }
            """
        )

    def tr(self, key, **kwargs):
        text = self.translations.get(self.current_language, {}).get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text

    def set_language(self, language_code):
        if language_code not in self.translations:
            return

        self.current_language = language_code
        texts = self.translations[language_code]

        blocker = QSignalBlocker(self.language_combo)
        index = self.language_combo.findData(language_code)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        del blocker

        self.setWindowTitle(texts["window_title"])
        self.version_label.setText(texts["version_label"].format(version=VERSION))
        self.github_link.setText(texts["github_link"].format(url=GITHUB_URL, owner=GITHUB_OWNER))
        self.language_label.setText(texts["language_label"])

        self.title_label.setText(texts["hero_title"])
        self.subtitle_label.setText(texts["hero_subtitle"])
        self.hero_description.setText(texts["hero_description"])
        for label, chip_text in zip(self.chip_labels, texts["chips"]):
            label.setText(chip_text)
        self.tips_title.setText(texts["tips_title"])
        self.tips_content.setText(texts["tips_content"])

        for label, key in self.form_label_widgets:
            label.setText(texts[key])
        self.form_helper.setText(texts["form_helper"])
        self.usernames_edit.setPlaceholderText(texts["placeholder_users"])
        self.open_folder_checkbox.setText(texts["option_auto_open"])
        self.clear_button.setText(texts["button_reset"])
        self.start_button.setText(texts["button_start"])

        self.log_header.setText(texts["log_header"])
        self.status_label.setText(self.tr(self.current_status_key))
        self.update_responsive_layout()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_responsive_layout()

    def update_responsive_layout(self):
        available_width = max(self.width() - 96, 640)
        available_height = max(self.height() - 96, 540)

        max_card_width = min(available_width, 1320)
        for card in (self.hero_card, self.glass_card, self.log_card):
            card.setMaximumWidth(max_card_width)

        quote_width = max(int(max_card_width * 0.32), 260)
        self.quote_card.setMinimumWidth(quote_width)
        self.quote_card.setMaximumWidth(max(quote_width, 380))

        wrap_width = max(int(max_card_width * 0.48), 360)
        for label in getattr(self, "responsive_labels", []):
            label.setMaximumWidth(wrap_width)

        log_min_height = max(int(available_height * 0.32), 220)
        self.log_output.setMinimumHeight(log_min_height)

        wrap_pixels = max(int(max_card_width * 0.65), 540)
        document = self.log_output.document()
        document.setTextWidth(wrap_pixels)

    def on_language_changed(self, index):
        language_code = self.language_combo.itemData(index)
        if language_code and language_code != self.current_language:
            self.set_language(language_code)

    def open_link(self, url):
        if url:
            QDesktopServices.openUrl(QUrl(url))

    def start_backup(self):
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(
                self,
                self.tr("dialog_in_progress_title"),
                self.tr("dialog_in_progress_body"),
            )
            return

        usernames_text = self.usernames_edit.text().strip()
        if not usernames_text:
            QMessageBox.warning(
                self,
                self.tr("dialog_missing_user_title"),
                self.tr("dialog_missing_user_body"),
            )
            return

        usernames = usernames_text.split()
        self.last_usernames = usernames
        credentials = {
            "CONSUMER_KEY": self.consumer_key.text().strip(),
            "CONSUMER_SECRET": self.consumer_secret.text().strip(),
            "ACCESS_TOKEN": self.access_token.text().strip(),
            "ACCESS_TOKEN_SECRET": self.access_token_secret.text().strip(),
        }

        missing = [key for key, value in credentials.items() if not value]
        if missing:
            QMessageBox.warning(
                self,
                self.tr("dialog_missing_keys_title"),
                self.tr("dialog_missing_keys_body"),
            )
            return

        self.log_output.clear()
        self.update_status("status_running", "busy")
        self.start_button.setDisabled(True)
        self.clear_button.setDisabled(True)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(True)

        self.worker = BackupWorker(usernames, credentials, self)
        self.worker.output.connect(self.append_log)
        self.worker.finished.connect(self.backup_finished)
        self.worker.start()

    def append_log(self, message):
        self.log_output.appendPlainText(message)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
        lowered = message.lower()
        if self.worker and self.worker.isRunning() and any(
            keyword in lowered for keyword in ("error", "失敗", "exception", "警告", "warning")
        ):
            self.update_status("status_warning_detected", "warning")

    def backup_finished(self, return_code):
        if return_code == 0:
            self.update_status("status_success", "success")
        else:
            self.update_status("status_warning", "warning")
        self.start_button.setDisabled(False)
        self.clear_button.setDisabled(False)
        self.worker = None
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        QTimer.singleShot(1200, lambda: self.progress_bar.setVisible(False))

        if return_code == 0 and self.open_folder_checkbox.isChecked() and self.last_usernames:
            first_user = self.last_usernames[0]
            target_path = Path(first_user).resolve()
            if target_path.exists():
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(target_path)))
            else:
                self.append_log(self.tr("log_missing_folder", path=target_path))

    def update_status(self, key, state):
        self.current_status_key = key
        self.status_label.setText(self.tr(key))
        self.status_label.setProperty("state", state)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

        self.status_effect.setOpacity(0.0)
        self.status_animation = QPropertyAnimation(self.status_effect, b"opacity")
        self.status_animation.setDuration(600)
        self.status_animation.setStartValue(0.0)
        self.status_animation.setEndValue(1.0)
        self.status_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.status_animation.start()

    def reset_form(self):
        self.consumer_key.clear()
        self.consumer_secret.clear()
        self.access_token.clear()
        self.access_token_secret.clear()
        self.usernames_edit.clear()
        self.log_output.clear()
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.update_status("status_reset", "idle")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
