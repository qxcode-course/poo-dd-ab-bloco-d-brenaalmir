class Coin:
    def __init__(self, value: float, volume: int, label: str):
        self.value = value
        self.volume = volume
        self.label = label

    def toString(self):
        return f"{self.value:.2f}:{self.volume}"

    def getValue(self):
        return self.value

    def getVolume(self):
        return self.volume

    def getLabel(self):
        return self.label


C10 = Coin(0.10, 1, "C10")
C25 = Coin(0.25, 2, "C25")
C50 = Coin(0.50, 3, "C50")
C100 = Coin(1.00, 4, "C100")

COIN_MAP = {
    10: C10,
    25: C25,
    50: C50,
    100: C100
}


class Item:
    def __init__(self, label: str, volume: int):
        self.label = label
        self.volume = volume

    def getLabel(self):
        return self.label

    def getVolume(self):
        return self.volume

    def toString(self):
        return f"{self.label}:{self.volume}"


class Pig:
    def __init__(self, volumeMax: int):
        self.items = []
        self.coins = []
        self.volumeMax = volumeMax
        self.broken = False

    def currentVolume(self):
        if self.broken:
            return 0
        vol = 0
        for coin in self.coins:
            vol += coin.getVolume()
        for item in self.items:
            vol += item.getVolume()
        return vol

    def addCoin(self, coin: Coin):
        if self.broken:
            print("fail: the pig is broken")
            return False
        if self.currentVolume() + coin.getVolume() > self.volumeMax:
            print("fail: the pig is full")
            return False
        self.coins.append(coin)
        return True

    def addItem(self, item: Item):
        if self.broken:
            print("fail: the pig is broken")
            return False
        if self.currentVolume() + item.getVolume() > self.volumeMax:
            print("fail: the pig is full")
            return False
        self.items.append(item)
        return True

    def getValue(self):
        return sum(c.getValue() for c in self.coins)

    def breakPig(self):
        if self.broken:
            print("fail: the pig is already broken")
            return False
        self.broken = True
        return True

    def extractCoins(self):
        if not self.broken:
            print("fail: you must break the pig first")
            return []
        arr = self.coins[:]
        self.coins = []
        return arr

    def extractItems(self):
        if not self.broken:
            print("fail: you must break the pig first")
            return []
        arr = self.items[:]
        self.items = []
        return arr

    def toString(self):
        state = "broken" if self.broken else "intact"
        coins = ", ".join(c.toString() for c in self.coins)
        items = ", ".join(i.toString() for i in self.items)
        value = self.getValue()
        vol = self.currentVolume()
        return f"state={state} : coins=[{coins}] : items=[{items}] : value={value:.2f} : volume={vol}/{self.volumeMax}"


def main():
    pig = None

    while True:
        try:
            line = input().strip()
        except EOFError:
            break

        if line == "":
            break

        print("$" + line)

        args = line.split()
        cmd = args[0]

        if cmd == "end":
            break

        elif cmd == "init":
            pig = Pig(int(args[1]))

        elif cmd == "addCoin":
            value = int(args[1])
            pig.addCoin(COIN_MAP[value])

        elif cmd == "addItem":
            label = args[1]
            volume = int(args[2])
            pig.addItem(Item(label, volume))

        elif cmd == "break":
            pig.breakPig()

        elif cmd == "extractCoins":
            arr = pig.extractCoins()
            print("[" + ", ".join(c.toString() for c in arr) + "]")

        elif cmd == "extractItems":
            arr = pig.extractItems()
            print("[" + ", ".join(i.toString() for i in arr) + "]")

        elif cmd == "show":
            print(pig.toString())


main()