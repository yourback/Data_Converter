import binascii
import sys, os, time

from PyQt5.QtWidgets import *

from transDemo_rc import Ui_MainWindow

from PyQt5.QtCore import *

from concurrent.futures import ThreadPoolExecutor

from data_process import word_num, byte_num


class transprogram(QMainWindow, Ui_MainWindow):
    btn_setsource = pyqtSignal()
    btn_setdest = pyqtSignal()

    # 转换完成信号
    trans_finish = pyqtSignal()
    # 单文件转换完成信号
    single_trans_finish = pyqtSignal(int)

    def __init__(self, parent=None):
        super(transprogram, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.executor = ThreadPoolExecutor(max_workers=1)

    def initUI(self):
        # 进度归零
        self.pb_transform.setValue(0)
        # 设置监听
        self.init_listener()

    def begin_transform(self):
        # 进度归零
        self.pb_transform.setValue(0)
        # print('开始转换')
        if not self.et_source.text() or not self.et_dest.text():
            # print('没有文件夹')
            self.box_information("请先选择源文件夹与目的文件夹")
        else:
            # print('已经选择了文件夹')
            # 判断源文件夹中有没有TXT文件

            filenames = []
            i = 1
            for file_name in os.listdir(self.et_source.text()):
                if file_name.endswith("txt") or file_name.endswith('TXT'):
                    d = dict()
                    d['name'] = file_name
                    d['path'] = self.et_source.text() + '/' + file_name
                    d['index'] = i
                    i += 1
                    filenames.append(d)

            if not filenames:
                self.box_information('没有TXT文档可以转换')
            else:
                self.files_size = len(filenames)

                self.pb_transform.setRange(0, self.files_size)

                self.executor.map(self.trans_files, filenames)

    def box_information(self, msg):
        QMessageBox.information(self, "提示", msg, QMessageBox.Ok, QMessageBox.Ok)

    def trans_files(self, file_dict):
        # 当前转换文件名称：
        file_name = file_dict['name']
        file_path = file_dict['path']
        file_index = file_dict['index']

        # print('当前处理文件：%s' % file_dict['name'])
        # 目的目录
        # self.et_dest.text()

        # 新文件目录
        new_file_path = self.et_dest.text() + '/trans_' + file_name

        # print('新文件夹的路径', new_file_path)

        self.old2new(file_path, new_file_path)

        # self.et_transforming.setText("%i/%i" % (file_dict['index'], self.files_size))
        self.et_transforming.setText(file_name[:file_name.rindex('.')])

        self.single_trans_finish.emit(int(file_index))

        if file_index == self.files_size:
            self.trans_finish.emit()

    # 转换完成后的操作
    def trans_over(self):
        self.box_information('转换完成')
        self.et_transforming.setText('')
        self.et_dest.setText('')
        self.et_source.setText('')
        self.pb_transform.setValue(0)

    # 单个文件转换完成后的操作
    def single_trans_over(self, i):
        self.pb_transform.setValue(i)

    def old2new(self, old_path, new_path):
        old_file = open(old_path, 'r+', encoding='utf-8')
        new_file = open(new_path, 'w+', encoding='utf-8')
        new_file.write('LD       LU       RD       RU       Ctrl     UDM\n')
        while True:
            line_str = old_file.readline().strip()
            print('读取一行信息：', line_str)
            if not line_str:
                break
            if '[' in line_str:
                str = line_str[:line_str.rindex('[')].replace(' ', '')
            else:
                str = line_str
            # print('读取数据长度：', len(line_str))
            if len(str) != 74:
                # print('数据长度有误')
                continue
            LD = word_num(str[0:4], str[18:22]).__str__().ljust(7)
            LU = word_num(str[4:8], str[22:26]).__str__().ljust(7)
            RD = word_num(str[8:12], str[26:30]).__str__().ljust(7)
            RU = word_num(str[12:16], str[30:34]).__str__().ljust(7)
            E = byte_num(str[16:18], str[34:36]).__str__().ljust(7)
            J = byte_num(str[-6:-4], '00')
            new_file.write('%s  %s  %s  %s  %s  %s\n' % (LD, LU, RD, RU, E, J))

        old_file.close()
        new_file.close()

    def set_sourcefile(self):
        # print("设置源文件夹")
        sourcedlg = QFileDialog()
        sourcedlg.setFileMode(QFileDialog.Directory)
        sourcedlg.setFilter(QDir.Files)

        if sourcedlg.exec_():
            source_file_name = sourcedlg.selectedFiles()
            # print(source_file_name)
            self.et_source.setText(source_file_name[0])

    def set_destfile(self):
        # print("设置目的文件夹")
        destdlg = QFileDialog()
        destdlg.setFileMode(QFileDialog.Directory)
        destdlg.setFilter(QDir.Files)

        if destdlg.exec_():
            dest_file_name = destdlg.selectedFiles()
            # print(source_file_name)
            self.et_dest.setText(dest_file_name[0])

    def init_listener(self):
        # 设置源
        self.btn_setsource.clicked.connect(self.set_sourcefile)
        # 设置目的
        self.btn_setdest.clicked.connect(self.set_destfile)
        # 设置开始转换
        self.btn_trans_begin.clicked.connect(self.begin_transform)
        # 设置转换完成
        self.trans_finish.connect(self.trans_over)
        # 源输入框
        self.et_source.clicked.connect(self.set_sourcefile)
        # 目的输入框
        self.et_dest.clicked.connect(self.set_destfile)
        # 设置单个文件转换完成
        self.single_trans_finish.connect(self.single_trans_over)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = transprogram()

    win.show()

    sys.exit(app.exec_())
