"""Main window for the file viewer application."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence

from .file_table import FileTableWidget
from .native_ops import move_to_trash


class FileViewerWindow(QMainWindow):
    """Main window for viewing and managing files."""

    def __init__(self, file_entries, parent=None):
        """
        Initialize the file viewer window.

        Args:
            file_entries: List of FileEntry objects to display
            parent: Parent widget
        """
        super().__init__(parent)
        self.file_entries = file_entries
        self.setup_ui()
        self.setup_shortcuts()

        # Populate table with files
        if file_entries:
            self.file_table.populate_files(file_entries)

    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle('Sweep - File Review')
        self.setMinimumSize(800, 600)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel('Search:')
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText('Filter files by name...')
        self.search_box.textChanged.connect(self.filter_files)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)
        main_layout.addLayout(search_layout)

        # File table
        self.file_table = FileTableWidget()
        main_layout.addWidget(self.file_table)

        # Bottom button bar
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.trash_button = QPushButton('Move to Trash')
        self.trash_button.clicked.connect(self.move_selected_to_trash)
        button_layout.addWidget(self.trash_button)

        main_layout.addLayout(button_layout)

        # Status bar to show file count
        self.statusBar().showMessage(f'{len(self.file_entries)} files found')

    def setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # Cmd+W to close window
        close_action = QAction('Close', self)
        close_action.setShortcut(QKeySequence('Ctrl+W'))  # Qt maps Ctrl to Cmd on macOS
        close_action.triggered.connect(self.close)
        self.addAction(close_action)

        # Cmd+F to focus search
        search_action = QAction('Search', self)
        search_action.setShortcut(QKeySequence('Ctrl+F'))
        search_action.triggered.connect(self.focus_search)
        self.addAction(search_action)

        # Delete/Backspace to move to trash
        delete_action = QAction('Delete', self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self.move_selected_to_trash)
        self.addAction(delete_action)

    def focus_search(self):
        """Focus the search box."""
        self.search_box.setFocus()
        self.search_box.selectAll()

    def filter_files(self, search_text):
        """
        Filter table rows based on search text.

        Args:
            search_text: Text to search for in file names
        """
        search_text = search_text.lower()

        for row in range(self.file_table.rowCount()):
            item = self.file_table.item(row, 0)  # Name column
            if item:
                file_name = item.text().lower()
                # Show row if search text is in file name, hide otherwise
                self.file_table.setRowHidden(row, search_text not in file_name)

        # Update status bar with visible count
        visible_count = sum(
            1 for row in range(self.file_table.rowCount())
            if not self.file_table.isRowHidden(row)
        )
        total_count = self.file_table.rowCount()

        if search_text:
            self.statusBar().showMessage(
                f'{visible_count} of {total_count} files shown'
            )
        else:
            self.statusBar().showMessage(f'{total_count} files found')

    def move_selected_to_trash(self):
        """Move selected files to trash."""
        selected_files = self.file_table.get_selected_files()

        if not selected_files:
            QMessageBox.information(
                self,
                'No Selection',
                'Please select files to move to trash.'
            )
            return

        # Confirm action
        file_count = len(selected_files)
        if file_count == 1:
            message = f'Move "{selected_files[0].name}" to trash?'
        else:
            message = f'Move {file_count} files to trash?'

        reply = QMessageBox.question(
            self,
            'Confirm Move to Trash',
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Get row indices before moving
            selected_rows = set(item.row() for item in self.file_table.selectedItems())

            # Move to trash
            if move_to_trash(selected_files):
                # Remove from table
                self.file_table.remove_rows(selected_rows)

                # Update status bar
                remaining = self.file_table.rowCount()
                self.statusBar().showMessage(
                    f'{remaining} files remaining ({file_count} moved to trash)'
                )
            else:
                QMessageBox.warning(
                    self,
                    'Error',
                    'Failed to move files to trash. Please check permissions.'
                )
