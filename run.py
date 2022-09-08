from util.Scheduler import Scheduler
from util.Parser import Parser
import json

# import configuration data
with open("config.json", "r") as read_file:
    data = json.load(read_file)

# init parser and scheduler

parser = Parser(data["WATCH_DIR"], data["PROCESS_NAME"], data["SEPARATOR"])
scheduler = Scheduler(data["WATCH_DIR"], data["PROCESS_NAME"], parser)
scheduler.start()