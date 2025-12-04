class Fone:
    def __init__(self, label, number):
        self.label = label
        self.number = number

    def __str__(self):
        return f"{self.label}:{self.number}"

def is_valid(number):
    valid = "0123456789()."
    for c in number:
        if c not in valid:
            return False
    return True


class Contact:
    def __init__(self, name):
        self.name = name
        self.fones = []
        self.favorited = False 

    def addFone(self, label, number):
        if not is_valid(number):
            print("fail: invalid number")
            return
        self.fones.append(Fone(label, number))

    def rmFone(self, index):
        if 0 <= index < len(self.fones):
            self.fones.pop(index)

    def toggleFavorited(self):
        self.favorited = not self.favorited

    def isFavorited(self):
        return self.favorited

    def __str__(self):
        prefix = "@" if self.favorited else "-"
        lista = ", ".join(str(f) for f in self.fones)
        return f"{prefix} {self.name} [{lista}]"


class Agenda:
    def __init__(self):
        self.contacts = []

    def findPosByName(self, name):
        for i, c in enumerate(self.contacts):
            if c.name == name:
                return i
        return -1

    def addContact(self, name, fones):
        pos = self.findPosByName(name)
        if pos == -1:
            contact = Contact(name)
            for f in fones:
                contact.addFone(f[0], f[1])
            self.contacts.append(contact)
        else:
            contact = self.contacts[pos]
            for f in fones:
                contact.addFone(f[0], f[1])
        self.contacts.sort(key=lambda c: c.name)

    def getContact(self, name):
        pos = self.findPosByName(name)
        if pos != -1:
            return self.contacts[pos]
        return 

    def rmContact(self, name):
        pos = self.findPosByName(name)
        if pos != -1:
            self.contacts.pop(pos)

    def search(self, pattern):
        resultados = []
        for cont in self.contacts:
            texto = str(cont)
            if pattern in texto:
                resultados.append(cont)
        return resultados

    def getFavorited(self):
        favs = []
        for cont in self.contacts:
            if cont.isFavorited():
                favs.append(cont)
        return favs

    def getContacts(self):
        return self.contacts

    def __str__(self):
        return "\n".join(str(c) for c in self.contacts)


def main():
    agenda = Agenda()

    while True:
        line = input().strip()
        if line == "":
            continue
        print("$" + line)
        args = line.split()

        if args[0] == "end":
            break

        elif args[0] == "add":
            name = args[1]
            fones_list = []
            for par in args[2:]:
                label, num = par.split(":")
                fones_list.append((label, num))
            agenda.addContact(name, fones_list)

        elif args[0] == "show":
            print(agenda)

        elif args[0] == "rm":
            name = args[1]
            agenda.rmContact(name)

        elif args[0] == "rmFone":
            name = args[1]
            index = int(args[2])
            cont = agenda.getContact(name)
            if cont is not None:
                cont.rmFone(index)

        elif args[0] == "search":
            pattern = args[1]
            resultados = agenda.search(pattern)
            for c in resultados:
                print(c)

        elif args[0] == "tfav":
            name = args[1]
            cont = agenda.getContact(name)
            if cont:
                cont.toggleFavorited()

        elif args[0] == "favs":
            favs = agenda.getFavorited()
            for c in favs:
                print(c)

        else:
            print("fail: comando invalido")

main() 