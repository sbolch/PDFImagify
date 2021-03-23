# PDFImagify

## Server mode

Run

```console
> python app.py
```
or use Gunicorn ([eg. deploy on Heroku](https://devcenter.heroku.com/articles/python-gunicorn))

## Standalone mode

Call

```console
> run.py --input=/path/to/pdf
```

### Available arguments

- --input: input file or directory (required)
- --output: output directory
- --format: output format
- --lossless (-l): lossless conversion
- --prefix: prefix for output file(s)
- --singlepage (-s): get only the first page from input file(s)
- --width: output file's width
