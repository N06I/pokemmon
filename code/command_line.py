import pygame

from raw import areaExits


class CommandLine:
    def __init__(self, chat, world):
        self.chat = chat
        self.world = world
        self.commands = ["tp"]
        pass

    def execute(self, command_str):
        args = command_str.split()
        command = args[0]
        if command in self.commands:
            if command == "tp":
                if args[1] in areaExits:
                    area = args[1]
                    if len(args) == 2:
                        self.world.load_area((area, (0, 0)))
                    else:
                        pos_str = args[2].strip("()").split(",")
                        pos = (int(pos_str[0]), int(pos_str[1]))
                        print(f"area: {area}, pos: {pos_str}")
                        self.world.load_area((area, pos))
                else:
                    pos_str = args[1].strip("()").split(",")
                    try:
                        pos = (int(pos_str[0]), int(pos_str[1]))
                    except ValueError:
                        return
                    self.world.area.character.teleport(pygame.Vector2(pos))
        elif command in self.chat.chan_names:  # .chat.chan_names
            self.chat.channel_switch(command)
            if len(args) > 1:
                self.chat.send(command_str.split(command + " ")[1])
