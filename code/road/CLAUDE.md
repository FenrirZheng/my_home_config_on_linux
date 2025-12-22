# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

百家樂大問路系統 - Baccarat road prediction system with visualization.

## Project Setup

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Development Commands

```bash
# Run application
python main.py                    # Interactive mode
python main.py "BPBPPBBB"         # With input string
python main.py --compact "BPBPPBBB"  # Compact output

# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_big_road.py::TestBigRoad::test_dragon_tail -v
```

## Architecture

```
src/
├── big_road.py        # 大路 - Main road tracking (handles dragon tail)
├── derived_roads.py   # 衍生路 - BigEyeRoad, SmallRoad, CockroachRoad
├── predictor.py       # 問路 - Prediction logic for B/P scenarios
└── display.py         # Terminal visualization using rich
```

## Key Concepts

- **B** = Banker (莊), **P** = Player (閒), **T** = Tie (和, ignored)
- **大路**: Records B/P results; same result goes down, different starts new column
- **龍尾**: When column exceeds 6 rows, extends horizontally at row 6
- **衍生路**: Derived from 大路 comparing column lengths
  - 大眼仔: compare_distance=1, starts col 1
  - 小路: compare_distance=2, starts col 2
  - 曱甴路: compare_distance=3, starts col 3
- **問路**: Predicts what color each derived road would show if B or P wins next
