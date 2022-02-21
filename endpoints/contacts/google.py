from flask_jsonrpc import JSONRPCBlueprint

from logger import CustomLogger

google_contacts = JSONRPCBlueprint("contacts", __name__)
log = CustomLogger()
