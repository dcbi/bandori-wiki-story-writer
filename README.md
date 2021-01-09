# bandori-wiki-story-writer
Python code for turning transcripts of event/card stories from Bandori into wiki-code (for use on [Bandori Wikia](https://bandori.fandom.com)).

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
(optional, only if you want to use UI)
- pyqt
- pyqtgraph 

### Example Usage
Suppose you have a transcript file already. As long as it is in the same location as the program and titled `transcript.txt`, simply run `python bandori_wiki_story_writer.py`. To loosen those restrictions, include the following optional arguments:
- `-path folder_1\folder_2` or `-path C:\Users\ursul\Desktop` sets the parent directory where the transcript file is to be read from and where the output file is to be saved. The path can be either absolute or relatative to the current working directory. By default, it is the parent directory of the program itself.
- `-readname transcript_file_name` tells the program the name of the transcript file to read. By default, it is `transcript`.
- `-writename output_file_name` tells the program what to name the output file. By default, it is `wiki`.

There are two versions of the code. The one with the label "base" at the end does not have the following features. For the main code, you can also run it with the following arguments:
- `-ui` opens up a window with a graphical user interface. If you open this, you don't need to enter the arguments in the list above. This requires the packages listed above in the **Dependencies** list.
- `-expand` wraps the wiki-code inside a collapsible frame. On the wikia, this looks like a button that says `Expand` which hides the story before being clicked and displays the story after being clicked.
- `-abbrev` turns on recognition of abbreviations for character names when indicating speaker (but it assumes it is universal, i.e. you shouldn't write a transcript with a mix of abbreviated names and non-abbreviated names).

### Writing a transcript file
Transcript files are `.txt` files. They hold all the dialogue of an event/card story and use minimal syntax to indicate location banners or a change of speaker.
- **Locations:** start a new line, and write the location name followed immediately by a slash (`/`). 
- **New speaker:** start a new line, and write either a single or double slash (`/` or `//`) followed by the speaker.
  - Single slash is for the main characters (those of the 25 bands and Marina). It doesn't matter if they're capitalized or not. These can also be abbrevations. See below for the abbreviations. You can change them to your own if you want. They're just hard-coded in for now.
  - Double slash is for anything else. They can be unvoiced characters or groups of main characters or a main character but in a special situation (e.g. on the phone). In this case, character names cannot be abbreviated. You have to write them all out, with proper capitalization.
  - The speaker does not have to be indicated before every line of dialogue, only when there is a change of speaker.
- **Dialogue:** start a new line (immediately below the line indicating the speaker if a new speaker has just been indicated) and type the dialogue exactly as is, nothing added.
- **Blank space:** to insert `<br />`, start a new line and type space followed by a single slash. This can represent when the story skips a brief moment of time, or whatever it may be.
- **Mentions of player character:** whenever the player character's name is mentioned, replace it, and the "-san" suffix after it, with `[you]`. In the wiki-code output file, this will become `{{USERNAME}}`.

Be careful that slashes doesn't appear in any of the dialogue lines, names of speakers, or names of locations. If they do, there is some clunky error handling that I tried to incorporate, which asks for user input to directly tell the program what to do. Also be wary of special symbols, such as those in the emotes that Rinko uses when typing. The program might not recognize them and raise an error.

The following abbreviations are used: ['kas', 'tae', 'rim', 'say', 'ari', 'y', 's', 'l', 'a', 'r', 'aya', 'hin', 'chi', 'may', 'eve', 'ran', 'moc', 'him', 'tom', 'tsu', 'kok', 'kao', 'hag', 'kan', 'mis', 'mar']. You can probably tell which band is my favorite.
