# Torless Tails Terminal

[Tails](https://tails.net/) is a live boot operating system that you run from a USB stick or DVD. It is built for maximum privacy. Part of its appeal is the fact that all Internet traffic runs through the [Tor network](https://www.torproject.org/).

This program allows you to start a Bash shell in Tails whose traffic does **not** go through Tor. This allows you to execute programs or run scripts that use the Internet without going over Tor. This is a huge privacy risk. Your real IP address is exposed to any online services used in that terminal. **Use at your own risk!**

This "Torless" feature is contained to the Bash shell it spawns. The rest of the OS and other terminals will all still strictly go through Tor.



## How to use
It is assumed you are running Tails. Running this program requires an administrator password. Be sure to set one up at the Welcome Screen you get when starting up Tails.

You only have to do the setup once when you first download the files.

### Setup
1. Download this repository, you can do this with `git clone` or on GitHub by clicking `Code > Download ZIP`.

2. Open a terminal and navigate into the folder that contains the files of this repository.

3. Give the script permission to run by executing `chmod +x torless-tails-terminal.sh` in the terminal.

### Running
1. Start the Torless Tails Terminal by executing `./torless-tails-terminal.sh`.

2. To close the terminal, execute `exit`.


---

*See how Torless Tails Terminal is used after setup*

![GIF showing usage in terminal](https://github.com/user-attachments/assets/84f1d200-3928-4d1f-9834-5e757b0b5971)

---


*How many t's can you find in the following text?*
> Technically, Tails tries to take total traffic through Tor. Though this tool takes terminal traffic through Torless trenches. Terrific!
