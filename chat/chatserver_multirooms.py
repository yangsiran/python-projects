from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore


PORT = 5005
NAME = 'TestChat'


class EndSession(Exception): pass


class CommandHandler:
    """
    Simple command handler similar to cmd.Cmd from the standard
    libary.
    """

    def unknown(self, session, line):
        'Respond to an unknown command'
        cmd = line.split(' ', 1)
        session.push('Unknown command: %s\r\n' % cmd)

    def handle(self, session, line):
        'Handle a received line from a given session'
        if not line.strip(): return
        # Split off the command:
        parts = line.split(' ', 1)
        cmd = parts[0]
        try: arg = parts[1].strip()
        except IndexError: arg = ''
        # Try to find a handler:
        meth = getattr(self, 'do_'+cmd, None)
        try:
            # Assume it's callable
            meth(session, arg)
        except TypeError:
            # If it isn't, respond to the unknown command:
            self.unknown(session, line)


class Room(CommandHandler):
    """
    A generic environment which may contain one or more users
    (sessions). It takes care of basic command handling and
    broadcasting.
    """

    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        'A session (user) has entered the room'
        self.sessions.append(session)

    def remove(self, session):
        'A session (user) has left the room'
        self.sessions.remove(session)

    def broadcast(self, line):
        'Send a line to all sessions in the room'
        for session in self.sessions:
            session.push(line)

    def do_who(self, session, line):
        'Handles the who command, used to see who is logged in'
        session.push('The following are logged in:\r\n')
        for user in self.server.users:
            session.push(user + '\r\n')

    def do_quit(self, session, line):
        'Respond to the quit command'
        raise EndSession


class LoginRoom(Room):
    """
    A room meant for a single person who has just connected.
    """

    def add(self, session):
        Room.add(self, session)
        # When a user enters, greet him/her:
        self.broadcast('Welcome to %s\r\n' % self.server.name)

    def unknown(self, session, line):
        # All unknown commands (anything except login or logou)
        # result in prodding:
        session.push('Use "look" to check for existing rooms\r\n')
        session.push('Use "login <room> <user>" to login into a room\r\n')
        session.push('Use "new <room>" to open a new room\r\n')

    def do_look(self, session, line):
        'Handles the look command, used to see what rooms are existing'
        session.push('The following room(s) are in the server:\r\n')
        for room in self.server.rooms:
            session.push(room + '\r\n')

    def do_new(self, session, line):
        'Handles the new command, used to open a new room.'
        name = line.strip()
        if not name:
            session.push('Please enter a room name\r\n')
        elif name in self.server.rooms:
            session.push('The name "%s" is taken.\r\n' % name)
            session.push('Please try again.\r\n')
        else:
            self.server.rooms[name] = ChatRoom(self.server)

    def do_login(self, session, line):
        'Handles the login command, used to login into a room.'
        if not line.strip(): return
        try:
            room, user = line.split(' ', 1)
        except ValueError:
            session.push('Please enter a user name\r\n')
        else:
            user = user.strip()
            if room not in self.server.rooms:
                session.push('The room name "%s" doesn\'t exist.\r\n' % room)
                session.push('Please [look] for a room.\r\n')
                return
            if not user:
                session.push('Please enter a user name\r\n')
                return
            if user in self.server.users:
                session.push('The user name "%s" is taken.\r\n' % user)
                session.push('Please try again.\r\n')
                return
            session.name = user
            session.enter(self.server.rooms[room])


class ChatRoom(Room):
    """
    A room meant for multiple users who can chat with the others in
    the room.
    """

    def add(self, session):
        # Notify everyone that a new user has entered:
        self.broadcast(session.name + ' has entered the room\r\n')
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        Room.remove(self, session)
        del self.server.users[session.name]
        # Notify everyone that a user has left:
        self.broadcast(session.name + ' has left the room.\r\n')

    def unknown(self, session, line):
        self.broadcast(session.name+': '+line+'\r\n')

    def do_look(self, session, line):
        'Handles the look command, used to see who is in a room'
        session.push('The following are in this room:\r\n')
        for other in self.sessions:
            session.push(other.name + '\r\n')

    def do_logout(self, session, line):
        'Handles the logout command, used to go back to LoginRoom'
        session.enter(LoginRoom(self.server))


class EndRoom(Room):
    """
    When a user quit, he come into this room but do nothing.
    """


class ChatSession(async_chat):
    """
    A single session, which takes care of the communication with a
    single user.
    """

    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator('\r\n')
        self.data = []
        self.name = None
        # All sessions begin in a separate LoginRoom:
        self.enter(LoginRoom(server))

    def enter(self, room):
        # Remove self from current room and add self to
        # next room...
        try: cur = self.room
        except AttributeError: pass
        else: cur.remove(self)
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        line = ''.join(self.data)
        self.data = []
        try: self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(EndRoom(self.server))


class ChatServer(dispatcher):
    """
    A chat server with a single room.
    """
    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.name = name
        self.users = {}
        self.rooms = {}

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)


if __name__ == '__main__':
    ChatServer(PORT, NAME)
    try: asyncore.loop()
    except KeyboardInterrupt: print
