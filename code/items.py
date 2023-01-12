class Item:
    def __init__(self, item_type, name: str, modifiers: dict):
        self.type = item_type
        self.name = name
        self.modifiers = modifiers

    def __str__(self):
        return f"[{self.name}] " + ", ".join(f"{mod}:{val}" for mod, val in self.modifiers.items())