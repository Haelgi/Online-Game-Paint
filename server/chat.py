class Chat(object):

    def __init__(self, r):
        self.content = ['sdfsdf', 'sdfsdfsdf']
        self.round = r

    def update_chat(self, msg):
        """add one massage to list content chat

        Args:
            msg (txt): 'msg1'
        """
        # TODO функция работает, но на ней все стопится
        self.content.append(msg)

    def get_chat(self):
        """retutne all content in chat

        Returns:
            list: ['msg1', 'msg2'...]
        """
        return self.content

    def __len__(self):
        """msg quantity on chat

        Returns:
            num: 1....40
        """
        return len(self.content)

    def __str__(self):
        """convert list of msg chats to one string (for json)

        Returns:
            str: 'msg1, msg2...'
        """
        return "".join(self.content)

    def __repr__(self):
        """return Chat obj as string

        Returns:
            str: '< Chat obj >'
        """
        return str(self)

