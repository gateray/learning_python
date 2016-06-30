#!/usr/bin/env python
# coding: utf-8

class ContactList(list):
    def search(self, name):
        matching_contacts = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts

class Contact:
    all_contacts = ContactList()
    def __init__(self, name, email, **kwargs):
        self.name = name
        self.email = email
        Contact.all_contacts.append(self)

    def display(self):
        print("name: {}, email: {}".format(self.name, self.email))

# class Friend(Contact):
#     def __init__(self, name, email, phone):
#         super().__init__(name,email)
#         self.phone = phone


class AddressHolder:
    def __init__(self, street='', city='', state='', code='', **kwargs):
        super().__init__(**kwargs)
        self.street = street
        self.city = city
        self.state = state
        self.code = code
    def display(self):
        print("street: {}, city: {}, state: {}, code: {}".format(self.street,self.city,self.state,self.code))

class Friend(Contact, AddressHolder):
    def __init__(self, phone='', **kwargs):
        print(kwargs)
        super().__init__(**kwargs)
        self.phone = phone
        self.ext = kwargs
    def display(self):
        print("name: {name}, email: {email}, phone: {phone},  "
              "city: {city},  code: {code}".format(phone=self.phone,**self.ext))

if __name__ == '__main__':
    f1 = Friend('13539720475', name='user1', email='user1@126.com', city='gz')
    f2 = Friend('18675820370', name='user2', email='user2@163.com', city='bj', code='010')
    print(f1)
    print(f1.all_contacts)
    print(f2.all_contacts.search("user1"))
    print(f2.all_contacts.search("user2")[0].display())

