class UserManager:
    def login(self, username, password):
        if username == 'catconv' and password == {'i': '00', 'k': '01', 't': '1'}:
            return True
        else:
            return False

