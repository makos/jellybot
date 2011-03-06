#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import irclib, re, random, time, sys
irclib.DEBUG=False # True for shitload of verbose text

#Plugins
import loli, checkem, eightball, google, gelbooru, timeleft, chat, gelboorus, tlnote

# Feel free to add new ops
ops = {"UbrFrG":"South Africa", "makos":"Poland", "fatapaca":"Latvia", "Feath":"Canada"}

# Chosen Ones
mods = ("makos", "fatapaca")

# Global Settings

#Channels
#Defalt output channel for some commands is first channel
channels = [ "#infinite-stratos", "#ujelly", "#madoka", "#k-on-game", "#koihime", "#pswg" ]
#channels = [ "#ujelly" ]

nick = "Jellybot"
con = "irc.rizon.net"
user = "ujelly"
port = 6667

class Bot:

  irc = irclib.IRC()
  server = irc.server()
  public = 1

  pomfdown = int( time.time() )
  baww     = int( time.time() )
  untz     = int( time.time() )

  def callback(self, handle, arg):
    """Standard callback function. Defines default commands to be used by typing them into chat."""

    user = irclib.nm_to_n(arg.source())
    args = arg.arguments()[0]
    chan = arg.target()

    if "!help" in args:
      self.server.privmsg(user, self.help(user))
    elif "!checkem" in args:
      output = checkem.checkem( user )

      if output:
        self.server.privmsg(chan, output )

    elif "!tlnote" in args:
      tlnote._open()
      tlnote._create()

      note = tlnote.tlnote()

      if note:
        self.server.privmsg(chan, note)

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

    elif re.search("^(!eightball|!8ball)", args):       # To have the ^ wildcard working in regexp we need to strip args from ['] first.
      self.server.privmsg( chan, eightball.eightball( user ) )

    elif re.search( "^!loli", args):

      #Open db and create if needed
      loli.open()
      loli.create()

      #Execute command and return output
      output = loli.loli( user )

      if output:
        self.server.privmsg(chan, output )

      #Close db
      loli.save()

    elif re.search( "^!steal", args):

      arguments = args.split(" ")

      #Only wrote !steal
      if len( arguments ) < 2:
        return;

      target = arguments[1]

      print user, "is attempting to steal lolis from", target

      if user == target:
        print ">> Attempting to steal from himself"

      #Open db
      loli.open()
      loli.create()

      #Execute command and return output
      output = loli.steal( user, target )

      if output:
        self.server.privmsg(chan, output )
      else:
        print ">> Nope."

      #Close db
      loli.save()

    elif re.search( "^!top5", args):
      loli.open()
      loli.create()

      data = loli.top5()

      if data:
        _i = 1

        for user in data:
          self.server.privmsg(chan, "#{} :: {} with {} lolis\n".format( _i, user[0], user[1], ) )
          _i += 1

    elif re.search( "^!google", args ):

      arguments = args.split(" ")

      if len(arguments) < 2:
        return

      _query = arguments[1:]

      self.server.privmsg( chan, google.search( user, " ".join( _query ) ) )

    elif re.search("^!gelbooru", args):

      arguments = args.split(" ")

      if len(arguments) < 2:
        return

      _query = arguments[1:]

      self.server.privmsg( chan, gelbooru.open( " ".join( _query ) ) )

    elif re.search( "^!timeleft", args ):

      self.server.privmsg(chan, timeleft.timeleft( user ))

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
      self.server.privmsg(chan, "THE TRUTH LIES BEYOND THE GATE")
    elif re.search("THE TRUTH EXISTS BEYOND THE GATE", args, re.IGNORECASE):
      self.server.privmsg(chan, "*guitar riff*")

    elif re.search("^!gsearch", args):
      arguments = args.split(" ")

      if len(arguments) < 2:
        return

      _query = arguments[1:]

      self.server.privmsg( chan, str(gelboorus.search( " ".join( _query ) ) ) )

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
      connection.ctcp_reply(arg.source().split('!')[0], "VERSION Python-IRCLib bot v0.2")
      print "Responded to CTCP VERSION query from", arg.source()

  def join(self, handle, arg):
    """Callback function greeting users joining the channel."""

    if irclib.nm_to_n(arg.source()) in ops.keys():
      self.server.privmsg( arg.target(), "{0}, the representative candidate from {1} is here!".format(irclib.nm_to_n(arg.source()), ops.get(irclib.nm_to_n(arg.source()))))
      print "JOIN: ", arg.source()
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

      elif re.search(".part", args):
          arg = args.split()

          if len(arg) < 2:
            return

          for chan in arg[1:]:
            print "Leaving channel", chan
            self.server.part( chan )

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

  def tlnote(self):
    """TL Note: docstring is what you are reading now."""

    return random.choice(tlnote)

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
    self.irc.process_forever()


if __name__ == "__main__":
  bot = Bot()
  bot.connect()
