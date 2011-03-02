#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import irclib, re, random, time
irclib.DEBUG=False

#Plugins
import loli, checkem, eightball, google, gelbooru

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
#channel = "#infinite-stratos"
channel = "#ifninite-stratos"
#channel = "#ujelly" #Test channel. Comment above before uncommenting this
con = "irc.rizon.net"
nick = "Jellybot"
user = "u jelly"
port = 6667

# For !checkem cooldown
last_usage = 0

class Bot:

    irc = irclib.IRC()
    server = irc.server()

    def callback(self, handle, arg):
        """Standard callback function. Defines default commands to be used by typing them into chat."""

        user = irclib.nm_to_n(arg.source())
        args = arg.arguments()
        if "!help" in args:
            self.server.privmsg(user, self.help(user))
            print arg.source(), ":", args
        elif "!checkem" in args:
            output = checkem.checkem( user )

            if output:
                self.server.privmsg(channel, output )

        elif "!tlnote" in args:
            self.tlnote()
            print arg.source(), ":", args
        elif re.search("!eightball", str(args)):
            self.server.privmsg( channel, eightball.eightball( user ) )
        elif re.search( "!loli", str(args) ):
            #Open db
            loli.open()

            #Create db if needed
            loli.create()

            #Execute command and return output
            output = loli.loli( user, time.time() )

            if output:
                self.server.privmsg(channel, output )

            #Close db
            loli.save()
        elif re.search( "!google", str(args) ):
            self.server.privmsg( channel, google.search( user, str(args).strip("[']")[7:] ) )
        elif re.search("!gelbooru", str(args)):
            #if len(args) < 13:
                #self.server.privmsg(channel, gelbooru.open())
            #else:
            self.server.privmsg(channel, gelbooru.open(str(str(args).strip("[']")[9:])))
        elif re.search("^POMF =3", str(args).strip("[']")):
            self.server.privmsg(channel, "Wah!")
        elif re.search("^Wah!", str(args).strip("[']")):
            self.server.privmsg(channel, "What are we gonna do on the bed?")
        else:
            print arg.source(), ":", args

    def help(self, user):
        """Sends help dialog via PM to user that asked."""

        self.server.privmsg(user, "Available commands:")
        self.server.privmsg(user, "* !help - this dialog")
        self.server.privmsg(user, "* !checkem - check 'em")
        self.server.privmsg(user, "* !tlnote - themoaryouknow")

    def ctcp(self, connection, event):
        """Sends CTCP answer to VERSION query."""

        if event.arguments() [0].upper() == "VERSION":
            connection.ctcp_reply(event.source().split('!')[0], "VERSION Python-IRCLib bot v0.2")
            print "Responded to CTCP VERSION query from", event.source()

    def join(self, handle, arg):
        """Callback function greeting users joining the channel."""

        global channel
        if irclib.nm_to_n(arg.source()) in ops.keys():
            self.server.privmsg(channel, "{0}, the representative candidate from {1} is here!".format(irclib.nm_to_n(arg.source()), ops.get(irclib.nm_to_n(arg.source()))))
            print "JOIN: ", arg.source()
        else:
            pass

    def modcmd(self, handle, arg):
        """Callback function for moderator commands (quit etc.)"""

        global channel
        user = irclib.nm_to_n(arg.source())
        args = arg.arguments()
        user = irclib.nm_to_n(arg.source())
        if user in mods or re.search("desu\.wa", irclib.nm_to_h(arg.source())) or re.search("is\.my\.husbando", irclib.nm_to_h(arg.source())):
            if ".quit" in args:
                self.server.close()
            elif re.search(".say", str(args)):
                temp = str(args)
                if re.search("/me", temp):
                    self.action(temp.strip("[']")[9:])
                else:
                    self.server.privmsg(channel, temp.strip("[']")[5:])
            elif "!help" in args:
                self.help(user)
            elif re.search(".nick", str(args)):
                self.server.nick(str(args).split()[1].strip("[']"))
        else:
            self.server.privmsg(user, "You are not allowed to use mod commands.")
            print "PRIVMSG from", arg.source(), ":", args

    def action(self, arg):
        """Prints /me action in given channel."""

        global channel
        self.server.ctcp('action', channel, arg)
        print "CTCP ACTION:", arg

    def tlnote(self):
        """TL Note: docstring is what you are reading now."""

        self.server.privmsg(channel, random.choice(tlnote))

    def connect(self):
        """Main function, connecting to server and channel and setting up event handlers."""

        global con, user, channel, nick, port
        self.server.connect(con, port, nick)
        self.server.user(user, user)
        self.server.join(channel)
        self.server.add_global_handler("pubmsg", self.callback)
        self.server.add_global_handler("privmsg", self.modcmd)
        self.server.add_global_handler("ctcp", self.ctcp)
        self.server.add_global_handler("join", self.join)
        self.irc.process_forever()


if __name__ == "__main__":
    bot = Bot()
    bot.connect()
