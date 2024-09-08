# DVD Encoder CLI

## Overview

**DVD Encoder CLI** is a Python-based command-line tool that helps you scan and encode DVD titles using [HandBrakeCLI](https://handbrake.fr/). This project is bundled with `HandBrakeCLI.exe` making it easy to distribute and run on different machines.

The program allows users to:
- Scan DVDs and list available titles with their durations.
- Select specific titles to encode.
- Store the DVD drive letter and target directory for reuse during a session.
- Rescan the DVD to display titles if the user wants to encode another title from the same DVD.
- Optimized encoding settings for the best DVD rip quality.

## Features

- **Title Scanning**: Automatically scan DVDs and display a list of titles and their durations.
- **Encoding**: Select and encode specific titles using `HandBrakeCLI`.
- **Session Reuse**: Optionally store the DVD drive letter and target directory for reuse during a session.
- **Rescan Feature**: Rescan DVDs if the user wants to encode additional titles.
- **Optimized Encoding Settings**: Pre-configured settings for the best DVD rip quality.

## Optimized Encoding Settings

The encoding settings used by **DVD Encoder CLI** have been optimized to provide the best possible quality for ripping DVDs. These settings ensure that the output file retains high video quality while maintaining a reasonable file size. Here are the key settings that are pre-configured:

- **Video Codec**: H.264 (x264), one of the most efficient and widely supported video codecs.
- **Resolution**: 720x576 (PAL DVD standard).
- **Frame Rate**: 25 FPS (frames per second), ensuring smooth playback.
- **Decomb Filter**: Used to remove interlacing artifacts from the DVD.
- **Audio Track**: The main audio track is passed through without re-encoding to preserve its original quality.
- **Preset**: Optimized for speed and quality using the "veryfast" encoder preset.
- **Output Format**: MP4 (MPEG-4 Part 14), which is a widely supported and efficient format for storing video.
  
These settings have been designed for DVD rips, ensuring high-quality output with minimal loss in quality and optimized file sizes for archiving or playback.

## Requirements

- Python 3.x
- [HandBrakeCLI](https://handbrake.fr/downloads.php) (bundled as `HandBrakeCLI.exe`)
- [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/) for bundling the script into an executable


