import logging
import socket as S
from collections import namedtuple
from pyirclogs import Message
from datetime import datetime


logger = logging.getLogger('irc_client')

class IRCClient:
    LowLvlMsg = namedtuple('LowLvlMsg', ['sender', 'verb', 'content'])

    def __init__(self, nick, desc):
        self.nick, self.desc = nick, desc
        self.sock = S.socket(S.AF_INET, S.SOCK_STREAM)

    def send(self, text):
        logger.debug("SENDING '%s'" % text)
        return self.sock.send((text + '\r\n').encode())

    def recv(self, size):
        res = self.sock.recv(size).decode()
        logger.debug("RECEIVING '%s'" % res.strip())
        return res

    def parse(self, line):
        origin, verb, content = line.split(' ', 2)
        return self.LowLvlMsg(origin.lstrip(':'), verb, content)

    def lines(self, chans):
        self.sock.connect(('irc.freenode.net', 6667))
        self.send("NICK %s" % self.nick)
        self.send("USER %s * * :%s" % (self.nick, self.desc))

        identified = False

        buf = ''
        while True:
            # Read from server
            r = self.recv(1024)
            if len(r) == 0:
                return

            # Append to our internal buffer
            buf += r

            # Split into lines, keep last line in buffer if incomplete
            lines = buf.split('\r\n')
            if buf.endswith('\n'):
                buf = ''
            else:
                lines, buf = lines[:-1], lines[-1]

            for line in lines:
                if not line:
                    continue

                # Handle ping
                if line.startswith('PING'):
                    answer = line.replace('PING', 'PONG')
                    self.send(answer)
                    logger.info(answer)
                    continue

                # Parse IRC protocol message
                msg = self.parse(line)

                # WELCOMED
                if msg.verb == '001':
                    if not identified:
                        for chan in chans:
                            self.send('JOIN %s' % chan)
                            logger.info("Joining %s", chan)
                    identified = True
                # Actual text message
                elif msg.verb == 'PRIVMSG':
                    nick = msg.sender.split('!', 1)[0]
                    chan, text = msg.content.split(' :', 1)
                    action = text.startswith('\x01ACTION ') and text.endswith('\x01')
                    if action:
                        text = text[8:-1]
                    yield Message(
                        time=datetime.now(),
                        nick=nick,
                        chan=chan,
                        action=action,
                        op=False,
                        text=text
                    )
                else:
                    logger.debug("MSG %s", msg)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    client = IRCClient("iTitest", "Titou testing things")
    for msg in client.lines(['#titoufaitdestests']):
        print(msg)
