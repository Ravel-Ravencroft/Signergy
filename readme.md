# Signergy

Project Signergy is the MVP of the Final Year Project conceptualised and created by Michael Nadesapillai, of the Informatics Institute of Technology (ID#: 2019121 / w1761053).

It is an OS-agnostic Sign Language Inference system designed to interface with any video conferencing platform with the aim of bridging the communication gap between the AV-Impaired and Non-Impaired with respect to Video Conferencing.

## Modes

Signergy offers two modes of functionality:

1. **Practice Mode**: Runs the Inference model with a display on-screen, and is for the user to test the model, and practice their signing
2. **Stream Mode**: Runs the Inference model and passes the results to a camera feed, and is for the user to utilise with the video-conferencing platform

In order to toggle the modes, the `stream_mode` option in the `config.json` file should be toggled between `true` and `false`.

## How to Get Started?

To begin using the project, there are two main methods:

1. Running the .exe file with the Runtime Bundle that can be downloaded from the Releases

2. Cloning the Source Code and running `main.py`


## Streaming Mode Prerequisites

To use the Stream Mode of Signage with either of the above approached, a Virtual Camera must be installed, as detailed below:

### OBS (Windows / macOS)

[OBS](https://obsproject.com/) includes a built-in virtual camera for Windows and macOS.

**NOTE**: Only OBS 28 and newer are supported.

To use the OBS virtual camera, follow these one-time setup steps:
1. [Install OBS](https://obsproject.com/download)
2. Start OBS
3. On Startup, the `Auto-Configuration Wizard` will be displayed. Select the **"I will only be using the Virtual Camera"** option, click *"Next"* (Bottom Right), and then click *"Apply Settings"*
4. Close OBS.

Once the above steps are completed, OBS will no longer need to be accessed, although it will still need to be left installed on the system.

### Unity Capture (Windows)

[Unity Capture](https://github.com/schellingb/UnityCapture) provides a virtual camera originally meant for streaming Unity games.
To use the Unity Capture virtual camera, follow the [installation instructions](https://github.com/schellingb/UnityCapture#installation) on the project site.
