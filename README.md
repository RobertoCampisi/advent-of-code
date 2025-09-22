# 🎄 Advent of Code Solutions <!-- sum of stars 1: begin -->(⭐ 146)<!-- sum of stars 1: end --> 🎄

[![Advent of Code](https://img.shields.io/badge/Advent%20of%20Code-ffff66?logo=adventofcode&logoColor=000)](<https://adventofcode.com/> "Advent of Code homepage")
[![Made with Python](https://img.shields.io/badge/Python->=3.10-blue?logo=python&logoColor=white)](<https://python.org> "Go to Python homepage")
![Last commit](https://img.shields.io/github/last-commit/Flizz95/advent-of-code "Last commit")

# advent-of-code

This repository contains my personal solutions written in python for the yearly Advent of Code coding challenges.
Currently I am working on making an command line interface (CLI) to facilitate intergration with the advent of code website and automatation, such as testing and benchmarking, for future solution. 

---
<!-- Badges of stars: start -->
[![AoC 2015](https://img.shields.io/badge/2015-⭐%2050-gray?logo=adventofcode&labelColor=8a2be2)](https://adventofcode.com/2015)
[![AoC 2016](https://img.shields.io/badge/2016-⭐%2013-gray?logo=adventofcode&labelColor=8a2be2)](https://adventofcode.com/2016)
[![AoC 2017](https://img.shields.io/badge/2017-⭐%2010-gray?logo=adventofcode&labelColor=8a2be2)](https://adventofcode.com/2017)
[![AoC 2023](https://img.shields.io/badge/2023-⭐%2026-gray?logo=adventofcode&labelColor=8a2be2)](https://adventofcode.com/2023)
[![AoC 2024](https://img.shields.io/badge/2024-⭐%2048-gray?logo=adventofcode&labelColor=8a2be2)](https://adventofcode.com/2024)  
<!-- Badges of stars: end -->
---

## CLI (Work in progress)

Since the tool is made for first personal use, it has been written to run in the same directory as the solutions.

It assumes the following file structure for any solution:
```{YEAR}/day{DAY}.py```
Where `YEAR` is four digit number for the year of the advent of code puzzles and `DAY` a two digit number for the day (example: 01,02,..,25).

The CLI can be started by executing `aoc.py` with python.

### Arguments

`{year}` - 4 digits for the year. This is an optional argument and defaults to the last Advent of code challenge, when left out.
`[day(s)]` -
`{part}` -

### Commands

`token` - Set or get the current session token for advent of code website

`scan` - Scans the directory for the assumed file structure to find existing solutions and add their entries to the savefile

`create` {year} [day(s)] - Creates an entry in the savefile for the given day(s)

`fetch` {year} [day(s)] - Fetches and stores the personal input data from advent of code for the given day(s)

`run` {year} [day(s)] {part} - Run the given solution(s) with the fetch input data and display its output

`submit` {year} [day(s)] {part} - Run the given solution(s) and automatically submits the result to advent of code

`benchmark` {year} [day(s)] {part} [n] - run the given solution [n] times and return and store the average time. 

`quit` - Closes the CLI


## 🎄 Stats

For every year, the Advent of Code calendar has `25` challenges with `2` tasks per challenge. Every task gives you a
star ⭐️ so the maximum amount of stars for a year is `50`.

<!-- Table summary of years: begin -->
| Year | Stars | Advent of Code Link |
| :--: | :---: | :--: |
| [2015](year/2015) | ⭐️50  | https://adventofcode.com/2015 |
| [2016](year/2016) | ⭐️13  | https://adventofcode.com/2016 |
| [2017](year/2017) | ⭐️10  | https://adventofcode.com/2017 |
| [2023](year/2023) | ⭐️26  | https://adventofcode.com/2023 |
| [2024](year/2024) | ⭐️48  | https://adventofcode.com/2024 |
<!-- Table summary of years: end -->
