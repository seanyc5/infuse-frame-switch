# Infuse Frame Rate Switcher

Automatically switches your display's refresh rate to 24Hz when Infuse is running, providing smoother playback for movies. When Infuse is closed, it restores your original refresh rate.

## Prerequisites

- macOS
- [Infuse](https://firecore.com/infuse) media player
- Python 3
- Homebrew (for installing displayplacer)

## Installation

1. Clone or download this repository:
```bash
git clone https://github.com/seanyc5/infuse-frame-switch
cd infuse-frame-switch



# Run the installer  -- This should install for you if not manual instructions below. 
./install.sh
```

2. Install displayplacer using Homebrew:
```bash
brew install jakehilborn/jakehilborn/displayplacer
```

3. Get your display ID:
```bash
displayplacer list
```
Look for your display's ID in the output (it will look something like "012A6609-58A0-45FF-8F55-8538870D40BB")

4. Edit `infuse_frame_switch.py` and replace the `display_id` value with your display's ID.

5. Make the script executable:
```bash
chmod +x infuse_frame_switch.py
```

6. Set up auto-start:
```bash
# Create LaunchAgents directory if it doesn't exist
mkdir -p ~/Library/LaunchAgents

# Copy the launch agent plist
cp com.infuse.frameswitch.plist ~/Library/LaunchAgents/

# Edit the plist file to update the paths
# Replace USER_NAME with your username in these paths:
# - /Users/USER_NAME/path/to/python3
# - /Users/USER_NAME/path/to/infuse_frame_switch.py
# - /Users/USER_NAME/path/to/log_file

# Load the launch agent
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.infuse.frameswitch.plist
```

## Usage

The script will start automatically when you log in and run in the background. It will:
- Switch to 24Hz when Infuse is running
- Switch back to your original refresh rate when Infuse is closed

To check if it's working:
1. Open Infuse
2. Check your display's refresh rate (System Settings > Displays)
3. Close Infuse
4. The refresh rate should switch back automatically

## Troubleshooting

Check the log file for any errors:
```bash
cat ~/path/to/infuse_frame_switch.log
```

To stop the auto-start:
```bash
launchctl bootout gui/$UID ~/Library/LaunchAgents/com.infuse.frameswitch.plist
```

## Customization

- To change the target refresh rate, edit the `switch_refresh_rate(24)` call in the script
- To change the polling rate, edit the `time.sleep(0.01)` value
- To modify the resolution, edit the resolution parameter in the `switch_refresh_rate()` function

## Contributing

Feel free to open issues or submit pull requests if you have any improvements or bug fixes.

## License

MIT License - feel free to modify and share! 
