# bandori-wiki-story-writer
Python script for turning transcripts of event/card stories from Bandori into wiki-code (for use on [Bandori Wikia](https://bandori.fandom.com)).

#### Example
The following transcript

```
CiRCLE - Studio/
/sayo
Today's the day...
 /
Imai-san, I love you!
//Ako, Rinko, and Yukina
...!
```

will turn into the following wiki-code

```
{{loc|CiRCLE - Studio}}
{{dialog|sayo|Today's the day...}}
<br />
{{dialog|sayo|Imai-san, I love you!}}
{{dialog|others|...!|Ako, Rinko, and Yukina}}
```
### Dependencies
- pathlib (optional, just take it out and uncomment `import sys, os` and the line right after)
- pyqt, pyqtgraph (optional, only if you want to use UI)

### Example Usage
Suppose you have a transcript file already. Simply run `python bandori_wiki_story_writer.py`. You can include the following optional arguments:
- `-abbrev` turns on recognition of abbreviations for character names when indicating speaker (but it assumes it is universal, i.e. you shouldn't write a transcript with a mix of abbreviated names and non-abbreviated names).
- `-expand` wraps the wiki-code inside a collapsible frame. On the wikia, this looks like a button that says `Expand` which hides the story before being clicked and displays the story after being clicked.
- `-ui` opens up a window with a graphical user interface. If you open this, you don't need to enter the following arguments.
- `-path XXX` sets the parent directory where the transcript file is to be read from and where the output file is to be saved. The path can be either absolute or relatative to the current working directory. By default, it is the parent directory of the program itself.
- `-readname XXX` tells the program the name of the transcript file to read. By default, it is `transcript`.
- `-writename XXX` tells the program what to name the output file. By default, it is `wiki`.

#### Writing a transcript file
Transcript files are `.txt` files. They hold all the dialogue of an event/card story and use minimal syntax to indicate location banners or a change of speaker.
- **Locations:** start a new line, and write the location name followed immediately by a slash (`/`). 
- **New speaker:** start a new line, and write either a single or double slash (`/` or `//`) followed by the speaker. Single slash is for the main characters (those of the 25 bands and Marina). Double slash is for anything else. They can be unvoiced characters or groups of main characters or a main character but in a special situation (e.g. on the phone). The speaker does not have to be indicated before every line of dialogue, only when there is a change of speaker.
- **Dialogue:** start a new line (immediately below line indicating the speaker if a new speaker has just been indicated) and type the dialogue exactly is, nothing added.
- **Blank space:** to insert `<br />`, start a new line and type space followed by a single slash. This can represent when the story skips a brief moment of time, or whatever it may be.
- **Mentions of player character:** whenever the player character's name is mentioned, replace it, and the "-san" suffix after it, with `[you]`. In the wiki-code output file, this will become `{{USERNAME}}`.
Be careful that slashes doesn't appear in any of the dialogue lines, names of speakers, or names of locations. If they do, there is some clunky error handling that I tried to incorporate, which asks for user input to directly tell the program what to do. Also be wary of special symbols, such as those in the emotes that Rinko uses when typing. The program might not recognize them and raise an error.
