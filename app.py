import sys
from requests import get, post
from json import loads
from tqdm import tqdm
from dotenv import load_dotenv
from os import getenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

api_key = getenv("API_KEY")
base_url = getenv("BASE_URL")
headers = {"X-Emby-Token": api_key}

def update_channel(channel, disable=None):
    url = f"{base_url}/LiveTv/Manage/Channels/{channel['Id']}/Disabled"
    if disable is None:
        disable = "ListingsProviderId" not in channel
    body = {"Id": channel["Id"], "ManagementId": channel["ManagementId"], "Disabled": disable}
    post(url, headers=headers, json=body)

if len(sys.argv) != 2 or sys.argv[1] not in ["enable", "disable", "disable_unmapped"]:
    print("Usage: python manage_channels.py [enable|disable|disable_unmapped]")
    sys.exit(1)

mode = sys.argv[1]
channels = loads(get(f"{base_url}/LiveTv/Manage/Channels?api_key={api_key}").text)["Items"]

with ThreadPoolExecutor() as executor:
    if mode == "enable":
        list(tqdm(executor.map(lambda c: update_channel(c, False), channels), total=len(channels), desc="Enabling all channels", unit="channels", colour="green"))
    elif mode == "disable":
        list(tqdm(executor.map(lambda c: update_channel(c, True), channels), total=len(channels), desc="Disabling all channels", unit="channels", colour="green"))
    else:
        list(tqdm(executor.map(lambda c: update_channel(c, None), channels), total=len(channels), desc="Disabling unmapped channels", unit="channels", colour="green"))
