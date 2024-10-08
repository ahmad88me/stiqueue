from stiqueue import SQServer


class SQServer2(SQServer):
    def other_actions(self, action_msg):
        action = action_msg[:self.action_len]
        if len(action_msg) >= self.action_len:
            msg = action_msg[self.action_len:]
            if action == b"rev":
                self.enq(msg[::-1])
            elif action == b"prt":
                self.logger.debug("printing the queue: ")
                for i, msg in enumerate(self.q):
                    self.logger.debug("q(%d)> %s" % (i, msg))
            else:
                self.logger.error("ERROR: invalid action:")
                self.logger.error(action_msg)
                self.logger.error(action)
        else:
            self.logger.error("Error: invalid action length:")
            self.logger.error(action_msg)
            self.logger.error(action)


if __name__ == '__main__':
    server = SQServer2()
    server.listen()
