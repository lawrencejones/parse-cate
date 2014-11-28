CATEScraper
===========

To install, run ` python setup.py install ` from the local_src folder.
This will install the relevant bs4 package that the parser requires.

## Want to Download ALL your Notes?
Yeah, that can be a pain. Luckily this should do it all for you! To
download all the notes, exercise spec sheets / model answers from CATe
for the specific term, then run the command

    `python LocalParser.py download`

from the `src` folder, once again supplying it with the chosen details.

### Downloading Specific Modules ONLY
To limit the download to only one module, simply pass the script the
module id followed by the keyword download.

    `python LocalParser.py 141 download`

...run once again from the `src` folder. That would for example download
the Reasoning About Program stuff.
