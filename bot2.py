import urllib.request
import urllib.parse
import json
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

TOKEN = "8580320767:AAE-k9f6dp3grRjPdqaQ_AvEGl7jC208ZlI"
GROUP_ID = -1003500099610

API_URL = f"https://api.telegram.org/bot{TOKEN}/"

def request(method, data=None):
    url = API_URL + method
    if data:
        data = urllib.parse.urlencode(data).encode()
    try:
        with urllib.request.urlopen(url, data=data) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as e:
        print("HTTP ERROR:", e.read().decode())
        return None

def get_updates(offset=None):
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    return request("getUpdates", params)

def copy_message(from_chat_id, message_id):
    return request("copyMessage", {
        "chat_id": GROUP_ID,
        "from_chat_id": from_chat_id,
        "message_id": message_id
    })

def main():
    offset = None

    while True:
        updates = get_updates(offset)

        if updates and updates.get("ok"):
            for update in updates["result"]:
                offset = update["update_id"] + 1

                if "message" in update:
                    message = update["message"]

                    if message["chat"]["type"] == "private":
                        copy_message(
                            message["chat"]["id"],
                            message["message_id"]
                        )

        time.sleep(1)

if __name__ == "__main__":
    main()