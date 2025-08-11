# What Is Bro Doing

A Discord Rich Presence tool that displays your currently active application.

## Features

- Real-time display of current active application
- Customizable display text
- Application name mapping support
- Dynamic application list editing

## Requirements

- Python 3.12+
- Discord desktop client
- Required Python packages:
  - pypresence
  - pygetwindow
  - psutil
  - pywin32

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ian-bug/WhatIsBroDoing.git
cd WhatIsBroDoing
```

2. Install required packages:
```bash
pip install pypresence pygetwindow psutil pywin32
```

## Usage

1. Run the program:
```bash
python main.py
```

2. Choose mode:
   - Enter `0` to start monitoring
   - Enter `1` to edit application list

3. If starting monitor mode:
   - Enter custom details text (or press Enter for default "bro is doing")
   - The program will start displaying your active applications in Discord

4. If editing application list:
   - Enter process name (e.g., "chrome.exe")
   - Enter display name (e.g., "Google Chrome")
   - The program will update the application list accordingly

## Configuration

You can customize application display names in `applist.py`. The format is:
```python
app_names = {
    "process_name.exe": "Display Name"
}
```

## Contributing

Feel free to open issues or submit pull requests if you have any improvements or suggestions.