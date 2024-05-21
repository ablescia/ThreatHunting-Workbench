import sys
from typing import List
from resources import resources_rc
from utils.file_manager import FileManager, FileSystemObject
from utils.network_manager import NetworkManager
from custom_components.custom_completer import CustomCompleter
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,QMessageBox, QTreeWidget, QTreeWidgetItem

from PyQt5.QtCore import QDir, Qt
from flatten_json import flatten


class Workbench(QMainWindow):

    def __init__(self):
        super().__init__()

        # Remove unused pylint warning
        _ = resources_rc
        self.configuration = FileManager.deserialize_configuration_file("./workbench/config.yml")

        # Load the interface.ui file
        uic.loadUi('./workbench/interface.ui', self)

        self.custom_completer = CustomCompleter()
        # Connect uiBtnExecute to the onClickUiBtnExecuteEvent function
        self.uiBtnExecute.aboutToShow.connect(self.__on_uibtnexecute_clicked_event)

        # Connect uiBtnExit to the onClickUiBtnExitEvent function
        self.uiBtnExit.triggered.connect(self.__on_uibtnexit_clicked_event)

        # Set the column label for the uiTreeRules widget
        self.uiTreeRules.setHeaderLabels(['Name', 'Type'])

        # Register the double click event for the uiTreeRules item
        self.uiTreeRules.itemDoubleClicked.connect(self.__on_ui_tree_rules_item_double_clicked)

        # Register the double click event for the uiListFields item
        self.uiListFields.itemDoubleClicked.connect(self.__on_list_widget_item_double_clicked)

        # Populate the uiTreeRules Widget with the rule set
        self.__fill_tree_widget(self.uiTreeRules,
                                FileManager.generate_folder_tree(self.configuration["rules_path"]))

        # Instantiate the NetworkManager
        self.network_manager = NetworkManager(self, self.configuration["rumbledb"]["url"],
                                              self.configuration["rumbledb"]["materialization_cap"])
        self.network_manager.check_connection_signal.connect(self.handle_connection_check)
        self.network_manager.run_query_signal.connect(self.handle_run_query)
        self.network_manager.check_connection()

        self.verticalLayout_2.replaceWidget(self.uiTxtQuery, self.custom_completer)

        self.document_fields = None
        

    def __on_ui_tree_rules_item_double_clicked(self, item):
        if item.text(1) == "File":
            file_path = item.data(0, Qt.UserRole)
            self.custom_completer.setText(FileManager.read_file_content(file_path, 'r', 'utf-8'))
    
    def __on_list_widget_item_double_clicked(self, item):
        cursor = self.custom_completer.textCursor()
        #cursor.movePosition(cursor.End)
        self.custom_completer.setTextCursor(cursor)

        # Insert text at cursor position
        self.custom_completer.insertPlainText(item.text())

    def add_items_to_listwidget(self, list_widget, items):
        """
        Adds a list of strings to the specified QListWidget.

        Args:
        list_widget (QListWidget): The QListWidget instance to which the items will be added.
        items (list of str): A list of strings that will be added to the QListWidget.
        """
        list_widget.clear()
        for item in items:
            list_widget.addItem(item)   

    def __fill_tree_widget(self, ui_tree: QTreeWidget, elements_to_show: List[FileSystemObject]):
        """
        Populates the given QTreeWidget with items based on the provided elements.
        """
        for element in elements_to_show:
            item = QTreeWidgetItem()
            icon = ":/ico/ico_document.ico" if element.type == "File" else ":/ico/ico_binder.ico"
            item.setIcon(0, QIcon(icon))
            item.setText(0, QDir(element.path).dirName())
            item.setText(1, element.type)

            # Set custom data for item selection ( __on_ui_tree_rules_item_double_clicked )
            item.setData(0, Qt.UserRole, element.path)
            item.setData(1, Qt.UserRole, element.type)

            if isinstance(ui_tree, QTreeWidget):
                ui_tree.addTopLevelItem(item)
            elif isinstance(ui_tree, QTreeWidgetItem):
                ui_tree.addChild(item)

            if element.type == "Folder":
                self.__fill_tree_widget(item, element.children)

    def __on_uibtnexit_clicked_event(self):
        self.close()

    def __on_uibtnexecute_clicked_event(self):

        self.uiBtnExecute.setEnabled(False)
        self.network_manager.run_query(self.custom_completer.toPlainText())

    def handle_connection_check(self, success: bool):

        if not success:
            QMessageBox.critical(self,"Error","Backend not connected!")

    def handle_run_query(self, json_data) -> None:
        self.uiBtnExecute.setEnabled(True)

        # Checks if there are errors:
        if "error-code" in json_data:
            QMessageBox.critical(self, json_data["error-code"],json_data["error-message"])
            return

        if len(json_data['values']) > 0:

            # Prints a simple list
            if not isinstance(json_data['values'][0], dict):
                self.table.setRowCount(len(json_data['values']))
                self.table.setColumnCount(len(json_data))

                #if self.document_fields is None:
                self.document_fields = sorted(list(json_data.keys()))

                for col_num, header in enumerate(self.document_fields):
                    self.table.setHorizontalHeaderItem(col_num, QTableWidgetItem(header))
                for row_num, row_data in enumerate(json_data["values"]):
                    self.table.setItem(row_num, 0, QTableWidgetItem(str(row_data)))

            # Prints a list of objects
            if isinstance(json_data['values'][0], dict):
                json_data = [flatten(item,separator=".") for item in json_data['values']]
                if json_data:
                    self.table.setRowCount(len(json_data))
                    self.table.setColumnCount(len(json_data[0]))
                    
                    
                    self.document_fields = sorted(list({key for d in json_data for key in d.keys()}))
                    self.custom_completer.setWordlist(self.document_fields)
                    self.add_items_to_listwidget(self.uiListFields, self.document_fields)

                    for col_num, header in enumerate(self.document_fields):
                        self.table.setHorizontalHeaderItem(col_num, QTableWidgetItem(header))

                    for row_num, row_data in enumerate(json_data):
                        for col_num, key in enumerate(self.document_fields):
                            self.table.setItem(row_num, col_num, QTableWidgetItem(str(row_data.get(key, ''))))
        else:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            QMessageBox.information(self,"Info","No resultset found!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Workbench()
    ex.show()
    sys.exit(app.exec_())
