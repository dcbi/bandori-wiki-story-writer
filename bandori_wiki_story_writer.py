import argparse
from pathlib import Path

parent_dir = str(Path(__file__).parent.absolute())

parser = argparse.ArgumentParser()

parser.add_argument('-path', help="parent directory of files to read and write, default="+parent_dir, default=parent_dir)
parser.add_argument('-readname', help='name of file to read from, default=transcript', default='transcript')
parser.add_argument('-writename', help='name of file to write to, default=wiki', default='wiki')
parser.add_argument('-ui', action='store_true')
parser.add_argument('-abbrev', action='store_true')
parser.add_argument('-expand', action='store_true')

args = parser.parse_args()

short = {'kas':'kasumi', 'tae':'tae', 'rim':'rimi', 'say':'saaya', 'ari':'arisa', 'y':'yukina', 's':'sayo', 'l':'lisa', 'a':'ako', 'r':'rinko', 'aya':'aya', 'hin':'hina', 'chi':'chisato', 'may':'maya', 'eve':'eve', 'ran':'ran', 'moc':'moca', 'him':'himari', 'tom':'tomoe', 'tsu':'tsugumi', 'kok':'kokoro', 'kao':'kaoru', 'hag':'hagumi', 'kan':'kanon', 'mis':'misaki', 'mar':'marina'}

def process(name, abbrev):
	if abbrev: return short[name]
	else: return name

class Slash(Exception): pass

def main(f1, f2, expand):
	if expand: f2.write('<div class="mw-collapsible mw-collapsed">\n')

	skip = ['-'*10 + 'SKIPPED LINE' + '-'*10, 0]

	writeNew = ''

	for line in f1:
		if '/' in line:
			try:
				tag = line.split('/')
				if tag[0] == ' ': f2.write('<br />\n')
				elif tag[0] == '':
					if tag[1] == '': writeNew = '{{dialog|others|[line]|' + line.strip().replace('/','') + '}}\n'
					else: writeNew = '{{dialog|' + process(tag[1].strip().lower(), args.abbrev) + '|[line]}}\n'
				else:
					if tag[1].strip() == '': f2.write('{{loc|' + tag[0] + '}}\n')
					else: raise Slash()
				continue
			except Slash:
				print('\nDetected possible slash "/" in dialog or loc text.')
				print('LINE: ' + line.strip())
				cont = input('Select: (0) neither, (1) loc, (2) dialog\n--> ')
				if cont == '0':
					f2.write(skip[0])
					skip[1] += 1
				elif cont == '1':
					f2.write('{{loc|' + line[:len(line)-1] + '}}\n')
				elif cont == '2':
					f2.write( writeNew.replace('[line]', line.strip().replace('[you]', '{{USERNAME}}-san')) )
				else:
					print('INVALID INPUT.')
					f2.write(skip[0])
					skip[1] += 1
				continue
		else:
			try:
				f2.write( writeNew.replace('[line]', line.strip().replace('[you]', '{{USERNAME}}-san')) )
			except UnicodeError:
				print('Possible special character. Check transcript file.')
				f2.write(skip[0])
				skip[1] += 1
				continue

	if expand: f2.write('</div>')

	if not skip[1] == 0: print(str(skip[1]) + '\nline(s) skipped. Fix output file manually.')

if args.ui:
	import sys
	from PyQt5.QtWidgets import (QPushButton, QWidget, QLabel, QLineEdit, QGridLayout, QApplication, QHBoxLayout, QVBoxLayout,
	    QFileDialog)
	from pyqtgraph.Qt import QtGui, QtCore
	from PyQt5.QtGui import QIcon

	writeFileName = None

	class MyApp(QWidget):
		def __init__(self):
			super().__init__()

			self.title = 'Bandori Wiki Story Writer'
			self.left = 10
			self.top = 10
			self.width = 500
			self.height = 200
			self.initUI()

		def initUI(self):
			font=QtGui.QFont()
			font.setPixelSize(25)

			self.readFileNameLabel = QLabel('Path of file to read')
			self.fileLoadEdit = QLineEdit(self)
			self.loadButton = QPushButton('Select', self)
			self.loadButton.clicked.connect(self.openFile)

			self.writeFileNameLabel = QLabel('Name of file to write')
			self.writeFileNameEdit = QLineEdit(self)

			self.startButton = QPushButton('Run', self)
			self.startButton.clicked.connect(self.start)
			self.stopButton = QPushButton('Exit', self)
			self.stopButton.clicked.connect(self.stop)

			mainhbox = QHBoxLayout(self)

			fileloadbox = QHBoxLayout(self)
			fileloadbox.addWidget(self.fileLoadEdit)
			fileloadbox.addWidget(self.loadButton)

			vbox = QVBoxLayout(self)
			vbox.addWidget(self.readFileNameLabel)
			vbox.addLayout(fileloadbox)
			vbox.addWidget(self.writeFileNameLabel)
			vbox.addWidget(self.writeFileNameEdit)

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
			self.fileLoadEdit.setText(filename[0])

		def stop(self):
			self.close()

		def start(self):
			readfile = self.fileLoadEdit.text()
			p = str(pathlib.Path(readfile).parent) + '\\'

			if self.writeFileNameEdit.text() == '':
				writefile = p + 'wiki.txt'
			else:
				writefile = p + self.writeFileNameEdit.text() + '.txt'

			f1 = open(readfile, 'r')
			f2 = open(writefile, 'w')
			main(f1, f2, args.expand)
			f1.close()
			f2.close()
			print('Read: ' + readfile.replace('/','\\') + '\nWrite: ' + writefile)


	if __name__ == '__main__':
		app = QApplication(sys.argv)
		ex = MyApp()
		sys.exit(app.exec_())

else:
	f1 = open(args.path + '\\' + args.readname + '.txt', 'r', encoding='utf-8')
	f2 = open(args.path + '\\' + args.writename + '.txt', 'w', encoding='utf-8')
	main(f1, f2, args.expand)
	f1.close()
	f2.close()
