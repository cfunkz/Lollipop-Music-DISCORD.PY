# Music Bot Discord Cog

This is a Python Discord bot cog that provides music-related commands for your server with buttons included. This cog is designed to be used with the [discord.py](https://github.com/Rapptz/discord.py) library and the [wavelink](https://github.com/PythonistaGuild/Wavelink) library for audio streaming.

## Features

- Play music from YouTube, Soundcloud, HTTP, Vimeo & Soon Spotify.
- Create and manage a queue of songs.
- Display the currently playing song with a progress bar.
- Control playback (skip, pause, resume, stop).
- Adjust volume.
- Shuffle the queue.
- Repeat a song or the entire queue.

## Prerequisites

Before using this cog, make sure you have the following installed:

- Python
- [discord.py](https://github.com/Rapptz/discord.py)
- [wavelink](https://github.com/PythonistaGuild/Wavelink)

## Installation

1. Download the `MusicCommands` class from this repository.
2. Add it to your Discord bot project or bot's cog folder.
3. Modify your bot's code to load this cog. You can use `bot.load_extension('cog_file_name')` to load it.

## Usage

1. Join a voice channel: `/play <query>` - Searches YouTube for a song and plays it in the user's voice channel.
2. Display the currently playing song: `/nowplaying` - Shows the song that is currently playing with a progress bar.
3. Skip the current song: `/skip` - Skips the current song and plays the next one in the queue.
4. Play the previous song: `/previous` - Plays the last song in the queue history.
5. Clear the queue: `/clear` - Clears the song queue.
6. Shuffle the queue: `/shuffle` - Shuffles the order of songs in the queue.
7. Pause playback: `/pause` - Pauses the currently playing song.
8. Resume playback: `/resume` - Resumes playback if it's paused.
9. Stop playback and disconnect: `/stop` - Stops playback and disconnects the bot from the voice channel.
10. Adjust volume: `/volume <volume>` - Sets the volume of the bot (0-100%).
11. Repeat all songs in the queue: `/repeatall` - Toggles repeat mode for the entire queue.
12. Repeat the current song: `/repeat` - Toggles repeat mode for the current song.

## Credits

This cog is built using the [discord.py](https://github.com/Rapptz/discord.py) and [wavelink](https://github.com/PythonistaGuild/Wavelink) libraries. Special thanks to the developers of these libraries for making it possible to create such functionality.

## License

This code is available under the MIT License. Feel free to use, modify, and distribute it as you see fit.
