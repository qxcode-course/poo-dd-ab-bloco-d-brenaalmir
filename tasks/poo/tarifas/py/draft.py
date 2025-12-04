class Operation:
    def __init__(self, op_id, label, value):
        self.id = op_id
        self.label = label
        self.value = value

    def __str__(self):
        return f"{self.id}:{self.label}:{self.value}"