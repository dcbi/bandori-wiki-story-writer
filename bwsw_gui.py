import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QPushButton, QWidget, QLabel, QLineEdit, QGridLayout, QApplication, QHBoxLayout, QVBoxLayout, QFileDialog, QCheckBox, QMessageBox)
from pathlib import Path
from traceback import print_exc

short = {'kas':'kasumi', 'tae':'tae', 'rim':'rimi', 'say':'saaya', 'ari':'arisa',
'y':'yukina', 's':'sayo', 'l':'lisa', 'a':'ako', 'r':'rinko',
'aya':'aya', 'hin':'hina', 'chi':'chisato', 'may':'maya', 'eve':'eve',
'ran':'ran', 'moc':'moca', 'him':'himari', 'tom':'tomoe', 'tsu':'tsugumi',
'kok':'kokoro', 'kao':'kaoru', 'hag':'hagumi', 'kan':'kanon', 'mis':'misaki', 'mar':'marina',
'mash': 'mashiro', 'tok': 'touko', 'nan': 'nanami', 'tsuk': 'tsukushi', 'rui': 'rui'}

def checkName(NAME):
    name = NAME.lower()
    if name in list(short.keys()):
        return short[name]
    elif name in list(short.values()):
        return name
    else:
        return NAME

class Slash(Exception): pass

skip = ['-'*10 + 'SKIPPED LINE' + '-'*10]

def main(f1, f2, expand):
    if expand: f2.write('<div class="mw-collapsible mw-collapsed">\n')

    writeNew = ''

    for line in f1:
        l = line.strip()
        if l == '':
            f2.write('<br />\n')
            continue

        elif '/' in l:
            try:
                tag = l.split('/')
                if tag[0] == '':
                    if tag[1] == '':
                        writeNew = '{{dialog|others|[line]|' + tag[2] + '}}\n'
                    else:
                        writeNew = '{{dialog|' + checkName(tag[1]) + '|[line]}}\n'
                else:
                    if tag[1] == '': f2.write('{{loc|' + tag[0] + '}}\n')
                    else: raise Slash
                continue

            except Slash:
                msg = QMessageBox()
                msg.setWindowTitle('Slash Error')
                msg.setIcon(QMessageBox.Warning)
                msg.setText('Detected possible slash "/" in dialog or loc text. Check console.')
                msg.exec()
                print('LINE: ' + l)
                cont = input('SELECT: (1) loc, (2) dialog\n--> ')
                if cont == '1':
                    f2.write('{{loc|' + l[:len(line)-1] + '}}\n')
                elif cont == '2':
                    f2.write( writeNew.replace('[line]', l.replace('[you]', '{{USERNAME}}-san')) )
                else:
                    f2.write(skip[0])
                    skip.append(l)
                continue

        else:
            try:
                f2.write( writeNew.replace('[line]', l.replace('[you]', '{{USERNAME}}-san')) )
            except UnicodeError:
                skip.append(l)
                f2.write(skip[0])
                continue

    if expand: f2.write('</div>')

    num_errors = len(skip)-1
    if num_errors > 0:
        msg = QMessageBox()
        msg.setWindowTitle('Errors')
        msg.setIcon(QMessageBox.Warning)
        for i in range(1,len(skip)): print(skip[i])
        msg.setText(str(num_errors) + ' line(s) skipped. Check console and fix output file manually.')
        msg.exec()

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'Bandori Wiki Story Writer'
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 200
        self.initUI()

    def initUI(self):
        font=QtGui.QFont()
        font.setPixelSize(25)

        self.readFileLabel = QLabel('Transcript File')
        self.readFileLoadEdit = QLineEdit(self)
        self.readFileLoadEdit.setPlaceholderText('File path')
        self.loadButton = QPushButton('Load file', self)
        self.loadButton.clicked.connect(self.openFile)

        self.writeFileLabel = QLabel('Output File')
        self.writeFileNameEdit = QLineEdit(self)
        self.writeFileNameEdit.setPlaceholderText('File name')
        self.folderLabel = QLabel('Folder to save file in')
        self.folderNameEdit = QLineEdit(self)
        self.folderNameEdit.setPlaceholderText('Folder path')
        self.selectFolderButton = QPushButton('Select Folder', self)
        self.selectFolderButton.clicked.connect(self.openFolder)

        self.expand = QCheckBox('Include expand wrapper')

        self.startButton = QPushButton('Run', self)
        self.startButton.clicked.connect(self.start)
        self.stopButton = QPushButton('Exit', self)
        self.stopButton.clicked.connect(self.stop)

        mainhbox = QHBoxLayout(self)

        fileloadbox = QHBoxLayout(self)
        fileloadbox.addWidget(self.readFileLoadEdit)
        fileloadbox.addWidget(self.loadButton)

        folderloadbox = QHBoxLayout(self)
        folderloadbox.addWidget(self.folderNameEdit)
        folderloadbox.addWidget(self.selectFolderButton)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.readFileLabel)
        vbox.addLayout(fileloadbox)
        vbox.addWidget(self.writeFileLabel)
        vbox.addLayout(folderloadbox)
        vbox.addWidget(self.writeFileNameEdit)
        vbox.addWidget(self.expand)

        hbox = QHBoxLayout(self)
        hbox.addStretch(1)
        hbox.addWidget(self.stopButton)
        hbox.addWidget(self.startButton)
        hbox.addStretch()
        vbox.addLayout(hbox)
        vbox.addStretch()

        mainhbox.addLayout(vbox)

        self.setLayout(mainhbox)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Select File')
        self.readFileLoadEdit.setText(filename[0])

    def openFolder(self):
        dlg = QFileDialog(self, 'Select folder')
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.folderNameEdit.setText(filenames[0])

    def start(self):

        readfile = self.readFileLoadEdit.text()
        writefile = ''

        if self.folderNameEdit.text() == '':
            writefile = str(Path(readfile).parent) + '\\'
        else:
            writefile = self.folderNameEdit.text() + '/'

        if self.writeFileNameEdit.text() == '':
            writefile = writefile + 'wikicode.txt'
        else:
            writefile = writefile + self.writeFileNameEdit.text() + '.txt'

        with open(readfile, 'r') as f1, open(writefile, 'w') as f2:
            try: main(f1, f2, self.expand.isChecked())
            except:
                print_exc()
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setIcon(QMessageBox.Warning)
                msg.setText('An error occured. Please check console for info.')
                msg.exec()
            else:
                msg = QMessageBox()
                msg.setWindowTitle('Run')
                msg.setText('Read: ' + readfile + '\nWrite: ' + writefile + '\nSuccess!')
                msg.exec()

    def stop(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
