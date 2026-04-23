# Prerequisites

## uv

Both templates use [uv](https://docs.astral.sh/uv/) for dependency management. uv can also install and manage
Python for you.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

The installer will tell you to restart your shell or `source` a file so `uv` ends up on your `PATH`. Follow it,
then verify:

```bash
uv --version
```

## Python 3.12+

Check whether you already have a suitable Python:

```bash
python3 --version
```

If you see `3.12.x` or newer, you're set. Otherwise, let uv fetch Python for you - this installs into uv's own
directory and doesn't touch any system Python:

```bash
uv python install 3.12
```

(You can skip this step - `uv sync` will auto-install a matching Python when it reads the generated project's
`pyproject.toml`. Running it now just makes the failure mode clearer if something is wrong.)

## make

`make` is used as the task runner and is usually pre-installed on Linux. Check with:

```bash
make --version
```

If it's missing on Debian/Ubuntu:

```bash
sudo apt install make
```

## git

Most Linux distros ship with git; check with:

```bash
git --version
```

If it's missing on Debian/Ubuntu:

```bash
sudo apt install git
```

Then set the name and email that will appear on every commit:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@ceh.ac.uk"
```
