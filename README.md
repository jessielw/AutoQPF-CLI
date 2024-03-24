# AutoQPF-CLI

```
usage: AutoQPF-CLI [-h] [-v] [-i INPUT [INPUT ...]] [-s] [-f FPS] [-a]
                   [-c CHAPTER_CHUNKS] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i, --input, INPUT [INPUT ...]
                        Input file paths or directories
  -s, --staxrip-batch   If used, will auto create StaxRip temp directories with proper QPF files inside.
  -f, --fps, FPS        Define source file FPS.
  -a, --auto-fps        If used, will over ride any user fps input if the input file is a media file.
  -c, --chapter-chunks, CHAPTER_CHUNKS
                        If chapters are generated, sets the percentage of total duration they will be created for.
  -o, --output, OUTPUT  The output file path. Output will be put alongside input.
```
