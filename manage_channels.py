"""
Emby Live TV Channel Manager
Source: https://github.com/sufamic/emby-channel-manager/
License: MIT License

This script allows you to enable all channels, disable all channels,
or disable only unmapped channels in Emby Live TV using the Emby API.
"""

from sys import argv, exit
from requests import get, post
from json import loads
from tqdm import tqdm
from dotenv import load_dotenv
from os import getenv

# Load environment variables from .env
load_dotenv()
api_key = getenv("API_KEY")
base_url = getenv("BASE_URL")
headers = {"X-Emby-Token": str(api_key)}

# Validate command-line arguments
if len(argv) != 2 or argv[1] not in ["enable", "disable", "disable_unmapped"]:
    print("Usage: python manage_channels.py [enable|disable|disable_unmapped]")
    exit(1)

# Determine desired state based on mode
mode = {"enable": False, "disable": True, "disable_unmapped": None}[argv[1]]

# Fetch all channels from Emby API
channels = loads(get(f"{base_url}/LiveTv/Manage/Channels?api_key={api_key}").text)["Items"]

# Loop through each channel and update its disabled state if needed
for channel in tqdm(channels, total=len(channels), unit="channel", colour="green"):
    # Determine target disabled state for this channel
    disable = mode if mode is not None else "ListingsProviderId" not in channel
    # Skip if already in desired state
    if channel.get("Disabled") == disable: 
        continue
    # Construct API endpoint and request body
    url = f"{base_url}/LiveTv/Manage/Channels/{channel['Id']}/Disabled"
    body = {"Id": channel["Id"], "ManagementId": channel["ManagementId"], "Disabled": disable}
    # Send POST request to update channel
    post(url, headers=headers, json=body)
