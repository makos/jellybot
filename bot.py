#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import irclib, re, random, time, sys
irclib.DEBUG=False # True for shitload of verbose text

#Plugins
import loli, checkem, eightball, google, gelbooru, timeleft, chat

# Feel free to add new ops
ops = {"UbrFrG":"South Africa", "makos":"Poland", "fatapaca":"Latvia", "Feath":"Canada"}

# Chosen Ones
mods = ("makos", "fatapaca")

# Add more stuff. kthxbai
tlnote = ("TL Note: Yuki means snow.", "TL Note: Kuroneko means black cat.", \
          "TL Note: keikaku means plan.", "TL Note: yome means bride, here it is implied as wife.", \
          "TL Note: Hourou Musuko means What The Fuck Am I Watching.")

# any idea how to make this display in multiple lines?
# """TL Note: Schneizel just made an illegal move in chess, so it doesn't make sense
#that he could say checkmate, he might possibly say check but the use of the term here is wrong. The only way this could be a legal
#move is if this were blitz chess, also known as "Fast Chess". However, in this scene, it is never declared they are playing "Fast Chess",
#and neither of the players are using clocks to time their turns in the game. (Source: /a/)
#TL Note 2: The reason why Schneizel did this is because the game was going to turn into a threefold rep. By pulling this illegal move, he
#is able to gain insight into Zero's personality, and "un-mask" part of him, thus fulfilling his victory condition in a subtle and Schneizel-ish
#manner. To look at the picture more properly, think of the chess board not as a game but as a battlefield. Zero's other options were to take his King,
#which would have made him similar to his father, or to call Schneizel out on making an illegal move, which would have made Zero look dumb since
#"lol rules of war". What Zero chose to do was keep his pride and run away from a free victory. Furthermore, by placing his King behind a pawn instead
#of any other open tile, Zero symbolically shows cowardice.
#TL Note 3: Alternatively, read it like this:
#[aers|laptop] Well personally I think the symbolism in Schneizel moving his king is that he wants to be buddy-buddy with Zero. And that Zero moving
#behind the pawn is because he is afraid of Schneizel's advances. (Geass is about yaoi and shit, so the likelihood of aers being correct is somewhere
#over 9000.)
#TL Note 4: This scene is interesting because it raises the question of whether or not Schneizel "plays dirty" in bed with Canon. :3
#CHECKMATE."""
# whew.


# Global Settings

#Channels
#Defalt output channel for some commands is first channel
channels = [ "#infinite-stratos", "#ujelly", "#madoka", "#k-on-game" ]
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
            self.server.privmsg(chan, self.tlnote())

        elif re.search("^(!eightball|!8ball)", args):              # To have the ^ wildcard working in regexp we need to strip args from ['] first.
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

        else:

            mentioned   = 0
            public      = self.public
            nickname    = self.server.nickname

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

    def ctcp(self, connection, event):
        """Sends CTCP answer to VERSION query."""

        if event.arguments() [0].upper() == "VERSION":
            connection.ctcp_reply(event.source().split('!')[0], "VERSION Python-IRCLib bot v0.2")
            print "Responded to CTCP VERSION query from", event.source()

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
        chan    = arg.target()
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
