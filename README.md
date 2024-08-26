# Torless Tails Terminal

[Tails](https://tails.net/) is a live boot operating system that you run from a USB stick or DVD. It is built for maximum privacy. Part of its appeal is the fact that all Internet traffic runs through the [Tor network](https://www.torproject.org/).

This program allows you to start a Bash shell in Tails whose traffic does **not** go through Tor. This allows you to execute programs or run scripts that use the Internet without going over Tor. This is a huge privacy risk. Your real IP address is exposed to any online services used in that terminal. **Use at your own risk!**

This "Torless" feature is contained to the Bash shell it spawns. The rest of the OS and other terminals will all still strictly go through Tor.



## How to use
It is assumed you are running Tails. Running this program requires an administrator password. Be sure to set one up at the Welcome Screen you get when starting up Tails.

1. [Download this repository](https://github.com/TheGeorgeAlexander/torless-tails-terminal/archive/refs/heads/main.zip).
2. Run `chmod +x torless-tails-terminal.sh` once to make it executable.
3. Right-click on `torless-tails-terminal.sh` and click `Run as a Program`.
4. To close the terminal, execute `exit` or close the window


---

![GIF showing how it is used](https://github.com/user-attachments/assets/a1bc3856-1667-411c-9454-bf2bef498a5b)

---


*How many t's can you find in the following text?*
> Technically, Tails tries to take total traffic through Tor. Though this tool takes terminal traffic through Torless trenches. Terrific!
