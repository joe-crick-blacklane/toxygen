# -*- coding: utf-8 -*-

from menu import *
from profile import *
from list_items import *


class MessageArea(QtGui.QPlainTextEdit):

    def __init__(self, parent, form):
        super(MessageArea, self).__init__(parent)
        self.parent = form

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.parent.send_message()
        else:
            super(self.__class__, self).keyPressEvent(event)


class MainWindow(QtGui.QMainWindow):

    def __init__(self, tox):
        super(MainWindow, self).__init__()
        self.tox = tox
        self.initUI()

    def setup_menu(self, MainWindow):
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setNativeMenuBar(False)
        self.menubar.setMinimumSize(self.width(), 25)
        self.menubar.setMaximumSize(self.width(), 25)
        self.menubar.setBaseSize(self.width(), 25)
        self.menuProfile = QtGui.QMenu(self.menubar)
        self.menuProfile.setObjectName("menuProfile")
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.actionAdd_friend = QtGui.QAction(MainWindow)
        self.actionAdd_friend.setObjectName("actionAdd_friend")
        self.actionProfile_settings = QtGui.QAction(MainWindow)
        self.actionProfile_settings.setObjectName("actionProfile_settings")
        self.actionPrivacy_settings = QtGui.QAction(MainWindow)
        self.actionPrivacy_settings.setObjectName("actionPrivacy_settings")
        self.actionInterface_settings = QtGui.QAction(MainWindow)
        self.actionInterface_settings.setObjectName("actionInterface_settings")
        self.actionNotifications = QtGui.QAction(MainWindow)
        self.actionNotifications.setObjectName("actionNotifications")
        self.actionNetwork = QtGui.QAction(MainWindow)
        self.actionNetwork.setObjectName("actionNetwork")
        self.actionAbout_program = QtGui.QAction(MainWindow)
        self.actionAbout_program.setObjectName("actionAbout_program")
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuProfile.addAction(self.actionAdd_friend)
        self.menuProfile.addAction(self.actionSettings)
        self.menuSettings.addAction(self.actionPrivacy_settings)
        self.menuSettings.addAction(self.actionInterface_settings)
        self.menuSettings.addAction(self.actionNotifications)
        self.menuSettings.addAction(self.actionNetwork)
        self.menuAbout.addAction(self.actionAbout_program)
        self.menubar.addAction(self.menuProfile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.actionAbout_program.triggered.connect(self.about_program)
        self.actionNetwork.triggered.connect(self.network_settings)
        self.actionAdd_friend.triggered.connect(self.add_contact)
        self.actionSettings.triggered.connect(self.profile_settings)
        self.actionPrivacy_settings.triggered.connect(self.privacy_settings)
        self.actionInterface_settings.triggered.connect(self.interface_settings)
        self.actionNotifications.triggered.connect(self.notification_settings)

        self.menuProfile.setTitle(QtGui.QApplication.translate("MainWindow", "Profile", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSettings.setTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_friend.setText(QtGui.QApplication.translate("MainWindow", "Add contact", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProfile_settings.setText(QtGui.QApplication.translate("MainWindow", "Profile", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrivacy_settings.setText(QtGui.QApplication.translate("MainWindow", "Privacy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInterface_settings.setText(QtGui.QApplication.translate("MainWindow", "Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNotifications.setText(QtGui.QApplication.translate("MainWindow", "Notifications", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNetwork.setText(QtGui.QApplication.translate("MainWindow", "Network", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_program.setText(QtGui.QApplication.translate("MainWindow", "About program", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup_right_bottom(self, Form):
        Form.setObjectName("right_bottom")
        Form.resize(650, 100)
        self.messageEdit = MessageArea(Form, self)
        self.messageEdit.setGeometry(QtCore.QRect(0, 10, 450, 110))
        self.messageEdit.setObjectName("messageEdit")
        self.screenshotButton = QtGui.QPushButton(Form)
        self.screenshotButton.setGeometry(QtCore.QRect(460, 10, 90, 50))
        self.screenshotButton.setObjectName("screenshotButton")
        self.fileTransferButton = QtGui.QPushButton(Form)
        self.fileTransferButton.setGeometry(QtCore.QRect(460, 70, 90, 50))
        self.fileTransferButton.setObjectName("fileTransferButton")
        self.sendMessageButton = QtGui.QPushButton(Form)
        self.sendMessageButton.setGeometry(QtCore.QRect(550, 10, 60, 110))
        self.sendMessageButton.setObjectName("sendMessageButton")
        self.sendMessageButton.clicked.connect(self.send_message)
        self.screenshotButton.setText(QtGui.QApplication.translate("Form", "Screenshot", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTransferButton.setText(QtGui.QApplication.translate("Form", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.sendMessageButton.setText(QtGui.QApplication.translate("Form", "Send", None, QtGui.QApplication.UnicodeUTF8))
        QtCore.QMetaObject.connectSlotsByName(Form)

    def setup_left_bottom(self, Form):
        Form.setObjectName("left_bottom")
        Form.resize(500, 80)
        self.online_contacts = QtGui.QCheckBox(Form)
        self.online_contacts.setGeometry(QtCore.QRect(0, 20, 141, 22))
        self.online_contacts.setObjectName("online_contacts")
        self.online_contacts.clicked.connect(self.filtering)
        self.contact_name = QtGui.QLineEdit(Form)
        self.contact_name.setGeometry(QtCore.QRect(0, 40, 140, 28))
        self.contact_name.setObjectName("contact_name")
        self.contact_name.textChanged.connect(self.filtering)
        self.online_contacts.setText(QtGui.QApplication.translate("Form", "Online contacts", None, QtGui.QApplication.UnicodeUTF8))
        QtCore.QMetaObject.connectSlotsByName(Form)

    def setup_left_top(self, Form):
        Form.setObjectName("left_top")
        Form.resize(500, 300)
        Form.setCursor(QtCore.Qt.PointingHandCursor)
        Form.setMinimumSize(QtCore.QSize(250, 100))
        Form.setMaximumSize(QtCore.QSize(250, 100))
        Form.setBaseSize(QtCore.QSize(250, 100))
        self.avatar_label = Form.avatar_label = QtGui.QLabel(Form)
        self.avatar_label.setGeometry(QtCore.QRect(10, 20, 64, 64))
        self.avatar_label.setScaledContents(True)
        self.name = Form.name = QtGui.QLabel(Form)
        Form.name.setGeometry(QtCore.QRect(80, 30, 120, 25))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        Form.name.setFont(font)
        Form.name.setObjectName("name")
        self.status_message = Form.status_message = QtGui.QLabel(Form)
        Form.status_message.setGeometry(QtCore.QRect(80, 60, 190, 20))
        font.setPointSize(12)
        font.setBold(False)
        Form.status_message.setFont(font)
        Form.status_message.setObjectName("status_message")
        self.connection_status = Form.connection_status = StatusCircle(self)
        Form.connection_status.setGeometry(QtCore.QRect(200, 34, 64, 64))
        Form.connection_status.setMinimumSize(QtCore.QSize(32, 32))
        Form.connection_status.setMaximumSize(QtCore.QSize(32, 32))
        Form.connection_status.setBaseSize(QtCore.QSize(32, 32))
        self.avatar_label.mouseReleaseEvent = self.profile_settings
        self.status_message.mouseReleaseEvent = self.profile_settings
        self.name.mouseReleaseEvent = self.profile_settings
        self.connection_status.raise_()
        Form.connection_status.setObjectName("connection_status")

    def setup_right_top(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 300)
        self.account_avatar = QtGui.QLabel(Form)
        self.account_avatar.setGeometry(QtCore.QRect(10, 20, 64, 64))
        self.account_avatar.setScaledContents(True)
        self.account_name = QtGui.QLabel(Form)
        self.account_name.setGeometry(QtCore.QRect(100, 30, 400, 25))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        self.account_name.setFont(font)
        self.account_name.setObjectName("account_name")
        self.account_status = QtGui.QLabel(Form)
        self.account_status.setGeometry(QtCore.QRect(100, 50, 400, 25))
        font.setPointSize(12)
        font.setBold(False)
        self.account_status.setFont(font)
        self.account_status.setObjectName("account_status")
        self.callButton = QtGui.QPushButton(Form)
        self.callButton.setGeometry(QtCore.QRect(550, 30, 75, 30))
        self.callButton.setObjectName("callButton")
        self.callButton.setText(QtGui.QApplication.translate("Form", "Start call", None, QtGui.QApplication.UnicodeUTF8))
        QtCore.QMetaObject.connectSlotsByName(Form)

    def setup_left_center(self, widget):
        self.friends_list = QtGui.QListWidget(widget)
        self.friends_list.setGeometry(0, 0, 250, 250)
        self.friends_list.clicked.connect(self.friend_click)
        self.friends_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.friends_list.connect(self.friends_list, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                  self.friend_right_click)

    def setup_right_center(self, widget):
        self.messages = QtGui.QListWidget(widget)
        self.messages.setGeometry(0, 0, 600, 250)

    def initUI(self):
        self.setMinimumSize(900, 550)
        self.setMaximumSize(900, 550)
        self.setGeometry(400, 400, 900, 550)
        self.setWindowTitle('Toxygen')
        main = QtGui.QWidget()
        grid = QtGui.QGridLayout()
        search = QtGui.QWidget()
        self.setup_left_bottom(search)
        grid.addWidget(search, 2, 0)
        name = QtGui.QWidget()
        self.setup_left_top(name)
        grid.addWidget(name, 0, 0)
        messages = QtGui.QWidget()
        self.setup_right_center(messages)
        grid.addWidget(messages, 1, 1)
        info = QtGui.QWidget()
        self.setup_right_top(info)
        grid.addWidget(info, 0, 1)
        message_buttons = QtGui.QWidget()
        self.setup_right_bottom(message_buttons)
        grid.addWidget(message_buttons, 2, 1)
        main_list = QtGui.QWidget()
        self.setup_left_center(main_list)
        grid.addWidget(main_list, 1, 0)
        grid.setColumnMinimumWidth(1, 500)
        grid.setColumnMinimumWidth(0, 250)
        grid.setRowMinimumHeight(1, 250)
        main.setLayout(grid)
        self.setCentralWidget(main)
        self.setup_menu(self)
        self.user_info = name
        self.friend_info = info
        self.profile = Profile(self.tox, self)

    def closeEvent(self, *args, **kwargs):
        self.profile.save_history()

    # -----------------------------------------------------------------------------------------------------------------
    # Functions which called when user click in menu
    # -----------------------------------------------------------------------------------------------------------------

    def about_program(self):
        import util
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("About")
        msgBox.setText("Toxygen is pythonic Tox client. Version: " + util.program_version)
        msgBox.exec_()

    def network_settings(self):
        self.n_s = NetworkSettings()
        self.n_s.show()

    def add_contact(self):
        self.a_c = AddContact()
        self.a_c.show()

    def profile_settings(self, *args):
        self.p_s = ProfileSettings()
        self.p_s.show()

    def privacy_settings(self):
        self.priv_s = PrivacySettings()
        self.priv_s.show()

    def notification_settings(self):
        self.notif_s = NotificationsSettings()
        self.notif_s.show()

    def interface_settings(self):
        self.int_s = InterfaceSettings()
        self.int_s.show()

    # -----------------------------------------------------------------------------------------------------------------
    # Messages
    # -----------------------------------------------------------------------------------------------------------------

    def send_message(self):
        text = self.messageEdit.toPlainText()
        self.profile.send_message(text)

    # -----------------------------------------------------------------------------------------------------------------
    # Functions which called when user open context menu in friends list
    # -----------------------------------------------------------------------------------------------------------------

    def friend_right_click(self, pos):
        item = self.friends_list.itemAt(pos)
        if item is not None:
            self.listMenu = QtGui.QMenu()
            set_alias_item = self.listMenu.addAction('Set alias')
            clear_history_item = self.listMenu.addAction('Clear history')
            copy_key_item = self.listMenu.addAction('Copy public key')
            remove_item = self.listMenu.addAction('Remove friend')
            self.connect(set_alias_item, QtCore.SIGNAL("triggered()"), lambda: self.set_alias(item))
            self.connect(remove_item, QtCore.SIGNAL("triggered()"), lambda: self.remove_friend(item))
            self.connect(copy_key_item, QtCore.SIGNAL("triggered()"), lambda: self.copy_friend_key(item))
            self.connect(clear_history_item, QtCore.SIGNAL("triggered()"), lambda: self.clear_history(item))
            parent_position = self.friends_list.mapToGlobal(QtCore.QPoint(0, 0))
            self.listMenu.move(parent_position + pos)
            self.listMenu.show()

    def set_alias(self, item):
        num = self.friends_list.indexFromItem(item).row()
        self.profile.set_alias(num)

    def remove_friend(self, item):
        num = self.friends_list.indexFromItem(item).row()
        self.profile.delete_friend(num)

    def copy_friend_key(self, item):
        num = self.friends_list.indexFromItem(item).row()
        tox_id = self.profile.friend_public_key(num)
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(tox_id)

    def clear_history(self, item):
        num = self.friends_list.indexFromItem(item).row()
        self.profile.clear_history(num)

    # -----------------------------------------------------------------------------------------------------------------
    # Functions which called when user click somewhere else
    # -----------------------------------------------------------------------------------------------------------------

    def friend_click(self, index):
        print 'row:', index.row()
        num = index.row()
        self.profile.set_active(num)

    def mouseReleaseEvent(self, event):
        x, y = event.x(), event.y()
        pos = self.connection_status.pos()
        if (pos.x() < x < pos.x() + 32) and (pos.y() < y < pos.y() + 32):
            self.profile.change_status()
        else:
            super(self.__class__, self).mouseReleaseEvent(event)

    def filtering(self):
        self.profile.filtration(self.online_contacts.isChecked(), self.contact_name.text())


