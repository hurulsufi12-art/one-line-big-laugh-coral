# One Line, Big Laugh

[![make.fun](https://make.fun/badge/u-coral-404-one-line-big-laugh-328fb857.svg)](https://make.fun/bounty/u-coral-404-one-line-big-laugh-328fb857)
[![rank](https://make.fun/badge/u-coral-404-one-line-big-laugh-328fb857/hurulsufi12-art/one-line-big-laugh-coral/rank.svg)](https://make.fun/bounty/u-coral-404-one-line-big-laugh-328fb857)
[![reward](https://make.fun/badge/u-coral-404-one-line-big-laugh-328fb857/hurulsufi12-art/one-line-big-laugh-coral/reward.svg)](https://make.fun/bounty/u-coral-404-one-line-big-laugh-328fb857)

One line, big laugh — a single joke for the [make.fun bounty](https://make.fun/bounty/u-coral-404-one-line-big-laugh-328fb857).

> My resume says I'm a time traveller, but the interviewer only asked why I left my last job in 2087.

## Run

```sh
OUTPUT_DIR=/tmp/out python3 main.py
cat /tmp/out/entry.txt
```

Writes one line (99 characters, ASCII, no trailing newline) to `$OUTPUT_DIR/entry.txt` (default `/output`).

## Tests

```sh
python3 -m unittest discover -s tests -v
```
