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
    def __init__(self, name=""):
        self.name = name
        self.fones = []
        self.favorited = False

    def add(self, label, number):
        if not is_valid(number):
            print("fail: invalid number")
            return
        self.fones.append(Fone(label, number))

    def rm(self, index):
        if 0 <= index < len(self.fones):
            self.fones.pop(index)

    def tfav(self):
        self.favorited = not self.favorited

    def __str__(self):
        prefix = "@ " if self.favorited else "- "
        lista = ", ".join(str(f) for f in self.fones)
        return f"{prefix}{self.name} [{lista}]"


def main():
    contact = Contact()
    while True:

        line = input().strip()
        if line == "":
            continue
        print("$" + line)
        args = line.split()

        if args[0] == "end":
            break

        elif args[0] == "init":
            name = args[1] if len(args) > 1 else ""
            contact = Contact(name)

        elif args[0] == "show":
            print(contact)

        elif args[0] == "add":
            label = args[1]
            number = args[2]
            contact.add(label, number)

        elif args[0] == "rm":
            index = int(args[1])
            contact.rm(index)

        elif args[0] == "tfav":
            contact.tfav()

        else:
            print("fail: comando invalido")


main()