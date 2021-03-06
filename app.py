from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QFileInfo
from lib.mainwindow import MainWindow
from lib.dlg_license import Dlg_License
from lib.functions import verify_due_day, verify_license
import sys
import os
import ctypes
import traceback
import json
import base64


ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class MyApp(QMainWindow):
    '''
    :ivar windows: store existing MainWindow object.
    :vartype windows: [MainWindow]
    '''

    def __init__(self):
        super().__init__()
        self.windows = []
        self.key_valid = False
        self.create_document()
        self.create_mainwindow()

    def create_document(self) -> None:
        self.document = QMainWindow()
        browser = QWebEngineView()
        relative_html = './doc/build/html/index.html'
        fileurl = QUrl.fromLocalFile(
            QFileInfo(relative_html).absoluteFilePath())
        browser.load(fileurl)
        self.document.setCentralWidget(browser)
        self.document.setWindowTitle("Document")
        self.document.resize(1100, 600)

    def create_mainwindow(self, path: str = None) -> None:
        """
        Create a new Mainwindow object, and append it in the attrbute ``windows``.

        :param path: The absolute path to retrieve project file (*.pkl)
        """
        new_windows = MainWindow(app=self, project_path=path)
        self.windows.append(new_windows)
        new_windows.menutopbar.act_help.triggered.connect(self.show_document)

        new_windows.show()

    def show_document(self) -> None:
        """
        Show the document window.
        All mainwindow object in this app share the same document window.
        """
        self.document.show()


def load_conf():
    try:
        with open('./conf.txt') as f:
            code = f.readlines()[0]
            decode = base64.b64decode(code).decode("utf-8")
            conf = json.loads(decode)
    except Exception as e:
        conf = {"license": "", "license_due_day": "", "license_used": []}
        conf_str = json.dumps(conf)
        encode = base64.b64encode(conf_str.encode("utf-8"))
        with open("./conf.txt", "wb+") as file:
            file.write(encode)

    if "license" not in conf.keys():
        conf["license"] = ""
    if "license_due_day" not in conf.keys():
        conf["license_due_day"] = ""
    if "license_used" not in conf.keys():
        conf["license_used"] = []

    return conf


def check_license(conf):
    """
    Check the license.
    If the license doesn't exit or already expired, execute license comfirmation dialog.
    Otherwise, return True.
    """
    license_isvalid = verify_license(conf["license"])
    license_due_day = conf["license_due_day"]
    due_day_isvalid = verify_due_day(license_due_day)
    dlg_info = "Welcome to SAE PlotTool!\nPlease enter the license to execute the app."

    if license_isvalid and due_day_isvalid:
        print("App Execute!!\n")
        return True
    elif license_isvalid and not due_day_isvalid:
        dlg_info = "Oops! Original License was expired at %s.\n Please enter a new license." % license_due_day
        conf["license_used"].append(conf["license"])

    conf["license"] = ""
    dlg = Dlg_License(dlg_info=dlg_info, license_used=conf["license_used"])
    return dlg.exec_()


def main():
    print("app.main os.path.dirname(__file__)", os.path.dirname(__file__))
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            font-family: Arial;
        }
        QMainWindow {
            background-color: white;
            font-family: Arial;
        }
        QMainWindow QWidget#wg_central{
            background-color: #efefef;
            border: 2px solid #808080;
        }
        QDockWidget QWidget#wg_main {
            border-left: 2px solid #808080;
            border-bottom: 2px solid #808080;
            border-right: 2px solid #808080;
        }
        QMenuBar QMenu {
            padsa/ding: 2px 5px
        }
        QTabBar::scroller QToolButton  {
            background-color: white;
        }
        QLabel#warning_massage{
            background-color: #e80000;
            padding: 4px;
            color: "white";
        }
    """)
    conf = load_conf()
    if check_license(conf):
        try:
            MyApp()
            sys.exit(app.exec_())
        except Exception as e:
            error_class = e.__class__.__name__
            detail = e.args[0]
            cl, exc, tb = sys.exc_info()
            # print(cl, exc, tb)
            lastCallStack = traceback.extract_tb(tb)[-1]
            fileName = lastCallStack[0]
            lineName = lastCallStack[1]
            funcName = lastCallStack[2]
            print("#########  Error Message   #########\n")
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(
                fileName, lineName, funcName, error_class, detail)
            print(errMsg)
            print("\n####################################")
    else:
        return


if __name__ == '__main__':
    main()
