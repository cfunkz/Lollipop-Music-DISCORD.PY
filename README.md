# Interactive Discord.py Music Bot

This is a Python Discord bot that provides music-related commands for your server with buttons included. This bot is designed to be used with the [discord.py](https://github.com/Rapptz/discord.py), [Lavalink](https://github.com/lavalink-devs/Lavalink) backend and the [Wavelink](https://github.com/PythonistaGuild/Wavelink) library for audio streaming and processing.

# **THIS REQUIRES LAVALINK SERVER SETUP BEFOREHAND.. ITS EASY TO DO RESEARCH!**

## Features

- Play music from YouTube, Soundcloud, HTTP, Vimeo & Soon Spotify.
- Create and manage a queue of songs.
- Display the currently playing song with a progress bar.
- Control playback (skip, pause, resume, stop).
- Adjust volume.
- Shuffle the queue.
- Repeat a song or the entire queue.

## Dependencies

Before you can run the Music Bot, make sure you have the following dependencies installed:

- [Python](https://www.python.org/) (Python 3.7 or higher)
- [discord-py](https://github.com/Rapptz/discord.py)
- [Wavelink](https://github.com/PythonistaGuild/Wavelink)
- [Lavalink](https://github.com/lavalink-devs/Lavalink) server running. VPS or Home PC.

## Installation

1. Download the Music Bot source code from this repository.

2. Set up and configure the necessary dependencies and environment for the bot, such as Python and the required libraries.

3. Run the bot using the appropriate command or script to start it. Should work on replit also because I am hosting my bot on replit and it works fine.


## Usage

1. Join a voice channel: `/play <query>` - Searches YouTube for a song and plays it in the user's voice channel.
2. Display the currently playing song: `/nowplaying` - Shows the song that is currently playing with a progress bar.
3. View queue: `/queue` - View current queue.
4. Skip the current song: `/skip` - Skips the current song and plays the next one in the queue.
5. Play the previous song: `/previous` - Plays the last song in the queue history.
6. Clear the queue: `/clear` - Clears the song queue.
7. Shuffle the queue: `/shuffle` - Shuffles the order of songs in the queue.
8. Pause playback: `/pause` - Pauses the currently playing song.
9. Resume playback: `/resume` - Resumes playback if it's paused.
10. Stop playback and disconnect: `/stop` - Stops playback and disconnects the bot from the voice channel.
11. Adjust volume: `/volume <volume>` - Sets the volume of the bot (0-100%).
12. Repeat all songs in the queue: `/repeatall` - Toggles repeat mode for the entire queue.
13. Repeat the current song: `/repeat` - Toggles repeat mode for the current song.

## Credits

This bot is built using the [discord.py](https://github.com/Rapptz/discord.py), [wavelink](https://github.com/PythonistaGuild/Wavelink) and [Lavalink](https://github.com/lavalink-devs/Lavalink) libraries. Special thanks to the developers of these libraries for making it possible to create such functionality.

## License

This code is available under the Apache 2.0 License. Contact me for any details through discord/email or github.
