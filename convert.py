#!/usr/bin/env python

from datetime import datetime
import glob
import os.path
import plistlib
import sys
import re

data = {
    'date_saved': datetime.now(),
    'notes': []
}

suffix_regex = re.compile(r'\.\w{1,3}$')

with open("output.jtbackup", 'w') as plist:
    directory = os.path.expanduser(sys.argv[1])
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)

        # Remove the file format suffix
        title = suffix_regex.sub('', filename)

        # Skip dotfiles
        if path.startswith("."):
            continue

        try:
            with open(path) as f: pass
        except IOError:
            pass
        else:
            with open(path) as f:
                file_data = {
                    'color': 2,
                    'dateModified': datetime.fromtimestamp(os.path.getmtime(path)),
                    'fontIsBold': 0,
                    'fontName': "Inconsolata",
                    'fontSize': 14,
                    'hasDefaultFont': 1,
                    'hasDefaultTitle': 0,
                    'isStarred': 0,
                    'title': suffix_regex.sub('', filename)
                }

                contents = f.read()
                try:
                    file_data['text'] = contents.encode("utf-8")
                except ValueError:
                    # file_data['text'] = plistlib.Data(contents)
                    # Skip this file...for now
                    continue

                data['notes'].append(file_data)

    plistlib.writePlist(data, plist)

