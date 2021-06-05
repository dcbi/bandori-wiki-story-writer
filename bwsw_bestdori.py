import argparse
from pathlib import Path

dir = str(Path(__file__).parent.absolute())

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--path', help="parent directory of files to read and write, default="+dir, default=dir)
parser.add_argument('-r', '--readname', help='name of file to read from, default=transcript', default='source')
parser.add_argument('-w', '--writename', help='name of file to write to, default=wikicode', default='wikicode')
parser.add_argument('-e', '--expand', action='store_true', help='inserts wikicode to put story inside collapsible frame')
parser.add_argument('-y', '--yourName', help='your username on bestdori', default='New Staff')

args = parser.parse_args()

YN = (not args.yourName == 'New Staff') * '@' + args.yourName

skip = ['-'*10 + 'SKIPPED LINE' + '-'*10 + '}}\n', 0]

specialNames = {'Saya': 'Saaya', 'Toko': 'Touko'}

def checkName(bestdoriName):
    bandoriWikiName = bestdoriName
    for name in specialNames.keys():
        if name in bestdoriName: bandoriWikiName = bandoriWikiName.replace(name, specialNames[name])
    return bandoriWikiName

def process(line,f1,f2):
    global skip

    tag = line[0]
    l = line[1]

    if tag == 0:
        f2.write( '{{loc|' + l + '}}\n' )
    elif tag == 1:
        f2.write( '{{dialog|' + checkName(l) + '|' )
    elif tag == 2:
        try:
            l = l.replace('Saya', 'Saaya')
            l = l.replace('Toko', 'Touko')
            l = l.replace(YN, '{{USERNAME}}')
            f2.write( l + '}}\n')
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
            self.transcript.append( (0, data.strip()) )
            self.loc = False
        elif self.name_div and self.name_span:
            self.transcript.append( (1, data.strip()) )
            self.name_div = False
            self.name_span = False
        elif self.dialog1 and self.dialog2:
            a = data.strip().replace('\n','#')
            if '#' in a:
                i = a.index('#')
                if (a[i-1] == ' ') or (a[i+1] == ' '): a = a.replace('#', '')
                else: a = a.replace('#', ' ')
            self.transcript.append( (2, a) )
            self.dialog1 = False
            self.dialog2 = False

    def get_transcript(self):
        return self.transcript

bestdori_parser = Bestdori_Parser()

with open(args.path + '\\' + args.readname + '.txt', 'r', encoding='utf-8') as f1, open(args.path + '\\' + args.writename + '.txt', 'w', encoding='utf-8') as f2:

    bestdori_parser.feed( f1.read() )

    main(f1, f2, args.expand, bestdori_parser.get_transcript() )
