"""Custom table widget for displaying files."""

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from .file_model import FileTableRow, create_table_row
from .native_ops import open_file, show_in_finder, copy_path_to_clipboard


class SortableTableItem(QTableWidgetItem):
    """Custom table item that supports proper sorting of numeric values."""

    def __init__(self, text, sort_value=None):
        """
        Initialize sortable item.

        Args:
            text: Display text
            sort_value: Value to use for sorting (if different from text)
        """
        super().__init__(text)
        if sort_value is not None:
            self.setData(Qt.ItemDataRole.UserRole, sort_value)

    def __lt__(self, other):
        """Compare items for sorting."""
        self_data = self.data(Qt.ItemDataRole.UserRole)
        other_data = other.data(Qt.ItemDataRole.UserRole)

        if self_data is not None and other_data is not None:
            return self_data < other_data

        return super().__lt__(other)


class FileTableWidget(QTableWidget):
    """Custom table widget for displaying file information."""

    def __init__(self, parent=None):
        """Initialize the file table widget."""
        super().__init__(parent)
        self.setup_table()

    def setup_table(self):
        """Configure table appearance and behavior."""
        # Set columns
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['Name', 'Size', 'Kind', 'Date Modified'])

        # Enable sorting
        self.setSortingEnabled(True)

        # Set selection behavior
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        # Set column widths
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        self.setColumnWidth(0, 300)  # Name
        self.setColumnWidth(1, 100)  # Size
        self.setColumnWidth(2, 120)  # Kind

        # Disable editing
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Alternating row colors for better readability
        self.setAlternatingRowColors(True)

    def populate_files(self, file_entries):
        """
        Populate table with file entries.

        Args:
            file_entries: List of FileEntry objects
        """
        self.setRowCount(0)  # Clear existing rows
        self.setSortingEnabled(False)  # Disable sorting while populating

        for entry in file_entries:
            row_data = create_table_row(entry)
            self.add_row(row_data)

        self.setSortingEnabled(True)  # Re-enable sorting
        self.sortItems(0, Qt.SortOrder.AscendingOrder)  # Sort by name initially

    def add_row(self, row_data: FileTableRow):
        """
        Add a single row to the table.

        Args:
            row_data: FileTableRow object
        """
        row = self.rowCount()
        self.insertRow(row)

        # Name column
        name_item = SortableTableItem(row_data.name)
        name_item.setData(Qt.ItemDataRole.UserRole + 1, str(row_data.path))  # Store full path
        self.setItem(row, 0, name_item)

        # Size column (with numeric value for sorting)
        size_item = SortableTableItem(row_data.size, row_data.size_bytes)
        self.setItem(row, 1, size_item)

        # Kind column
        kind_item = SortableTableItem(row_data.kind)
        self.setItem(row, 2, kind_item)

        # Date Modified column (with timestamp for sorting)
        date_item = SortableTableItem(row_data.modified, row_data.modified_ts)
        self.setItem(row, 3, date_item)

    def get_selected_files(self):
        """
        Get list of selected file paths.

        Returns:
            List of Path objects for selected files
        """
        from pathlib import Path

        selected_rows = set(item.row() for item in self.selectedItems())
        file_paths = []

        for row in selected_rows:
            name_item = self.item(row, 0)
            if name_item:
                path_str = name_item.data(Qt.ItemDataRole.UserRole + 1)
                if path_str:
                    file_paths.append(Path(path_str))

        return file_paths

    def remove_rows(self, row_indices):
        """
        Remove rows from the table.

        Args:
            row_indices: List of row indices to remove
        """
        # Remove in reverse order to avoid index shifting issues
        for row in sorted(row_indices, reverse=True):
            self.removeRow(row)

    def mouseDoubleClickEvent(self, event):
        """Handle double-click to open file."""
        super().mouseDoubleClickEvent(event)

        selected_files = self.get_selected_files()
        if selected_files:
            open_file(selected_files[0])

    def contextMenuEvent(self, event):
        """Show context menu on right-click."""
        selected_files = self.get_selected_files()
        if not selected_files:
            return

        menu = QMenu(self)

        # Open action
        open_action = QAction('Open', self)
        open_action.triggered.connect(lambda: self._open_selected())
        menu.addAction(open_action)

        # Show in Finder action
        show_action = QAction('Show in Finder', self)
        show_action.triggered.connect(lambda: self._show_in_finder())
        menu.addAction(show_action)

        menu.addSeparator()

        # Copy Path action
        copy_action = QAction('Copy Path', self)
        copy_action.triggered.connect(lambda: self._copy_path())
        menu.addAction(copy_action)

        menu.addSeparator()

        # Move to Trash action
        trash_action = QAction('Move to Trash', self)
        trash_action.triggered.connect(lambda: self._move_to_trash())
        menu.addAction(trash_action)

        menu.exec(event.globalPos())

    def _open_selected(self):
        """Open selected file(s)."""
        selected_files = self.get_selected_files()
        for file_path in selected_files:
            open_file(file_path)

    def _show_in_finder(self):
        """Show selected file in Finder."""
        selected_files = self.get_selected_files()
        if selected_files:
            show_in_finder(selected_files[0])

    def _copy_path(self):
        """Copy path of selected file."""
        selected_files = self.get_selected_files()
        if selected_files:
            copy_path_to_clipboard(selected_files[0])

    def _move_to_trash(self):
        """Move selected files to trash."""
        from .native_ops import move_to_trash

        selected_files = self.get_selected_files()
        if not selected_files:
            return

        # Get row indices to remove
        selected_rows = set(item.row() for item in self.selectedItems())

        # Move to trash
        if move_to_trash(selected_files):
            # Remove from table if successful
            self.remove_rows(selected_rows)
