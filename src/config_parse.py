#Module for parsing configuration files
from random import seed


def config_read(path: str):
    seed = 42
    try:
        with open(path) as file:
            text = file.read().split('\n')

            for line in text:
                line = line.strip()

                if not line or line[0] == '#':
                    continue

                line = line.split('=')

                if len(line) != 2:
                    return "ERROR"

                param = line[0].strip()
                value = line[1].strip()

                match param:
                    case "WIDTH":
                        width = int(value)

                    case "HEIGHT":
                        height = int(value)

                    case "ENTRY":
                        value = value.split(',')

                        if len(value) != 2:
                            return "ERROR"

                        entry = (int(value[0]), int(value[1]))

                    case "EXIT":
                        value = value.split(',')

                        if len(value) != 2:
                            return "ERROR"

                        exit = (int(value[0]), int(value[1]))

                    case "OUTPUT_FILE":
                        output_file = value

                    case "PERFECT":
                        if value == "True":
                            perfect = True
                        elif value == "False":
                            perfect = False
                        else:
                            return "ERROR"
                    case "SEED":
                        seed = int(value)

        return (width, height, entry, exit, output_file, perfect, seed)

    except (OSError, ValueError):
        return "ERROR"

def config_parse(width: int, height: int, entry: tuple, exit: tuple, output_file: str, perfect: bool, seed: int):

    if width <= 0 or height <= 0:
        return "ERROR"

    if entry[0] < 0 or entry[0] >= width or entry[1] < 0 or entry[1] >= height:
        return "ERROR"

    if exit[0] < 0 or exit[0] >= width or exit[1] < 0 or exit[1] >= height:
        return "ERROR"

    if not output_file:
        return "ERROR"

    return (width, height, entry, exit, output_file, perfect, seed)
