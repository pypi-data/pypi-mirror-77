# get-stick-bugged-lol
A Python module and command-line tool that generates a 
[Get Stick Bugged Lol](https://knowyourmeme.com/memes/get-stick-bugged-lol) video from any image.

![Example](examples/python.gif)

[Example video with sound](https://github.com/n0spaces/get-stick-bugged-lol/raw/master/examples/python.mp4)

This script uses [pylsd-nova](https://github.com/AndranikSargsyan/pylsd-nova) to detect line segments in the image,
Pillow to draw the lines as they move to form the stick bug, and MoviePy to create the video.

## Installation
**NOTE: This package requires a 64-bit installation of Python 3. pylsd-nova does not work on 32-bit.**

This package can be installed using pip:
```
pip install get-stick-bugged-lol
```

## Usage
#### In the terminal
Installing the package will register the `gsbl` command in the terminal (or you can use `python -m gsbl`). To use the
image `input.png` to generate the video `output.mp4`:
```
gsbl input.png output.mp4
```
Optional arguments:
* `-h, --help` Display the help message and exit
* `--line-color R G B` RGB color to use for line segments (default: 255 255 211)
* `--bg-color R G B` RGB color to use for background after image disappears (default: 125 115 119)

More options will be added in later releases.

#### In a Python script

```python
import gsbl

# generate the video from input.png
video = gsbl.generate_stick_bug('input.png')

# save the video as output.mp4
gsbl.save_video(video, 'output.mp4')
```

## TODO
* Rewrite to be more object-oriented and easier to maintain
* Add more customization options, especially with the line detection and video resolution
* Make a GUI

## License
This package is available under the MIT License. See [LICENSE](LICENSE) for more info.

This package makes use of the following external libraries:
* [pylsd-nova](https://github.com/AndranikSargsyan/pylsd-nova)
* [NumPy](https://numpy.org)
* [Pillow](https://python-pillow.org)
* [MoviePy](https://github.com/Zulko/moviepy)
