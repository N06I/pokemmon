from raw import areaExits


class CommandLine:
    def __init__(self, game):
        self.game = game

    def execute(self, command_str):
        args = command_str.split()
        command = args[0]
        if command == "tp":
            if len(args) == 3:
                area = args[1]
                if area in areaExits:
                    pos_str = args[2].strip("()").split(",")
                    pos = (int(pos_str[0]), int(pos_str[1]))
                    print(f"area: {area}, pos: {pos_str}")
                    self.game.world.load_area((area, pos))
            else:
                pos_str = args[1].strip("()").split(",")
                pos = (int(pos_str[0]), int(pos_str[1]))
                self.game.world.area.character.teleport(pos)
