import argparse
from pathlib import Path

parent_dir = str(Path(__file__).parent.absolute())

parser = argparse.ArgumentParser()

parser.add_argument('-path', help="parent directory of files to read and write, default="+parent_dir, default=parent_dir)
parser.add_argument('-readname', help='name of file to read from, default=transcript', default='transcript')
parser.add_argument('-writename', help='name of file to write to, default=wiki', default='wikicode')
parser.add_argument('-gui', action='store_true')
parser.add_argument('-abbrev', action='store_true')
parser.add_argument('-expand', action='store_true')

args = parser.parse_args()

short = {'kas':'kasumi', 'tae':'tae', 'rim':'rimi', 'say':'saaya', 'ari':'arisa', 'y':'yukina', 's':'sayo', 'l':'lisa', 'a':'ako', 'r':'rinko', 'aya':'aya', 'hin':'hina', 'chi':'chisato', 'may':'maya', 'eve':'eve', 'ran':'ran', 'moc':'moca', 'him':'himari', 'tom':'tomoe', 'tsu':'tsugumi', 'kok':'kokoro', 'kao':'kaoru', 'hag':'hagumi', 'kan':'kanon', 'mis':'misaki', 'mar':'marina'}

def process(name, abb):
	if abb: return short[name]
	else: return name

class Slash(Exception): pass

def main(f1, f2, abb, expand):
	if expand: f2.write('<div class="mw-collapsible mw-collapsed">\n')

	skip = ['-'*10 + 'SKIPPED LINE' + '-'*10, 0]

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
						writeNew = '{{dialog|' + process(tag[1].lower(), abb) + '|[line]}}\n'
				else:
					if tag[1] == '': f2.write('{{loc|' + tag[0] + '}}\n')
					else: raise Slash
				continue

			except Slash:
				print('\nDetected possible slash "/" in dialog or loc text.')
				print('LINE: ' + l)
				cont = input('Select: (0) neither, (1) loc, (2) dialog\n--> ')
				if cont == '0':
					f2.write(skip[0])
					skip[1] += 1
				elif cont == '1':
					f2.write('{{loc|' + line.strip()[:len(line)-1] + '}}\n')
				elif cont == '2':
					f2.write( writeNew.replace('[line]', l.replace('[you]', '{{USERNAME}}-san')) )
				else:
					print('INVALID INPUT.')
					f2.write(skip[0])
					skip[1] += 1
				continue
		else:
			try:
				f2.write( writeNew.replace('[line]', l.replace('[you]', '{{USERNAME}}-san')) )
			except UnicodeError:
				print('Possible special character. Check transcript file.')
				f2.write(skip[0])
				skip[1] += 1
				continue

	if expand: f2.write('</div>')

	if not skip[1] == 0: print(str(skip[1]) + ' line(s) skipped. Fix output file manually.')

if args.ui:
	import sys
	from PyQt5 import QtGui, QtCore
	from PyQt5.QtWidgets import (QPushButton, QWidget, QLabel, QLineEdit, QGridLayout, QApplication, QHBoxLayout, QVBoxLayout, QFileDialog, QCheckBox)

	writeFileName = None

	class MyApp(QWidget):
		def __init__(self):
			super().__init__()

			self.title = 'Bandori Wiki Story Writer'
			self.left = 10
			self.top = 10
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

			self.abbreviation = QCheckBox('Use abbreviations')
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
			vbox.addWidget(self.abbreviation)
			vbox.addWidget(self.expand)

			buttonsbox = QHBoxLayout(self)
			buttonsbox.addStretch(1)
			buttonsbox.addWidget(self.stopButton)
			buttonsbox.addWidget(self.startButton)
			buttonsbox.addStretch()

			vbox.addLayout(buttonsbox)
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

		def stop(self):
			self.close()

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
				main(f1, f2, self.abbreviation.isChecked(), self.expand.isChecked())

			print('Read: ' + readfile + '\nWrite: ' + writefile)


	if __name__ == '__main__':
		app = QApplication(sys.argv)
		ex = MyApp()
		sys.exit(app.exec_())

else:
	with open(args.path + '\\' + args.readname + '.txt', 'r') as f1, open(args.path + '\\' + args.writename + '.txt', 'w') as f2:
		main(f1, f2, args.abbrev, args.expand)
