# PyOctoscraper
A Python based scraper to download Python source code from Github and train an RNN to generate source code. I have no hopes that the code generated will be useful, or even valid, but it's a fun experiment nonetheless.

## Scraper

I could not find any dataset of source code, so I scraped it myself. The [scraper.py](scraper.py) does the magic. To keep things sane, we're only interested in `keras` code written in `python` that have more than 500 stars. The rationale being that well written code is more likely to be written correctly (not exactly proof, but a close enough approximation).

## Generation

A super big shoutout to [Max Woolf](http://minimaxir.com/) for creating the [textgenrnn](https://github.com/minimaxir/textgenrnn) package. It made my life considerably easier and I highly recommend it for quick and dirty projects.

## Samples