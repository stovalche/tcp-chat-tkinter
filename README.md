# tcp-chat-tkinter

This is a chating and file transferring application based on tcp python socket programming with tkinter gui.

## Features

- Broadcast chatting
- Private chatting
- Text file transferring

## File Management

- received file => ./received/ (auto generated directory)
- history file => ./hist/ (auto generated directory)

## Requirements

- python3
- tkinter module
  - Debian based distros:
    ```
    apt-get install python3-tk
    ```
  - Arch based distros:
    ```
    pacman -Sy tk
    ```
  - Or install it by running ./setup:
    ```
    chmod +x ./setup
    ./setup
    ```
