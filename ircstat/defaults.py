# Copyright 2013 John Reese
# Licensed under the MIT license

# the regex to parse data from irc log filenames.
# must contain two named matching groups:
#   channel: the name of the channel
#   date: the date of the conversation
filename_regex = r'#?(?P<channel>[a-z]+)_(?P<date>\d{8}).log'

# the format of the date content in the matched filename.
# must follow python's datetime.strptime() format, as defined at
# http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
filename_date_format = r'%Y%m%d'
