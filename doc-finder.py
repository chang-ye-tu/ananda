import os
import sys
import sqlite3
import time
from functools import partial
from subprocess import Popen, call
from pathlib import Path
from typing import List, Tuple, Optional

from PyQt5.QtCore import QUrl, Qt, pyqtSlot, pyqtSignal, QTimer, QObject, QStringListModel
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame, QMenu, QAction, QInputDialog, QMessageBox, QCompleter
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel

class DocumentFinderConfig:
    """Configuration class for document finder settings"""
    SEARCH_FOLDERS = ['/home/cytu/usr/']
    DOCUMENT_TYPES = ['.pdf', '.djvu', '.ps', '.chm', '.epub']
    DATABASE_PATH = os.path.join(Path(__file__).resolve().parent, 'db', 'doc.db')
    TEMP_HTML_PATH = os.path.join(Path(__file__).resolve().parent, 'tmp', 'doc_finder.htm')

def generate_html(content, centered=False):
    """Generate HTML with proper styling and web channel setup"""
    centered_content = f'''<div id='outer'><div id='middle'><div id='inner'>
        {content}
        </div></div></div>''' if centered else content
    
    return f'''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 
    'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<meta http-equiv='X-UA-Compatible' content='IE=EmulateIE7'>
<head>
    <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script type="text/javascript">
        var doc_finder;
        if (typeof qt !== 'undefined') {{
            new QWebChannel(qt.webChannelTransport, function(channel) {{
                doc_finder = channel.objects.doc_finder;
            }});
        }}
    </script>
    <style>
        p {{ font-family: "Helvetica", "Noto Sans", serif, Times; font-size: 20px; }}
        img {{ float:left; margin-right: 5px; }}
        a {{ font-weight: bold; text-decoration: none; color: blue; }}
        .fsize {{ font-weight: bold; color: red; }}
        .ctime {{ font-weight: bold; color: green; }}
        .fpath {{ font-weight: bold; }}
    </style>
</head>
<body>
{centered_content}
</body>
</html>'''

def format_file_size(size):
    """Convert file size to human readable format"""
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while size > 1024.0 and index < len(suffixes) - 1:
        index += 1
        size /= 1024.0
    return f'{size:.2f} {suffixes[index]}'

class DatabaseManager:
    """Handle all database operations"""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def initialize_database(self):
        """Create necessary tables and indexes"""
        # Create documents table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS doc (
                id INTEGER PRIMARY KEY,
                filename TEXT NOT NULL,
                path TEXT NOT NULL UNIQUE,
                created TEXT NOT NULL,
                size TEXT NOT NULL
            )
        ''')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS ix_doc_filename ON doc(filename)')

        # Create history table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                search TEXT NOT NULL,
                created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS ix_history_search ON history(search)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS ix_history_created ON history(created)')
        
        self.connection.commit()

    def rebuild_database(self):
        """Rebuild the database with fresh document information"""
        # Save old history
        old_history = self.cursor.execute(
            'SELECT search, created FROM history'
        ).fetchall()

        # Recreate tables
        self.cursor.execute('DROP TABLE IF EXISTS doc')
        self.cursor.execute('DROP TABLE IF EXISTS history')
        self.initialize_database()

        # Restore history
        if old_history:
            self.cursor.executemany(
                'INSERT INTO history(search, created) VALUES(?, ?)',
                old_history
            )

        # Scan for documents
        for folder in DocumentFinderConfig.SEARCH_FOLDERS:
            for root, _, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in DocumentFinderConfig.DOCUMENT_TYPES):
                        path = os.path.join(root, file)
                        self.add_document(path)

        self.connection.commit()

    def add_document(self, path: str):
        """Add a single document to the database"""
        filename = os.path.splitext(os.path.basename(path))[0]
        created = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(os.path.getmtime(path))
        )
        size = format_file_size(os.path.getsize(path))
        
        self.cursor.execute(
            'INSERT INTO doc(filename, path, created, size) VALUES(?, ?, ?, ?)',
            (filename, path, created, size)
        )

class DocumentBrowser(QWebEngineView):
    """Custom WebEngine view for document display"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.NoContextMenu)

    def display_content(self, html_content: str):
        """Display HTML content in the browser"""
        with open(DocumentFinderConfig.TEMP_HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(html_content)
        self.load(QUrl.fromLocalFile(DocumentFinderConfig.TEMP_HTML_PATH))

class DocumentFinderJS(QObject):
    """JavaScript bridge for document operations"""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    @pyqtSlot(str)
    def open_file(self, file_id: str):
        """Handle file opening requests from JavaScript"""
        self.parent.open_file(file_id)

class SearchWidget(QWidget):
    """Widget containing search box and results display"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        self.search_box = QLineEdit(self)
        self.browser = DocumentBrowser(self)
        
        layout.addWidget(self.search_box)
        layout.addWidget(self.browser)

class DocumentFinderWindow(QMainWindow):
    """Main application window"""
    status_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_database()
        self.setup_actions()
        self.initialize_state()

    def setup_ui(self):
        """Initialize UI components"""
        self.setWindowTitle('Document Finder')
        self.setWindowIcon(QIcon('/home/cytu/usr/src/py/ananda/res/img/filefind.png'))
        
        # Setup status bar
        self.setup_status_bar()
        
        # Setup main widget
        self.search_widget = SearchWidget()
        self.setCentralWidget(self.search_widget)
        
        # Setup completer
        self.completer = QCompleter()
        self.completer_model = QStringListModel()
        self.completer.setModel(self.completer_model)
        self.search_widget.search_box.setCompleter(self.completer)
        
        # Setup web channel
        self.setup_web_channel()

    def setup_status_bar(self):
        """Initialize status bar components"""
        status_bar = self.statusBar()
        
        self.status_label = QLabel(self)
        self.total_label = QLabel(self)
        
        for label in (self.status_label, self.total_label):
            label.setAlignment(Qt.AlignCenter)
            label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
            status_bar.addPermanentWidget(label, 1)
        
        status_bar.setSizeGripEnabled(False)

    def setup_web_channel(self):
        """Setup communication channel between Python and JavaScript"""
        self.js_bridge = DocumentFinderJS(self)
        channel = QWebChannel(self)
        channel.registerObject('doc_finder', self.js_bridge)
        self.search_widget.browser.page().setWebChannel(channel)

    def setup_database(self):
        """Initialize database connection"""
        self.db = DatabaseManager(DocumentFinderConfig.DATABASE_PATH)
        if not os.path.isfile(self.db.db_path):
            self.db.rebuild_database()

    def setup_actions(self):
        """Setup menu actions and shortcuts"""
        # Create context menu
        self.context_menu = QMenu(self)
        
        # Define menu actions
        actions = [
            ('open_doc', 'Open File', '', False),
            None,
            ('open_parent', 'Open Parent Folder', '', False),
            None,
            ('sort_fname', 'Sort by File Name', '', False),
            ('sort_path', 'Sort by Path', '', False),
            ('sort_ctime', 'Sort by Created Time', '', False),
            None,
            ('rename_file', 'Rename File', '', False),
            ('copy_name', 'Copy File Name', '', False),
            ('pdftk', 'PDFtk File', '', False),
            None,
            ('delete_file', 'Delete File', '', False),
            None,
            ('recreate_db', 'Recreate Database', '', False),
        ]

        # Create menu actions
        for action_def in actions:
            if action_def is None:
                self.context_menu.addSeparator()
                continue
                
            name, title, shortcut, checkable = action_def
            action = QAction(title, self)
            action.setCheckable(checkable)
            if shortcut:
                action.setShortcut(shortcut)
            action.triggered.connect(partial(self.handle_action, name))
            self.context_menu.addAction(action)
            setattr(self, f'action_{name}', action)

        # Setup keyboard shortcuts
        shortcuts = [
            ('focus', 'Ctrl+K'),
            ('find_text', 'Ctrl+F'),
            ('find_previous', 'Alt+Left'),
            ('find_next', 'Alt+Right'),
        ]

        for name, key in shortcuts:
            action = QAction(self)
            action.setShortcut(key)
            action.triggered.connect(partial(self.handle_action, name))
            self.addAction(action)
            setattr(self, f'action_{name}', action)

        # Connect search box signals
        self.search_widget.search_box.returnPressed.connect(self.show_search_results)
        self.status_changed.connect(self.update_status_bar)

    def initialize_state(self):
        """Initialize application state"""
        self.current_sort = 'filename'
        self.current_file_id = None
        self.history_index = 0
        self.update_document_count()
        self.update_search_history()
        QTimer.singleShot(2, self.restore_last_search)

    def restore_last_search(self):
        """Restore the last search query from history"""
        last_search = self.db.cursor.execute(
            'SELECT DISTINCT search FROM history ORDER BY created DESC LIMIT 1'
        ).fetchone()
        
        if last_search:
            self.search_widget.search_box.setText(last_search[0])
            self.update_search_results(last_search[0])

    def update_search_history(self):
        """Update search history and completer"""
        history = self.db.cursor.execute(
            'SELECT DISTINCT search FROM history ORDER BY created DESC LIMIT 1000'
        ).fetchall()
        
        if history:
            self.completer_model.setStringList([item[0] for item in history])
        self.history_index = 0

    def update_document_count(self):
        """Update total document count in status bar"""
        count = self.db.cursor.execute('SELECT COUNT(*) FROM doc').fetchone()[0]
        self.update_status('total_label', 
            f'<font color="blue">Total Documents: &nbsp;&nbsp;&nbsp;</font>'
            f'<font color="red">{count}</font>')

    def update_status_bar(self, data: dict):
        """Update status bar with provided information"""
        if 'label' in data and 'message' in data:
            label = getattr(self, f'{data["label"]}')
            if label:
                label.setText(data['message'])

    def update_status(self, label: str, message: str):
        """Emit signal to update status bar"""
        self.status_changed.emit({'label': label, 'message': message})

    def show_search_results(self):
        """Handle search box return press"""
        self.update_status('status_label', 
            '<font color="blue">Searching...</font>')
        
        query = self.search_widget.search_box.text()
        QTimer.singleShot(1, lambda: self.update_search_results(query))
        
        # Add to history
        try:
            self.db.cursor.execute(
                'INSERT INTO history (search) VALUES (?)',
                (query,)
            )
            self.db.connection.commit()
            self.update_search_history()
        except sqlite3.Error as e:
            print(f"Error updating history: {e}")

        self.search_widget.browser.setFocus()

    def update_search_results(self, query: str):
        """Update browser with search results"""
        try:
            results = self.db.cursor.execute(
                f'SELECT * FROM doc WHERE filename LIKE ? ORDER BY {self.current_sort}',
                (f'%{query}%',)
            ).fetchall()

            html_content = self.generate_results_html(results)
            self.search_widget.browser.display_content(
                generate_html(html_content)
            )

            self.update_status('status_label',
                f'<font color="blue">Results: &nbsp;&nbsp;&nbsp;</font>'
                f'<font color="red">{len(results)}</font>')

        except sqlite3.Error as e:
            self.update_status('status_label', f'<font color="red">Search error: {e}</font>')

    def generate_results_html(self, results):
        """Generate HTML content for search results"""
        html_parts = []
        for result in results:
            doc_id, filename, path, created, size = result
            file_type = os.path.splitext(path)[1][1:].lower()
            
            html_parts.append(f"""
                <p>
                    <img src='/home/cytu/usr/src/py/ananda/res/img/{file_type}_icon.png'
                         width='56' height='56' />
                    <a href='' onClick="doc_finder.open_file('{doc_id}'); return false;">
                        {filename}
                    </a><br />
                    <span class='ctime'>{created}</span>&nbsp;&nbsp;&nbsp;&nbsp;
                    <span class='fsize'>{size}</span>&nbsp;&nbsp;&nbsp;&nbsp;
                    <span class='fpath'>{path}</span><br />
                </p>
            """)
        
        return ''.join(html_parts)

    def handle_action(self, action_name: str):
        """Handle menu and shortcut actions"""
        search_box = self.search_widget.search_box
        query = search_box.text()
        
        if action_name == 'focus':
            search_box.setFocus()
            search_box.selectAll()
            
        elif action_name == 'find_text':
            self.search_widget.browser.page().findText(
                query.replace('%', ''),
                QWebEnginePage.FindWrapsAroundDocument
            )
            
        elif action_name in ['find_previous', 'find_next']:
            search_box.setFocus()
            history = self.completer_model.stringList()
            if history:
                self.history_index += (1 if action_name == 'find_previous' else -1)
                self.history_index %= len(history)
                search_box.setText(history[self.history_index])
                
        elif action_name.startswith('sort_'):
            sort_type = {
                'sort_fname': 'filename',
                'sort_path': 'path',
                'sort_ctime': 'created DESC'
            }.get(action_name)
            if sort_type:
                self.current_sort = sort_type
                self.update_search_results(query)
                
        elif action_name == 'recreate_db':
            self.db.rebuild_database()
            self.update_search_results(query)
            self.update_document_count()
            
        else:
            self.handle_file_action(action_name)

    def handle_file_action(self, action_name: str):
        """Handle file-related actions"""
        if not self.current_file_id:
            return
            
        try:
            path, filename = self.db.cursor.execute(
                'SELECT path, filename FROM doc WHERE id = ?',
                (self.current_file_id,)
            ).fetchone() or (None, None)
            
            if not path:
                return

            if action_name == 'open_doc':
                Popen(['xdg-open', path])
                
            elif action_name == 'open_parent':
                Popen(['xdg-open', os.path.dirname(path)])
                
            elif action_name == 'rename_file':
                self.rename_file(path, filename)
                
            elif action_name == 'delete_file':
                self.delete_file(path, filename)
                
            elif action_name == 'copy_name':
                QApplication.clipboard().setText(filename)
                
            elif action_name == 'pdftk':
                self.process_pdf(path)

        except Exception as e:
            self.update_status('status_label',
                f'<font color="red">Error: {e}</font>')

    def rename_file(self, path: str, filename: str):
        """Handle file renaming"""
        new_name, ok = QInputDialog.getText(
            self,
            'Rename File',
            f'Original Name:\n  {filename}',
            QLineEdit.Normal,
            filename
        )
        
        if ok and new_name:
            new_path = os.path.join(
                os.path.dirname(path),
                f"{new_name}{os.path.splitext(path)[1]}"
            )
            
            try:
                os.rename(path, new_path)
                self.db.cursor.execute(
                    '''UPDATE doc 
                       SET filename = ?, path = ?, created = ? 
                       WHERE id = ?''',
                    (
                        new_name,
                        new_path,
                        time.strftime(
                            '%Y-%m-%d %H:%M:%S',
                            time.localtime(os.path.getctime(new_path))
                        ),
                        self.current_file_id
                    )
                )
                self.db.connection.commit()
                self.update_search_results(self.search_widget.search_box.text())
                
            except OSError as e:
                self.update_status('status_label',
                    f'<font color="red">Error renaming file: {e}</font>')

    def delete_file(self, path: str, filename: str):
        """Handle file deletion"""
        reply = QMessageBox.question(
            self,
            'Delete File',
            f'Really want to delete file \n{filename} ?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                os.remove(path)
                self.db.cursor.execute(
                    'DELETE FROM doc WHERE id = ?',
                    (self.current_file_id,)
                )
                self.db.connection.commit()
                self.update_search_results(self.search_widget.search_box.text())
                self.update_document_count()
                
            except OSError as e:
                self.update_status('status_label',
                    f'<font color="red">Error deleting file: {e}</font>')

    def process_pdf(self, path: str):
        """Handle PDF processing with pdftk"""
        temp_path = f"{path}______"
        try:
            result = call(['pdftk', path, 'cat', '1-end', 'output', temp_path])
            if result == 0:
                os.replace(temp_path, path)
                
                self.db.cursor.execute(
                    'UPDATE doc SET created = ?, size = ? WHERE id = ?',
                    (
                        time.strftime(
                            '%Y-%m-%d %H:%M:%S',
                            time.localtime(os.path.getctime(path))
                        ),
                        format_file_size(os.path.getsize(path)),
                        self.current_file_id
                    )
                )
                self.db.connection.commit()
                self.update_search_results(self.search_widget.search_box.text())
            else:
                raise Exception("PDFtk processing failed")
                
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            self.update_status('status_label',
                f'<font color="red">Error processing PDF: {e}</font>')

    def open_file(self, file_id: str):
        """Handle file opening from JavaScript"""
        self.current_file_id = file_id
        self.context_menu.exec_(QCursor.pos())

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName('Document Finder')
    app.setFont(QFont('Microsoft JhengHei'))

    window = DocumentFinderWindow()
    window.showMaximized()
    
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
