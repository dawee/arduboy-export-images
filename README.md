# arduboy-export-images

Export images to arduboy sources

## Install

```
$ pip install -r requirements.txt
```

## Usage

```
$ python export-image.py nyan.png
```

You'll get **nyan.cpp** and **nyan.h** with the function **draw_nyan(arduboy, x, y)** (x and y are the coordinates to draw and arduboy, the Arduboy instance).
