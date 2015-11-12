# The BeagleBone Black Primer

Source code associated with [_The BeagleBone Black Primer_ by Brian McLaughlin](http://www.quepublishing.com/store/beaglebone-black-primer-9780789753861) and published by Que. [Available on Amazon as well](https://t.co/DiGeQwHp7s).

## Clone To Your BeagleBone Black

To clone this repository to your BeagleBone Black, if you are using a Debian Linux based operating system, you will first need to have the `git` utility installed. If you have `git` already installed you can skip ahead a bit.

_*Note:* These commands assume you are running as a `root` user. If you are not, you will need to use the `sudo` command in front of the `apt-get`._

First, make sure the packages you are using are all up to date.

```
$ apt-get update && apt-get dist-upgrade
```

Next, install the `git` softare packages.

```
$ apt-get install git
```

Now that you have `git` running on your BeagleBone Black, you can clone this repository to your device.

```
$ git clone https://github.com/SpinStabilized/bbb-primer
```

## Source Repository Information

As with anything done by humans, there are bound to be imperfections in the source code. I welcome forks or bug reports. I only ask that if you have a fix to please make sure you tell me in some capacity so that I can make the appropriate updates. Help me help the community!

_Last Updated: 12 November 2015_
