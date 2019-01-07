from welcomeView import *

from transDemo import *


class Main_Transform(object):

    def __init__(self):
        self.tran = transprogram()

        self.wel = WelcomeWindow()

        self.wel.fade_over.connect(self.welend)

    def begin(self):
        self.wel.show()

    def welend(self):
        self.tran.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_trans = Main_Transform()

    main_trans.begin()

    sys.exit(app.exec_())
