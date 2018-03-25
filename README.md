# ToxPhone-UI

## Simple and small UI for the ToxPhone

See [here](https://hackaday.io/project/9046-toxphone) for more details about the whole project (2 years old!)

__Warning ! Those instructions have been recently tested on a 64 bits laptop, not on a Raspberry Pi. Since the software used are 2 years old, there is no guarantee that it can be installed the same way on a Raspberry Pi.__

### Features

* Connection indicator
* Status indicator
* Friend's status
* Friend's status message
* Friend's "last seen"
* TCP/UDP switch
* IPv6 switch
* Clock indicator
* Audio calls

### Requirements

This code was written in 2016. Since then, the dependencies have changed so to make it work, you'll have to compile old softwares.

Dependencies:

* python3
* pygame (for python3)
* pyaudio (for python3)
* PyTox (specifically the commit 9c31ee5879775ef3352dd21b58ddb1fb0edc44b1)
* toxcore (specifically the commit 0938ba08d9a839df4111168f3414099268d69737)

#### toxcore

For Arch Linux users, it is possible to compile the package from [community] like any package from the AUR:

```bash
wget https://git.archlinux.org/svntogit/community.git/snapshot/community-c1dbb181bd9fe2551276d6c7bc8599ed1e08bd78.tar.gz
tar -xzvf community-c1dbb181bd9fe2551276d6c7bc8599ed1e08bd78.tar.gz
cd community-c1dbb181bd9fe2551276d6c7bc8599ed1e08bd78
makepkg
pacman -U toxcore-3697-1-x86_64.pkg.tar.xz
```

For other users, you should clone the specific commit and have a look at the README:

```bash
git clone https://github.com/irungentoo/toxcore.git
cd toxcore
git checkout 0938ba08d9a839df4111168f3414099268d69737
cat README.md
```

#### PyTox

Once toxcore is compiled and installed, you can clone PyTox and install it:

```bash
https://github.com/aitjcize/PyTox.git
cd PyTox
git checkout 9c31ee5879775ef3352dd21b58ddb1fb0edc44b1
python3 setup.py install
```

Or to install it only for the local user:

```bash
python3 setup.py install --user
```

#### ToxPhone-UI

After installing everything, you can clone this repository and go to the "Starting" section :

```bash
git clone https://github.com/rodolpheh/toxphone-ui.git
```

### Starting

For now, the program can't create a tox profile. The workaround is to use any tox client to create one, invite a few friends, quit the client and copy the profile's file in the local folder and rename it as `echo.data`.

After this, you can start using `python3 main.py`

Navigating through the UI is achieved with the following keys:

* NUMPAD_8 : down
* NUMPAD_2 : up
* NUMPAD_5 : enter
* r : return


