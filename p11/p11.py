#!/usr/bin/python
  
from Crypto.Cipher import AES # https://www.dlitz.net/software/pycrypto/

class Event():
  '''The class Event was created to defined a comparison based in time
     The greater the time, the lower the event
  '''
  def __init__(self, string):
    x,y,z = map(int,string.split(' '))
    self.user_id = x
    self.time = y
    self.event_id = z

  def __str__(self): return '%s' % (self.event_id)

  def __lt__(self, other): return self.time > other.time
  def __le__(self, other): return self.time >= other.time
  def __eq__(self, other): return self.time == other.time
  def __ne__(self, other): return self.time != other.time
  def __gt__(self, other): return self.time < other.time
  def __ge__(self, other): return self.time <= other.time

letters = 'qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM'
key_suffixes = [x+y+z for x in letters for y in letters for z in letters]

def find_feeds(user_id, key_prefix):
  '''find_feeds(str, str) -> list of Event
  
  Open the encrypted file for the specified user and tries
  to decrypt it withh all possible key combinations.

  Once decrypted, returns all the user events in a list
  '''
  user_suffix = user_id[len(user_id)-2:]
  filename = 'encrypted/'+user_suffix+'/'+user_id+'.feed'
  feed_file = open(filename, 'rb')
  feed_content = feed_file.read()
  for key_suffix in key_suffixes: # try all suffix combinations
    cipher = AES.new(key_prefix+key_suffix)
    possible_feed = cipher.decrypt(feed_content)
    # if the cipher worked, the decrypted content begins with
    # the user_id
    if possible_feed[:len(user_id)] == user_id:
      # split the events, remove the noisy bytes and create the event objects
      list_of_feeds = map(lambda y: Event(y), \
                          filter(lambda x:x[:len(user_id)] == user_id, \
                                 possible_feed.split('\n')))
      return list_of_feeds
  return [] # no feeds found

def last_time(user_id):
  '''last_time(str) -> int
  
  Open the last_time file for the user and returns its content
  '''
  user_suffix = user_id[len(user_id)-2:]
  filename = 'last_times/'+user_suffix+'/'+user_id+'.timestamp'
  return int(open(filename).read())

if __name__ == '__main__':
  try:
    feeds_found = {} # memoization to avoid repeated IO
    latest_feed = {} # memoization to avoid repeated IO
    while True:
      elements = raw_input().split('; ')
      minimum_feed = 99999999999
      feed_limit = int(elements[0])
      timeline = [] # priority queue for feeds
      friends = map(lambda x: x.split(','), elements[1:])
      for user_id, key_prefix in friends:
        if user_id not in latest_feed: 
          latest_feed[user_id] = last_time(user_id)

        # if the newest event for a friend is older than the oldest found
        # so far and we already have reached feed_limit events, then
        # there is no need to process this user
        if latest_feed[user_id] < minimum_feed and len(timeline) >= feed_limit: 
          continue

        if user_id not in feeds_found:
          feeds_found[user_id] = find_feeds(user_id, key_prefix)

        # [:feed_limit] no need to add all the events
        timeline = timeline + feeds_found[user_id][:feed_limit]
        timeline.sort() 
        timeline = timeline[:feed_limit] # remove events outside the timeline
        minimum_feed = timeline[-1].time # get the oldest event to avoid olders

      print ' '.join(map(str,timeline))
  except EOFError:
    pass # End of input
