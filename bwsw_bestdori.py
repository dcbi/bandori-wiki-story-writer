import argparse
from pathlib import Path

dir = str(Path(__file__).parent.absolute())

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--path', help="parent directory of files to read and write, default="+dir, default=dir)
parser.add_argument('-r', '--readname', help='name of file to read from, default=transcript', default='source')
parser.add_argument('-w', '--writename', help='name of file to write to, default=wikicode', default='wikicode')
parser.add_argument('-e', '--expand', action='store_true', help='inserts wikicode to put story inside collapsible frame')

args = parser.parse_args()

class Slash(Exception): pass

writeNew = ''
skip = ['-'*10 + 'SKIPPED LINE' + '-'*10, 0]
names = ('kasumi', 'tae', 'rimi', 'saaya', 'arisa', 'yukina', 'sayo', 'lisa', 'ako', 'rinko', 'aya', 'hina', 'chisato', 'maya', 'eve', 'ran', 'moca', 'himari', 'tomoe', 'tsugumi', 'kokoro', 'kaoru', 'hagumi', 'kanon', 'misaki', 'marina')

def check_name(NAME):
    name = NAME.lower()
    if name in names:
        return name
    else:
        return NAME

def process(line,f1,f2):
    global writeNew
    global skip

    l = line.strip()

    if '/' in l:
        try:
            tag = l.split('/')
            if tag[0] == '':
                if tag[1] == '': writeNew = '{{dialog|other||[line]|' + tag[2] + '}}\n'
                else: writeNew = '{{dialog|' + check_name(tag[1]) + '|[line]}}\n'
            else:
                if tag[1] == '': f2.write('{{loc|' + tag[0] + '}}\n')
                else: raise Slash
            return

        except Slash:
            print('\nDetected possible slash "/" in dialog or loc text.')
            print('LINE: ' + l)
            cont = input('Select: (0) neither, (1) loc, (2) dialog\n--> ')
            if cont == '0':
                f2.write(skip[0])
                skip[1] += 1
            elif cont == '1':
                f2.write('{{loc|' + l[:len(line)-1] + '}}\n')
            elif cont == '2':
                f2.write( writeNew.replace('[line]', l.replace('@chariot', '{{USERNAME}}') ) )
            else:
                print('INVALID INPUT.')
                f2.write(skip[0])
                skip[1] += 1
            return
    else:
        try:
            f2.write( writeNew.replace('[line]', l.replace('@chariot', '{{USERNAME}}') ) )
        except UnicodeError:
            print('Possible special character. Check transcript file.')
            f2.write(skip[0])
            skip[1] += 1
            return

def main(f1, f2, expand, lines):
    if expand: f2.write('<div class="mw-collapsible mw-collapsed">\n')

    for line in lines: process(line,f1,f2)

    if expand: f2.write('</div><br />')

    global skip
    if not skip[1] == 0: print(str(skip[1]) + ' line(s) skipped. Fix output file manually.')

from html.parser import HTMLParser

class Bestdori_Parser(HTMLParser):
    def __init__(self):
        super().__init__()

        self.transcript = list()

        self.name_div = False
        self.name_span = False
        self.dialog1 = False
        self.dialog2 = False
        self.loc = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for atr in attrs:
                if atr[1] == 'm-b-s has-text-centered': self.loc = True
                elif atr[1] == 'm-b-xs fg-text': self.name_div = True
                elif atr[1] == 'columns is-mobile is-gapless fg-text': self.dialog1 = True
                elif atr[1] == 'column': self.dialog2 = True

        elif tag == 'span':
            for atr in attrs:
                if atr[1] == 'vertical-align: middle;': self.name_span = True

    def handle_data(self, data):
        if self.loc:
            self.transcript.append(data.strip() + '/\n')
            self.loc = False
        elif self.name_div and self.name_span:
            self.transcript.append('/' + data.strip() + '\n')
            self.name_div = False
            self.name_span = False
        elif self.dialog1 and self.dialog2:
            self.transcript.append(data.strip().replace('\n','') + '\n')
            self.dialog1 = False
            self.dialog2 = False

    def get_transcript(self):
        return self.transcript

bestdori_parser = Bestdori_Parser()

with open(args.path + '\\' + args.readname + '.txt', 'r', encoding='utf-8') as f1, open(args.path + '\\' + args.writename + '.txt', 'w', encoding='utf-8') as f2:

    bestdori_parser.feed( f1.read() )

    main(f1, f2, args.expand, bestdori_parser.get_transcript() )