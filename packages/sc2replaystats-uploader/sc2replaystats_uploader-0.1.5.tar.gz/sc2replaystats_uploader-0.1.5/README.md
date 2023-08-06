sc2replaystats_uploader
=======================

[![image](https://img.shields.io/pypi/v/sc2replaystats_uploader.svg)](https://pypi.python.org/pypi/sc2replaystats_uploader)
[![image](https://img.shields.io/travis/StanczakDominik/sc2replaystats_uploader.svg)](https://travis-ci.com/StanczakDominik/sc2replaystats_uploader)
[![Documentation Status](https://readthedocs.org/projects/sc2replaystats-uploader/badge/?version=latest)](https://sc2replaystats-uploader.readthedocs.io/en/latest/?badge=latest)

Script to automatically upload new StarCraft II replays appearing in a
directory to sc2replaystats.

-   Free software: MIT license
-   Documentation: <https://sc2replaystats-uploader.readthedocs.io>.

Installation
------------

Just `pip install sc2replaystats_uploader`!

Usage
-----

The parameters are documented:

```

dominik@dell ~/Code/sc2replaystats_uploader % sc2replaystats_uploader --help                                                                                                             [0]
Usage: sc2replaystats_uploader [OPTIONS]

  Console script for sc2replaystats_uploader.

Options:
  --hashkey TEXT  sc2replaystats hashkey; find it in
                  https://sc2replaystats.com/account/settings -> Login Panel
                  [required]

  --auth TEXT     sc2replaystats authorization key; find it in
                  https://sc2replaystats.com/account/settings -> API Access
                  [required]

  --path PATH     Directories in which to find replays. You can put multiple
                  such options here. If using multiple in an environment
                  variable, separate them with a colon ':'.  [required]

  --help          Show this message and exit.

```

You can either put them in as flags:


```

sc2replaystats_uploader --auth "AUTHKEYGOESHERE" --hashkey "HASHKEYGOESHERE" --path "EU_REPLAY_DIR" --path "US_REPLAY_DIR"

```

Or you can use environment variables:

```
export SC2REPLAYSTATS_AUTH="AUTHKEYGOESHERE"
export SC2REPLAYSTATS_HASHKEY="HASHKEYGOESHERE"
export SC2REPLAYSTATS_PATHS="EU_REPLAY_DIR:US_REPLAY_DIR"
sc2replaystats_uploader
```

You can exit through Control-C.

## Usage with Lutris

I launch these scripts with SC2 through Lutris. In "System options", set a path
to a pre-launch script to an executable Bash file containing the following:

```
#!/usr/bin/bash
# do other stuff, Toggl tracking, etc
export SC2REPLAYSTATS_AUTH="AUTHKEYGOESHERE"
export SC2REPLAYSTATS_HASHKEY="HASHKEYGOESHERE"
export SC2REPLAYSTATS_PATHS="EU_REPLAY_DIR:US_REPLAY_DIR"
sc2replaystats_uploader

```

Then, to shut the script down, have a post-exit script that goes

```
#!/usr/bin/bash
pkill -f sc2replaystats_uploader

```
Credits
-------

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
