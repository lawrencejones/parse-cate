CATEScraper
===========

Originally designed with the purpose of supplying other apps with CATe
content, this package contains both a local and a server based solution
for scraping CATe info.
To install, run ` python setup.py install ` from the local_src folder.
This will install the relevant bs4 package that the parser requires.

## Want to Download ALL your Notes?
Yeah, that can be a pain. Luckily this should do it all for you! To
download all the notes, exercise spec sheets / model answers from CATe
for the specific term, then run the command

    `python LocalParser.py download`

from the `src` folder, once again supplying it with the chosen details.
I'd like to take this moment to point out the helpful TickList files
that are produced all over the place. I'm not spamming you, promise, the
idea is that as you do the exercises (dubious I know), then you'll be
able to drop a note to say what you got stuck on, when you got stuck on
it.

### Downloading Specific Modules ONLY
To limit the download to only one module, simply pass the script the
module id followed by the keyword download. Starting to regret the choice
of that flag now.

    `python LocalParser.py 141 download`

...run once again from the `src` folder. That would for example download
the Reasoning About Program stuff.
