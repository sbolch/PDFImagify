# PDFImagify

> A simple PDF to image converter

## Requirements

You can install these with pip

- Flask == 1.1.2
- pdf2image == 1.14.0

## Usage

### Standalone mode

Call `run.py --input=path/to/pdf` in your console

#### Available arguments

- --input: input file or directory (required)
- --output: output directory
- --format: output format
- --lossless (-l): lossless conversion
- --prefix: prefix for output file(s)
- --singlepage (-s): get only the first page from input file(s)
- --width: output file's width

### Server mode

Run `python app.py` in your console or use Gunicorn ([eg. deploy on Heroku](https://devcenter.heroku.com/articles/python-gunicorn)), then call server URL like `http://server?pdf=url/to/pdf`
