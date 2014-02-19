CATEScraper
===========

Originally designed with the purpose of supplying other apps with CATe
content, this package contains both a local and a server based solution
for scraping CATe info.
To install, run ` python setup.py install ` from the local_src folder.
This will install the relevant bs4 package that the parser requires.

## Just Collecting Info
To just pick up the information about exercises, modules, what-not and
just run with it, feel free to call the command

    `python LocalParser.py`

from the `src` folder. This will then ask for your login details, term
time etc. Using these credentials it will proceed to login to CATe,
process the content and spit it out in the terminal.

## Want to Download ALL your Notes?
Yeah, that can be a pain. Luckily this should do it all for you! To
download all the notes, exercise spec sheets / model answers from CATe
for the specific term, then run the command

    `python LocalParser.py kickass`

from the `src` folder, once again supplying it with the chosen details.
I'd like to take this moment to point out the helpful TickList files
that are produced all over the place. I'm not spamming you, promise, the
idea is that as you do the exercises (dubious I know), then you'll be
able to drop a note to say what you got stuck on, when you got stuck on
it.

### TickList files
Being an self-confessed obsessive compulsive monster, I really enjoy
seeing things slowly get ticked off all over the place. 
If it's really not your thing, then just run

    `rm **/TickList`

from the root of the downloaded files. You have my apology.

### On the subject of TickLists...
If you're planning on stacking up multiple term downloads, which is
perfectly fine by the way (just run the script once for each term in
chronological order), then make sure you remove the TickLists with that
command just prior to the last run through. Prevents duplication you
see. 

## Selecting Modules Specifically!
To pick out an individual module then just pass the modules id in as an
extra argument. At the moment it only outputs the notes, though I'm sure
I'll get the surge of energy required to have it output all the exercise
information in the future.

### Downloading Specific Modules ONLY
To limit the download to only one module, simply pass the script the
module id followed by the keyword kickass. Starting to regret the choice
of that flag now.

    `python LocalParser.py 141 kickass`

...run once again from the `src` folder. That would for example download
the Reasoning About Program stuff.
