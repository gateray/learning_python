#!/usr/bin/env python
# coding: utf-8

import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self._encrypt_pw(password)
        self.is_logged_in = False
    def _encrypt_pw(self,password):
        hash_string = (self.username + password)
        hash_string = hash_string.encode("utf8")
        return hashlib.sha256(hash_string).hexdigest()
    def check_password(self, password):
        encrypted = self._encrypt_pw(password)
        return encrypted == self.password

#认证的exception定义
class AuthException(Exception):
    def __init__(self, username, user=None):
        super().__init__(username)
        self.username = username
        self.user = user

class UsernameAlreadyExists(AuthException):
    pass

class PasswordTooShort(AuthException):
    pass

class InvalidUsername(AuthException):
    pass

class InvalidPassword(AuthException):
    pass

class NotLoggedInError(AuthException):
    pass

class Authenticator:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password):
        if username in self.users:
            raise UsernameAlreadyExists(username)
        if len(password) < 6:
            raise PasswordTooShort(username)
        self.users[username] = User(username, password)

    def login(self, username, password):
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)

        if not user.check_password(password):
            raise InvalidPassword(username, user)
        user.is_logged_in = True
        return True

    def is_logged_in(self, username):
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)
        return user.is_logged_in

#授权的exception的定义
class PermissionError(Exception):
    pass

class NotPermittedError(Exception):
    pass

class Authorizor:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}
    def add_permission(self, perm_name):
        if perm_name not in self.permissions:
            self.permissions[perm_name] = set()
        else:
            raise PermissionError("Permission Exists")
    #授予用户特定的权限
    def permit_user(self, perm_name, username):
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permission does not exist")
        else:
            if username not in self.authenticator.users:
                raise InvalidUsername(username)
            perm_set.add(username)
    def check_permission(self, perm_name, username):
        if not self.authenticator.is_logged_in(username):
            raise NotLoggedInError(username)
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permission does not exist")
        else:
            if username not in perm_set:
                raise NotPermittedError("{} is not permitted".format(username))
            else:
                return True

class Editor:
    authenticator = Authenticator()
    authorizor = Authorizor(authenticator)
    def __init__(self):
        self.username = None
        self.menu_map = {
            "login": self.login,
            "test": self.test,
            "change": self.change,
            "quit": self.quit
        }

    def login(self):
        logged_in = False
        while not logged_in:
            username = input("username: ")
            password = input("password: ")
            try:
                logged_in = Editor.authenticator.login(username, password)
            except InvalidUsername:
                print("Sorry, that username does not exist")
            except InvalidPassword:
                print("Sorry, incorrect password")
            else:
                self.username = username

    def is_permitted(self, permisstion):
        try:
            Editor.authorizor.check_permission(permisstion,self.username)
        except NotLoggedInError as e:
            print("{} is not logged in".format(e.username))
            return False
        except PermissionError as e:
            print("{} is not exist".format(permisstion))
        except NotPermittedError as e:
            print("{} cannot {}".format(self.username, permisstion))
            return False
        else:
            return True

    def test(self):
        if self.is_permitted("test program"):
            print("Testing program now...")

    def change(self):
        if self.is_permitted("change program"):
            print("changing program now...")

    def quit(self):
        raise SystemExit()

    def menu(self):
        try:
            while True:
                print("""
Please enter a command:
\tlogin\tLogin
\ttest\tTest the program
\tchange\tChange the program
\tquit\tQuit
""")
                answer = input("enter a command: ").lower()
                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print("{} is not a valid option".format(answer))
                else:
                    func()
        finally:
            print("Thank you for testing the auth module")

if __name__ == '__main__':
    Editor.authenticator.add_user("user1","123456")
    Editor.authorizor.add_permission("test program")
    Editor.authorizor.add_permission("change program")
    Editor.authorizor.permit_user("test program", "user1")
    Editor().menu()

