from dotenv import load_dotenv
from notifications import send_message, notify_owner
import json
load_dotenv()

send_message("Test", "If you can read this, notifications work.", "<p>If you can read this, notifications work.</p>")
print(json.dumps(notify_owner.params_json_schema, indent=2))
