A waybar custom module for showing current internet speed, inspired by [this issue](https://github.com/Alexays/Waybar/issues/2162)

![image](https://github.com/user-attachments/assets/bbcd94b3-e41b-4292-8ebd-48fa5b1a9a83)

Blue for download speed, red for upload.

# Usage:
1. Download the file `bandwidth.py`
2. Add it to the config file:
```json
    "modules-right": [
        "custom/bandwidth",
    ],
    "custom/bandwidth": {
        "exec": "$HOME/.config/waybar/bandwidth.py"
    },
```
