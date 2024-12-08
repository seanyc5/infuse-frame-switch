#!/bin/bash

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed. Please install it first:"
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
fi

# Install displayplacer
echo "Installing displayplacer..."
brew install jakehilborn/jakehilborn/displayplacer

# Get display ID
echo "Getting display information..."
displayplacer list
echo
echo "Please enter your display ID from the above output (e.g., 012A6609-58A0-45FF-8F55-8538870D40BB):"
read display_id

# Update the script with the display ID
echo "Updating script with display ID..."
sed -i '' "s/012A6609-58A0-45FF-8F55-8538870D40BB/$display_id/" infuse_frame_switch.py

# Make script executable
chmod +x infuse_frame_switch.py

# Get Python path
python_path=$(which python3)
echo "Found Python at: $python_path"

# Update plist file with correct paths
echo "Updating launch agent configuration..."
sed -i '' "s|/Library/Frameworks/Python.framework/Versions/3.11/bin/python3|$python_path|" com.infuse.frameswitch.plist
sed -i '' "s|/Users/sean/Developer/Infuse Frame Switch|$PWD|g" com.infuse.frameswitch.plist

# Create LaunchAgents directory and copy plist
echo "Setting up auto-start..."
mkdir -p ~/Library/LaunchAgents
cp com.infuse.frameswitch.plist ~/Library/LaunchAgents/

# Load the launch agent
echo "Loading launch agent..."
launchctl bootout gui/$UID ~/Library/LaunchAgents/com.infuse.frameswitch.plist 2>/dev/null || true
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.infuse.frameswitch.plist

echo
echo "Installation complete! The script will now:"
echo "1. Start automatically when you log in"
echo "2. Switch to 24Hz when Infuse is running"
echo "3. Switch back to your original refresh rate when Infuse is closed"
echo
echo "To test it, try opening and closing Infuse."
echo "Check the log file at: $PWD/infuse_frame_switch.log" 