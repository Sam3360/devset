# devset

A Swiss-army-knife CLI with the everyday tools every dev needs — plus a
one-command bootstrapper that spins up a virtualenv with a curated set of
Python packages already installed.

## Install

```bash
git clone <this repo>
cd devset
pip install -e .
```

This registers the `devset` command on your PATH, and also pulls in a
small set of core dependencies every dev tends to reach for — `requests`,
`python-dotenv`, `rich` — so they're available immediately, both for
`devset`'s own commands (like `net get`) and for you to `import` in your
own scripts once devset is on your PATH/venv.

Want more? Install extras for heavier, more specific toolsets:

```bash
pip install -e ".[dev]"    # pytest, black, ruff, mypy, ipython
pip install -e ".[web]"    # fastapi, uvicorn, httpx, pydantic
pip install -e ".[data]"   # numpy, pandas, matplotlib, jupyter, openpyxl
pip install -e ".[all]"    # everything above
```

## The headline feature: `devset setup`

Get a fully wired-up Python environment in one command:

```bash
devset setup init                       # essentials profile -> .venv/
devset setup init --profile web         # fastapi, httpx, pydantic, ...
devset setup init --profile data        # numpy, pandas, matplotlib, jupyter
devset setup init --profile testing     # pytest, mypy, black, ruff
devset setup init -p web -e sqlalchemy  # add extra package(s) on top
devset setup profiles                   # see what's in each profile
```

This creates a `.venv`, installs the chosen package set, and writes a
`requirements.txt` you can commit.

## Everything else

| Group   | Example                                      |
|---------|-----------------------------------------------|
| `json`  | `devset json pretty file.json --sort-keys`     |
| `b64`   | `devset b64 encode "hello"`                    |
| `hash`  | `devset hash sha256 "text"` / `hash all`       |
| `uuid`  | `devset uuid gen -n 5`                         |
| `git`   | `devset git summary` / `git clean-branches`    |
| `text`  | `devset text slug "My Title"` / `text case`    |
| `time`  | `devset time now` / `time from-unix 170...`    |
| `gen`   | `devset gen password -l 24` / `gen lorem`      |
| `net`   | `devset net port host 443` / `net get <url>`   |
| `color` | `devset color hex2rgb "#ff8800"`               |
| `fs`    | `devset fs tree --depth 2`                     |

Run `devset --help` or `devset COMMAND --help` for full details.

## Extending it

Each command group lives in its own file under `devset/commands/` as a
`click.Group`. To add a new one: create `devset/commands/my_tools.py` with a
`@click.group()`, then register it in `devset/cli.py`.
