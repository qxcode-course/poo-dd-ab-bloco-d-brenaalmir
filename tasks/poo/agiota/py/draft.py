class Transaction:
    def  __init__(self, tid, label, client, value):
        self.id = tid
        self.label = label
        self.client = client
        self.value = value

    def __str__(self):
        return f"id:{self.id} {self.label}:{self.client} {self.value}"

class Client:
    def __init__(self, codename, limit):
        self.codename = codename
        self.limit = limit
        self.ops = []

    def addOp(self, op):
        self.ops.append(op)

    def getBalance(self):
        total = 0
        for op in self.ops:
            if op.label == "give":
                total += op.value
            elif op.label == "take":
                total -= op.value
            elif op.label == "plus":
                total += op.value
        return total

    def __str__(self):
        return f"{self.codename} {self.getBalance()}/{self.limit}"


class Agiota:
    def __init__(self):
        self.clients = []
        self.dead = []
        self.trans = []
        self.nextId = 0

    def findClient(self, name, inDead=True):
        for c in self.clients:
            if c.codename == name:
                return c
        if inDead:
            for c in self.dead:
                if c.codename == name:
                    return c
        return None

    def addClient(self, name, limit):
        if self.findClient(name) is not None:
            print("fail: cliente ja existe")
            return
        self.clients.append(Client(name, limit))
        self.clients.sort(key=lambda c: c.codename)

    def newTransaction(self, label, client, value):
        op = Transaction(self.nextId, label, client.codename, value)
        self.nextId += 1
        self.trans.append(op)
        client.addOp(op)

    def give(self, name, value):
        cli = self.findClient(name, False)
        if cli is None:
            print("fail: cliente nao existe")
            return
        if cli.getBalance() + value > cli.limit:
            print("fail: limite excedido")
            return
        self.newTransaction("give", cli, value)

    def take(self, name, value):
        cli = self.findClient(name, False)
        if cli is None:
            print("fail: cliente nao existe")
            return
        self.newTransaction("take", cli, value)

    def kill(self, name):
        cli = self.findClient(name, False)
        if cli is None:
            print("fail: cliente nao existe")
            return
        historico = [op for op in self.trans if op.client == name]
        historico.sort(key=lambda op: op.id)
        cli.ops = historico[:]
        self.clients.remove(cli)
        self.dead.append(cli)
        self.dead.sort(key=lambda c: c.codename)
        self.trans = [op for op in self.trans if op.client != name]

    def plus(self):
        toKill = []
        for cli in self.clients:
            juros = int((cli.getBalance() * 0.10) + 0.9999)
            self.newTransaction("plus", cli, juros)
            if cli.getBalance() > cli.limit:
                toKill.append(cli.codename)
        for name in toKill:
            self.kill(name)

    def show(self):
        for c in self.clients:
            print(f":) {c}")
        trans_sorted = sorted(self.trans, key=lambda op: op.id) 
        for op in trans_sorted:
            print(f"+ {op}")
        for d in self.dead:
            print(f":( {d}") 
            
        for d in self.dead:
            for op in d.ops:
                print(f"- {op}")

    def showCli(self, name):
        cli = self.findClient(name) or self.findClient(name, True)
        if cli is None:
            print("fail: cliente nao existe")
            return
        print(cli)
        for op in cli.ops:
            print(f"id:{op.id} {op.label}:{op.client} {op.value}")

def main():
    agiota = Agiota()
    while True:
        line = input().strip()
        if line == "":
            continue
        print("$" + line)
        args = line.split()

        if args[0] == "end":
            break

        elif args[0] == "addCli":
            agiota.addClient(args[1], int(args[2]))

        elif args[0] == "give":
            agiota.give(args[1], int(args[2]))

        elif args[0] == "take":
            agiota.take(args[1], int(args[2]))

        elif args[0] == "show":
            agiota.show()

        elif args[0] == "showCli":
            agiota.showCli(args[1])

        elif args[0] == "kill":
            agiota.kill(args[1])

        elif args[0] == "plus":
            agiota.plus()

        else:
            print("fail: comando invalido")

main()