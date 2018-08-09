## What is this?
A little script in Python to generate fractal graphs similar to the Sierpinski carpet and Menger Sponge. The fractals are defined as subgraphs of `Z^d` induced by
```
{(x_1, ..., x_d): for all j |{x_i: x_i,j in A}| <= m}
```
where `x_i,j` are digits of `x_i` in base `b`. In other words, all points with at most `m` coordinates having a base `b` digit contained in `A` at any given position. The Sieprinski carpet is given by `d=2`, `b=3`, `m=1`, `A={1}` and the Menger Sponge is the same but with `d=3`.

Since it is impossible to draw infinitely many points on the screen, there is a parameter `k` specifying which iteration you want, and what it essentially does is limits the number of digits in each coordinate to `k`. Needless to say, large `k` (and 4 already is large enough) take a long time to compute and render, especially for large bases and dimensions, - I hope to improve the efficiency in the future.

All parameters have to be set at the top of the script for now. 
Also, the 3D fractals rotate (uncontrollably, for the time being).

## Setup
This script uses PyOpenGL which needs to be installed separately. This can be done via `pip`:
```
pip install PyOpenGL PyOpenGL_accelerate
```
Once you have it, simply run it with `python <path_to_script>/sierpinski.py`

#### Windows users:
Apparently, `pip` doesn't come with all the right dependencies on Windows. It is commonly suggested to download OpenGL packages from [here](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.lfd.uci.edu%2F~gohlke%2Fpythonlibs%2F%23pyopengl&h=AT3DRx9-IAKM8CQkXjTvkoZnODYOczhgQ8BE4QRRnbiVxhG_JUc6avOKWaQYowc4CLacBHKVIKs92aohczKIflbr3LkNn4Kammdxop28D_ERG1P5gmPRojggQh7ttw). The numbers in the file names correspond to your version of python (the `cpXX` part) and whether your system is 32- or 64-bit. Once you have the right file,
```
pip install package_you_downloaded.whl
```
should install it.
