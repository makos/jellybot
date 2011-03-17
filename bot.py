#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import irclib, re, random, time, sys, threading, logging
irclib.DEBUG=False # True for shitload of verbose text

#Plugins
import loli, checkem, eightball, google, gelbooru, timeleft, chat, gelboorus, tlnote, tweets, gtranslate, settopic, fourchan, ustream

logging.basicConfig(filename='jellybot.log',level=logging.DEBUG)

# Feel free to add new ops
ops = {"UbrFrG":"South Africa", "makos":"Poland", "fatapaca":"Latvia", "Feath":"Canada"}

# Chosen Ones
mods = ("makos", "fatapaca")

# Faggots
faggots = ( "ShiroKen", "Rizon-122C7F8A.cable.virginmedia.com" )

# Global Settings

#Channels
#Defalt output channel for some commands is first channel
channels = [ "#infinite-stratos", "#ujelly", "#k-on-game", "#pswg" ]
#channels = [ "#ujelly" ]

nick = "Jellybot"
con = "irc.rizon.net"
user = "ujelly"
port = 6667

class Bot:

  irc = irclib.IRC()
  server = irc.server()
  public = 1
  gaia   = True
  #running = True
  thread =  "47047124"

  pomfdown = int( time.time() )
  baww     = int( time.time() )
  untz     = int( time.time() )

  def twitter_update( self, name, num = 5, interval = 60, tl = True, channel = "#pswg" ):

    time.sleep(interval)

    latest = None

    while True:

      output = tweets.stalk( name, num, latest )

      if output:

        output.reverse()

        for s in output:

          text = s.text
          id   = s.id

          self.server.notice(channel, "%s [Posted by %s %s.]" % ( text.encode("utf8"), name, s.relative_created_at ))

          if tl:
            self.server.notice(channel, ":: Engrish >> %s" % ( gtranslate._translate(text).encode("utf8") ))

          latest = id

      time.sleep(interval)

  def thread_update(self, interval):
    time.sleep(interval)

    last_post = None

    while True:

      thread = None

      try:
        thread = fourchan.parse_thread( "a", self.thread )
        
        #Download images
        fourchan.download_images(thread)

        #Save json data of thread
        thread.save()

      except Exception, e:
        if str(e).find("Error 404") !=-1:
          print "Thread %s 404d" % self.thread
          time.sleep(interval * 2)
        else:
          print e
          
        continue

      if thread:
        #Last post
        post = thread.posts[-1]

        if post.id == last_post:
          time.sleep(interval)
          continue
          
        if not post.text:
          time.sleep(interval)
          continue
        
        message = ">>/a/%s#%s %s" % ( self.thread, post.id, post.text ) 
        
        try:
          self.server.notice( "#infinite-stratos",  message)
        except UnicodeEncodeError, e:
          print "derp"
          print "-" * 40
          print e

        last_post = post.id

      time.sleep(interval)

  def check_ustream(self, channel, interval = 60):

    time.sleep(10)

    notified = False

    while True:

      status = ustream.is_on(channel)

      if status:
        if notified:
          time.sleep(interval)
          continue

        self.server.notice("#pswg", "%s's broadcast has started, START RIPPING" % channel)
        self.server.notice("#pswg", "Watch at http://www.ustream.tv/channel/%s" % channel)
        notified = True
      else:
        notified = False

      time.sleep(interval)


  def callback(self, handle, arg):
    """Standard callback function. Defines default commands to be used by typing them into chat."""

    host = arg.source()
    user = irclib.nm_to_n(host)
    args = arg.arguments()[0]
    chan = arg.target()
    
    for faggot in faggots:
        if re.search(faggot, host):
          return

    if "!help" in args:
      self.server.privmsg(user, self.help(user))

      """ Useless faggotry
    elif "!checkem" in args:
      output = checkem.checkem( user )

      if output:
        self.server.notice(user, output )

    elif "!tlnote" in args:
      tlnote._open()
      tlnote._create()

      note = tlnote.tlnote()

      if note:
        self.server.notice(chan, note)

      tlnote._close()

    elif ".tlnote" in args:

      arguments = args.split(" ")

      if len(arguments) < 2:
        return

      note = " ".join( arguments[1:] )

      tlnote._open()
      tlnote._create()

      tlnote.add( user, note )
      self.server.privmsg( user, "Added: {}".format( note ) )

      tlnote._close()
      """

    elif "!thread" in args:
      if chan == "#infinite-stratos":
        thread = "http://boards.4chan.org/a/res/%s" % self.thread
        self.server.notice(chan, "Current thread: %s" % thread)

    elif re.search("^(!eightball|!8ball)", args):       # To have the ^ wildcard working in regexp we need to strip args from ['] first.
      self.server.notice( user, eightball.eightball( user ) )

    elif re.search( "^!loli", args):

      #Open db and create if needed
      loli.open()
      loli.create()

      #Execute command and return output
      output = loli.loli( user )

      if output:
        self.server.notice(user, output )

      #Close db
      loli.save()

    elif re.search( "^!steal", args):

      arguments = args.split(" ")

      #Only wrote !steal
      if len( arguments ) < 2:
        return;

      target = arguments[1]

      logging.debug("%s is attempting to steal lolis from %s" % ( user, target ))

      if user == target:
        return
      
      """
      if target in mods: #Because I can
        self.server.privmsg(chan, "NOPE.exe")
        return
      """

      #Open db
      loli.open()
      loli.create()

      #Execute command and return output
      output = loli.steal( user, target )

      if output:
        self.server.notice( "%s,%s" % (user, target), output )

      #Close db
      loli.save()

    elif re.search( "^!top5", args):
      print args
      print user

      loli.open()
      loli.create()

      data = loli.top5()
      
      print data

      if data:
        _i = 1

        for user in data:
          print user
          out = "%s. - %s with %s lolis" % ( _i, user[0], user[1], ) 
          print out
          self.server.privmsg(chan, out)
          _i += 1

      loli.save()

    elif re.search( "^!google", args ):

      arguments = args.split(" ")

      if len(arguments) < 2:
        return

      _query = arguments[1:]

      self.server.notice( user, google.search( user, " ".join( _query ) ) )

    elif re.search( "^!moon", args ):

      arguments = args.split(" ")

      if len(arguments) < 2:
        return

      text = " ".join( arguments[1:] )
      tl   = gtranslate._translate( text.decode('utf8') )

      self.server.notice( user, "%s, moon >> engrish :: %s" % ( user, tl.encode('utf8') ) )

    elif re.search("^!gelbooru", args):

      arguments = args.split(" ")

      if len(arguments) < 2:
        return

      _query = arguments[1:]

      self.server.notice( user, gelbooru.open( " ".join( _query ) ) )

    elif re.search( "^!timeleft", args ):
      if chan == "#infinite-stratos":
        self.server.notice(chan, timeleft.timeleft( user ))

    elif re.search("^POMF =3", args):

      #Stop spamming that shit
      if ( int(time.time()) - self.pomfdown ) > 5:
        self.server.privmsg(chan, "Wah!")

        self.pomfdown = int(time.time())

    elif re.search("^Wah!", args):

      #Stop spamming that shit
      if ( int(time.time()) - self.pomfdown ) > 5:
        self.server.privmsg(chan, "What are we gonna do on the bed?")

        self.pomfdown = int(time.time())

    elif re.search("^;_;", args):

      if ( int(time.time()) - self.baww ) > 5:
        self.server.privmsg(chan, ";_;")

        self.baww = int(time.time())

    elif re.search("UNTZ", args):

      if ( int(time.time()) - self.untz ) > 5:
        self.server.privmsg(chan, "UNTZ UNTZ UNTZ UTNZ UTNZ UNTZ")

        self.untz = int(time.time())

    # NOW I'VE LOST IT
    elif re.search("A NIGHT SKY FULL OF CRIES", args, re.IGNORECASE):
      self.server.privmsg(chan, "HEARTS FILLED WITH LIES")
    elif re.search("HEARTS FILLED WITH LIES", args, re.IGNORECASE):
      self.server.privmsg(chan, "THE CONTRACT, IS IT WORTH THE PRICE?")
    elif re.search("THE CONTRACT. IS IT WORTH THE PRICE.", args, re.IGNORECASE):
      self.server.privmsg(chan, "A SOUL PLEDGED TO THE DARKNESS")
    elif re.search("A SOUL PLEDGED TO THE DARKNESS", args, re.IGNORECASE):
      self.server.privmsg(chan, "NOW I'VE LOST IT")
    elif re.search("NOW I'VE LOST IT", args, re.IGNORECASE):
      self.server.privmsg(chan, "I KNOW I CAN KILL")
    elif re.search("I KNOW I CAN KILL", args, re.IGNORECASE):
      self.server.privmsg(chan, "THE TRUTH EXISTS BEYOND THE GATE")
    elif re.search("THE TRUTH (EXISTS|LIES|IS) BEYOND THE GATE", args, re.IGNORECASE):
      self.server.privmsg(chan, "*guitar riff*")

    elif re.search("(X|x|:|;|=)(P|D|\)|\(|\/|\\\)|((>|<|\*|O|o|\^)(\.*|_*|-*)(>|<|\*|O|o|\^))", args) and not self.gaia:

      if chan == "#madoka": #Derp
        return

      if not random.randint(0,4): #25%
        self.server.notice(user, "{}, gb2 >>>/gaia/".format(user))

    elif re.search("^!gsearch", args):
      arguments = args.split(" ")

      if len(arguments) < 2:
        return

      _query = arguments[1:]

      self.server.notice( user, str(gelboorus.search( " ".join( _query ) ) ) )

    else:
      mentioned = 0
      public    = self.public
      nickname  = self.server.nickname

      output = chat.parse( user, args, nickname, public )

      if output != None:
        self.server.privmsg( chan, output )

      return

  def help(self, user):
    """Sends help dialog via PM to user that asked."""

    self.server.privmsg(user, "Available commands:")
    self.server.privmsg(user, "* !help - this dialog")
    self.server.privmsg(user, "* !checkem - check 'em")
    self.server.privmsg(user, "* !tlnote - themoaryouknow")
    self.server.privmsg(user, "* !google - google search")
    self.server.privmsg(user, "* !gelbooru [tags] - gelbooru search for latest picture under given tag, if no tag given it defaults to infinite_stratos")
    self.server.privmsg(user, "* !loli - catch 'em all")

  def ctcp(self, connection, arg):
    """Sends CTCP answer to VERSION query."""
    chan  = arg.target()
    caller  = irclib.nm_to_n(arg.source())
    _args   = arg.arguments()

    if len(_args) > 1:
      if _args[0] == "ACTION":
        _act = _args[1].split()
        if len(_act) > 1:
          if _act[0] == "hugs":

            if _act[1] == self.server.nickname:
              self.server.ctcp('action', chan, "slaps {}".format(caller))

    if arg.arguments() [0].upper() == "VERSION":
      connection.ctcp_reply(arg.source().split('!')[0], "VERSION Jellybot :: Codename: U.JELLY")
      logging.debug("Responded to CTCP VERSION query from %s" % arg.source())

  def join(self, handle, arg):
    """Callback function greeting users joining the channel."""

    if irclib.nm_to_n(arg.source()) in ops.keys():
      self.server.notice( arg.target(), "{0}, the representative candidate from {1} is here!".format(irclib.nm_to_n(arg.source()), ops.get(irclib.nm_to_n(arg.source()))))
      logging.debug("JOIN: %s" % arg.source())
    else:
      pass

  def invite(self, handle, arg):
    chan = arg.arguments()[0]

    self.server.join( chan )

    print "Joining", chan, "because", arg.source(), "invited me."

  def kick(self, handle, arg):
    chan  = arg.target()
    kicker  = arg.source()
    target  = arg.arguments()[0]

    print "KICK: ", kicker, "kicked", target, "in", chan

    if target == self.server.nickname:
      time.sleep(5)
      print "Rejoining", chan
      self.server.join( chan )

    return

  def modcmd(self, handle, arg):
    """Callback function for moderator commands (quit etc.)"""

    user = irclib.nm_to_n(arg.source())
    args = arg.arguments()[0]

    if user in mods or re.search( "desu\.wa", user) or re.search("is\.my\.husbando", user ):

      if ".quit" in args:
        self.server.close()
        sys.exit()

      elif re.search(".say", args):
        arg = args.split()

        if len(arg) < 2:
          return

        if arg[1] in channels:
          if re.search("/me", arg[2]):
            if len(arg) < 4:
              return

            self.server.ctcp('action', arg[1], " ".join( arg[3:] ) )

          else:
            if len(arg) < 3:
              return

            self.server.privmsg(arg[1], " ".join( arg[2:] ))

        else:
          if re.search("/me", arg[1]):

            if len(arg) < 3:
              return

            self.action( " ".join( arg[2:] ) )

          else:
            self.server.privmsg(channels[0], " ".join( arg[1:] ))

      elif "!help" in args:
        self.help(user)

      elif re.search(".nick", args):
        arg = args.split()

        if len(arg) < 2:
          return

        print "Changed nick to", arg[1]
        self.server.nick(arg[1])

      elif ".pubchat" in args:
        if self.public == 0: self.public = 1
        else: self.public = 0

        self.server.privmsg(user, "Public conversation mode is now {}.".format( self.public == 0 and "OFF" or "ON" ))

      elif re.search(".join", str(args)):
          arg = args.split()

          if len(arg) < 2:
            return

          for chan in arg[1:]:
            print "Joing channel", chan
            self.server.join( chan )
            
            if not chan in channels:
              channels.append(chan)

      elif re.search(".part", args):
          arg = args.split()

          if len(arg) < 2:
            return

          for chan in arg[1:]:
            print "Leaving channel", chan
            self.server.part( chan )

            if chan in channels:
              channels.remove(chan)
      elif re.search(".channels", args):
        self.server.privmsg(user, "Channels: %s" % " ".join(channels) )

	    
      elif re.search(".settopic", args):
        """".settopic #chan thread episode"""
        
        arg = args.split()
        print arg
        
        if len(arg) < 3:
          return
        
        chan   = arg[1]
        thread = arg[2]
        ep     = None

        if len(arg) > 3:
          ep = arg[3]

        print chan
        print thread
        print ep
		    
        self.server.topic(chan, settopic.set_topic(thread, ep))
      
      elif ".thread" in args:
        arg = args.split()

        if len(arg) < 1:
          return
        
        self.server.privmsg(user, "Current thread is now: %s" % arg[1])
        self.thread = arg[1]

        
      else:
        
        output = chat.parse( user, args, self.server.nickname, True, False )

        if output != None:
          self.server.privmsg( user, output )

    else:
      print "PRIVMSG from", arg.source(), ":", args
      output = chat.parse( user, args, self.server.nickname, True, False )

      if output != None:
        print "->> REPLY:", output
        self.server.privmsg( user, output )

  def action(self, arg):
    """Prints /me action in given channel."""


    self.server.ctcp('action', channels[0], arg)
    print "CTCP ACTION:", arg

  def connect(self):
    """Main function, connecting to server and channel and setting up event handlers."""

    global con, user, channels, nick, port

    self.server.connect(con, port, nick)
    self.server.user(user, user)

    for chan in channels:
      self.server.join(chan)

    self.server.add_global_handler("pubmsg", self.callback)
    self.server.add_global_handler("privmsg", self.modcmd)
    self.server.add_global_handler("ctcp", self.ctcp)
    self.server.add_global_handler("join", self.join)
    self.server.add_global_handler("kick", self.kick)
    self.server.add_global_handler("invite", self.invite)

    twitter = threading.Thread( target=self.twitter_update,args=( "choroyama", 3, 60 ) )
    twitter.setDaemon(True)
    twitter.start()

    chan = threading.Thread( target=self.thread_update, args=([60]) )
    chan.setDaemon(True)
    chan.start()

    ustream = threading.Thread( target=self.check_ustream, args=("choroyama", 60) )
    ustream.setDaemon(True)
    ustream.start()
    
    """
    ustream = threading.Thread( target=self.check_ustream, args=("mogra1", 60) )
    ustream.setDaemon(True)
    ustream.start()
    """


    try:
      self.irc.process_forever()
    except KeyboardInterrupt, e:
      print "Exiting"
      sys.exit()

if __name__ == "__main__":
  bot = Bot()
  bot.connect()
