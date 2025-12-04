class Pet:
    def __init__(self, pid, name, specie):
        self.id = pid
        self.name = name
        self.specie = specie

    def __str__(self):
        return f"{self.id}:{self.name}:{self.specie}"


class Client:
    def __init__(self, cid, fullname):
        self.id = cid
        self.fullname = fullname
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)
        return True

    def get_pet(self, name):
        for p in self.pets:
            if p.name == name:
                return p
        return None

    def del_pet(self, name):
        for i, p in enumerate(self.pets):
            if p.name == name:
                self.pets.pop(i)
                return True
        return False

    def __str__(self):
        pets_str = "".join(f"[{p}]" for p in self.pets)
        if pets_str:
            return f"{self.id}: {self.fullname} {pets_str}"
        else:
            return f"{self.id}:{self.fullname}"
        

class Service:
    def __init__(self, sid, price):
        self.id = sid
        self.price = float(price)

    def __str__(self):
        return f"{self.id}:{self.price}"


class Sale:
    def __init__(self, sid, client_id, pet_name, service_id):
        self.id = sid
        self.client_id = client_id
        self.pet_name = pet_name
        self.service_id = service_id

    def __str__(self):
        return f"{self.id}:{self.client_id}:{self.pet_name}:{self.service_id}"


class Clinic:
    def __init__(self):
        self.clients = []
        self.services = {}
        self.sales = []
        self.next_pet_id = 1
        self.next_sale_id = 0

    def find_client(self, cid):
        for c in self.clients:
            if c.id == cid:
                return c
        return None

    def add_client(self, cid, fullname):
        c = self.find_client(cid)
        if c is not None:
            if c.fullname != fullname:
                print(f"fail: cliente {cid} ja cadastrado.")
            return
        self.clients.append(Client(cid, fullname))

    def get_client(self, cid):
        c = self.find_client(cid)
        if c is None:
            print(f"fail: cliente {cid} nao existe")
            return None
        s = f"{c.id}:{c.fullname}"
        print(s)
        return c

    def del_client(self, cid):
        for i, c in enumerate(self.clients):
            if c.id == cid:
                self.clients.pop(i)
                return True
        return False

    def list_clients(self):
        for c in self.clients:
            print(str(c))

    def add_pet(self, cid, petname, specie):
        cli = self.find_client(cid)
        if cli is None:
            print(f"fail: cliente {cid} nao existe")
            return
        if cli.get_pet(petname) is not None:
            print(f"fail: animal {petname} ja existe")
            return
        pet = Pet(self.next_pet_id, petname, specie)
        self.next_pet_id += 1
        cli.add_pet(pet)

    def add_service(self, sid, price):
        if sid not in self.services:
            self.services[sid] = Service(sid, price)

    def list_services(self):
        for sid, svc in self.services.items():
            print(str(svc))

    def sell(self, cid, petname, sid):
        cli = self.find_client(cid)
        if cli is None:
            print(f"fail: cliente {cid} nao existe")
            return
        pet = cli.get_pet(petname)
        if pet is None:
            print(f"fail: animal {petname} nao existe")
            return
        svc = self.services.get(sid)
        if svc is None:
            print(f"fail: servico {sid} nao existe")
            return
        sale = Sale(self.next_sale_id, cid, petname, sid)
        self.next_sale_id += 1
        self.sales.append(sale)

    def list_sales(self):
        for s in self.sales:
            print(str(s))

    def balance(self):
        total = 0.0
        for s in self.sales:
            svc = self.services.get(s.service_id)
            if svc:
                total += svc.price
        print(total)


def main():
    clinic = Clinic()
    while True:
        line = input().strip()
        if line == "":
            continue
        print("$" + line)                  
        args = line.split()

        if args[0] == "end":
            break

        elif args[0] == "addcli":
            cid = args[1]
            fullname = " ".join(args[2:])
            clinic.add_client(cid, fullname)

        elif args[0] == "getcli":
            clinic.get_client(args[1])

        elif args[0] == "show":
            clinic.list_clients()

        elif args[0] == "delcli":
            clinic.del_client(args[1])

        elif args[0] == "addpet":
            clinic.add_pet(args[1], args[2], args[3])

        elif args[0] == "addser":
            clinic.add_service(args[1], args[2])

        elif args[0] == "listser":
            clinic.list_services()

        elif args[0] == "sell":
            clinic.sell(args[1], args[2], args[3])

        elif args[0] == "listsell":
            clinic.list_sales()

        elif args[0] == "balance":
            clinic.balance()

        else:
            print("fail: comando invalido")
            
main()