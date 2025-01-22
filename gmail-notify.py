#!/usr/bin/env python3

import os
import sys
import base64
import subprocess
from email.mime.text import MIMEText
from datetime import datetime, timezone
from PyQt5.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, 
                            QMenu, QAction, QStyle)
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from inspect import getsourcefile

class GmailAuth:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, token_file='res/token.json', credentials_file='res/credentials.json'):
        self.token_file = token_file
        self.credentials_file = credentials_file
        self._creds = None

    def get_credentials(self):
        """Get valid credentials, refreshing or creating new ones if necessary."""
        if self._creds and self._creds.valid:
            return self._creds

        if os.path.exists(self.token_file):
            self._creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Missing credentials file: {self.credentials_file}\n"
                        "Please download it from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
                self._creds = flow.run_local_server(port=0)

            # Save the credentials
            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, 'w') as token:
                token.write(self._creds.to_json())

        return self._creds

class EmailMessage:
    def __init__(self, msg_data):
        self.id = msg_data['id']
        headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
        self.subject = headers.get('Subject', '(no subject)')
        self.from_addr = headers.get('From', '(unknown sender)')
        self.date = headers.get('Date')
        self.snippet = msg_data.get('snippet', '')

    @property
    def summary(self):
        return f"From: {self.from_addr}\nSubject: {self.subject}\n{self.snippet[:100]}..."

class GmailNotifier(QWidget):
    P_ON = './res/img/gmail_on.ico'
    P_OFF = './res/img/gmail_off.ico'
    CHECK_INTERVAL = 30000  # 30 seconds in milliseconds

    def __init__(self, parent=None):
        super().__init__(parent)
        os.chdir(os.path.dirname(os.path.abspath(getsourcefile(lambda:0))))
        
        self.known_messages = set()  # Store IDs of known unread messages
        self.setup_tray()
        self.setup_menu()
        self.setup_state()
        self.setup_gmail_service()
        self.setup_timer()
        self.setup_audio()

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        # Use system mail icon as fallback if custom icon not found
        if not os.path.exists(self.P_OFF):
            self.P_OFF = self.style().standardIcon(QStyle.SP_DialogNoButton)
        if not os.path.exists(self.P_ON):
            self.P_ON = self.style().standardIcon(QStyle.SP_DialogYesButton)
            
        self.tray_icon.setIcon(QIcon(self.P_OFF))
        self.tray_icon.activated.connect(self.handle_tray_activation)
        self.tray_icon.show()

    def setup_menu(self):
        menu = QMenu(self)
        actions = {
            'check': 'Check Now',
            'listen': 'Toggle Listening',
            'audio': 'Toggle Audio',
            'quit': 'Quit'
        }
        
        for action_name, display_name in actions.items():
            action = QAction(display_name, self)
            action.triggered.connect(getattr(self, action_name))
            menu.addAction(action)
            setattr(self, f'action_{action_name}', action)
        
        self.tray_icon.setContextMenu(menu)

    def setup_state(self):
        self.is_listening = True
        self.audio_enabled = False
        self.update_tooltip()

    def setup_gmail_service(self):
        try:
            self.auth = GmailAuth()
            creds = self.auth.get_credentials()
            self.service = build('gmail', 'v1', credentials=creds)
        except Exception as error:
            self.show_error(f'Authentication Error: {str(error)}')
            self.service = None

    def setup_timer(self):
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check)
        self.check_timer.start(self.CHECK_INTERVAL)

    def setup_audio(self):
        self.media_player = QMediaPlayer(self)
        audio_file = '/home/cytu/usr/src/py/ananda/res/av/gmail.mp3'
        if os.path.exists(audio_file):
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_file)))

    def get_message_details(self, msg_id):
        """Fetch detailed information about a specific message."""
        try:
            msg = self.service.users().messages().get(
                userId='me', 
                id=msg_id, 
                format='full'
            ).execute()
            return EmailMessage(msg)
        except HttpError as error:
            self.show_error(f'Error fetching message details: {error}')
            return None

    def check(self):
        if not self.is_listening or not self.service:
            return

        try:
            # Get list of unread messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                labelIds=['INBOX'],  # Only check inbox
                includeSpamTrash=False
            ).execute()
            
            messages = results.get('messages', [])
            current_unread = {msg['id'] for msg in messages}
            
            # Find new unread messages
            new_messages = current_unread - self.known_messages
            
            if new_messages:
                # Get details for new messages
                message_details = []
                for msg_id in new_messages:
                    msg = self.get_message_details(msg_id)
                    if msg:
                        message_details.append(msg)

                # Update UI and notify
                self.tray_icon.setIcon(QIcon(self.P_ON))
                
                if message_details:
                    # Create notification with details of new messages
                    summary = "\n\n".join(msg.summary for msg in message_details[:3])
                    if len(message_details) > 3:
                        summary += f"\n\n...and {len(message_details) - 3} more messages"
                    
                    self.tray_icon.showMessage(
                        f'New Mail ({len(new_messages)})',
                        summary,
                        QSystemTrayIcon.Information,
                        10000  # Show for 10 seconds
                    )
                    
                    if self.audio_enabled:
                        self.media_player.play()

            elif not current_unread:
                # No unread messages
                self.tray_icon.setIcon(QIcon(self.P_OFF))
            
            # Update known messages
            self.known_messages = current_unread

        except HttpError as error:
            if 'invalid_grant' in str(error):
                # Token expired or revoked, try to refresh
                self.setup_gmail_service()
            else:
                self.show_error(f'Error checking mail: {error}')

    def update_tooltip(self):
        status = 'idle' if not self.is_listening else 'listening'
        audio = 'on' if self.audio_enabled else 'off'
        self.tray_icon.setToolTip(f'Gmail Notifier - audio:{audio} [{status}]')

    def show_error(self, message):
        self.tray_icon.showMessage('Error', message, QSystemTrayIcon.Critical)

    def handle_tray_activation(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            subprocess.Popen(['google-chrome', 'https://mail.google.com/mail/u/0/?shva=1#search/is%3Aunread'])

    def listen(self):
        self.is_listening = not self.is_listening
        self.update_tooltip()
        if self.is_listening:
            self.check()  # Immediate check when resuming

    def audio(self):
        self.audio_enabled = not self.audio_enabled
        self.update_tooltip()

    def quit(self):
        self.tray_icon.hide()
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Gmail Notifier')
    
    font = QFont('Microsoft JhengHei')
    font.setPointSize(12)
    app.setFont(font)
    app.setQuitOnLastWindowClosed(False)
    
    notifier = GmailNotifier()
    sys.exit(app.exec())
