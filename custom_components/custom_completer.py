import sys
from typing import List
from PyQt5.QtWidgets import QTextEdit, QCompleter
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtGui import QTextCursor
from typing import List

class CustomCompleter(QTextEdit):
    def __init__(self):
        super().__init__()
        
        #self.initUI()
        # Create a list of words for auto-completion
        self.wordList = []

        # Create a completer with the word list
        self.model = QStringListModel(self.wordList, self)
        self.completer = QCompleter(self.model, self)

        self.setCompleter(self.completer)

    def setWordlist(self, wordlist):

        self.model = QStringListModel(wordlist, self)
        self.completer.setModel(self.model)
        self.style = self.window().styleSheet()
        self.completer.popup().setStyleSheet(self.style)

        #self.setCompleter(self.completer)

    def setCompleter(self, completer):
        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(False)
        completer.activated[str].connect(self.insertCompletion)
        self.completer = completer

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        textCursor = self.textCursor()
        textCursor.select(QTextCursor.WordUnderCursor)
        return textCursor.selectedText()

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in {Qt.Key_Return, Qt.Key_Enter, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab}:
                event.ignore()
                return
            # Allow normal character input
            if event.text() and len(event.text().strip()) > 0:
                super().keyPressEvent(event)
                self.completer.setCompletionPrefix(self.textUnderCursor())
                cursorRect = self.cursorRect()
                cursorRect.setWidth(self.completer.popup().sizeHintForColumn(0)
                                    + self.completer.popup().verticalScrollBar().sizeHint().width())
                self.completer.complete(cursorRect)
                return
            elif event.key() == Qt.Key_Backspace:
                super().keyPressEvent(event)
                self.completer.setCompletionPrefix(self.textUnderCursor())
                cursorRect = self.cursorRect()
                cursorRect.setWidth(self.completer.popup().sizeHintForColumn(0)
                                    + self.completer.popup().verticalScrollBar().sizeHint().width())
                self.completer.complete(cursorRect)
                return
            else:
                super(QTextEdit, self).keyPressEvent(event)
                return

        # Let the QTextEdit handle the event first; we'll handle completions afterward
        super().keyPressEvent(event)

        completionPrefix = self.textUnderCursor()

        # If the completionPrefix is empty or has space, then ignore
        if not completionPrefix or " " in completionPrefix:
            self.completer.popup().hide()
            return

        # This condition checks if the current prefix has a valid completion or not
        if (completionPrefix != self.completer.completionPrefix() and
                any(word.startswith(completionPrefix) for word in self.model.stringList())):
            self.completer.setCompletionPrefix(completionPrefix)
            self.completer.popup().setCurrentIndex(
                self.completer.completionModel().index(0, 0))

            cursorRect = self.cursorRect()
            cursorRect.setWidth(self.completer.popup().sizeHintForColumn(0)
                                + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cursorRect)
        elif not self.completer.completionCount():
            self.completer.popup().hide()