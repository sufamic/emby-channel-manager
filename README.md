
# Emby Live TV Channel Manager

A Python utility to manage Emby Live TV channels. It allows you to quickly **enable**, **disable**, or **disable unmapped** channels using the Emby API.

## Features
- Enable all channels
- Disable all channels
- Disable only unmapped channels (channels without a `ListingsProviderId`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sufamic/emby-channel-manager
   cd emby-channel-manager
   ```
2. Install dependencies:
   ```bash
   pip install requests tqdm python-dotenv
   ```
2. Modify the `.env` file to include the following:
   ```
   API_KEY=your_emby_api_key
   BASE_URL=http://your-emby-server:8096
   ```


## Usage
Run the script with one of three modes:
```bash
python manage_channels.py enable
python manage_channels.py disable
python manage_channels.py disable_unmapped
```

### Example
Enable all channels:
```bash
python manage_channels.py enable
```

Disable all channels:
```bash
python manage_channels.py disable
```

Disable unmapped channels:
```bash
python manage_channels.py disable_unmapped
```

## License
MIT License
