'''Bresenham algorithm'''
def bresenham(x_0: int, y_0: int, x_1: int, y_1: int) -> list[tuple[int, int]]:
    """
    Returns a list of coordinates
    representing a line from (x1, y1) to (x2, y2)
    Source: https://github.com/encukou/bresenham

    Copyright © 2016 Petr Viktorin

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    """
    coordinates = []
    d_x = x_1 - x_0
    d_y = y_1 - y_0

    x_sign = 1 if d_x > 0 else -1
    y_sign = 1 if d_y > 0 else -1

    d_x = abs(d_x)
    d_y = abs(d_y)

    if d_x > d_y:
        x_x, x_y, y_x, y_y = x_sign, 0, 0, y_sign
    else:
        d_x, d_y = d_y, d_x
        x_x, x_y, y_x, y_y = 0, y_sign, x_sign, 0

    d_val = 2*d_y - d_x
    y_val = 0

    for x_val in range(d_x + 1):
        coordinates.append((x_0 + x_val*x_x + y_val*y_x,
                           y_0 + x_val*x_y + y_val*y_y))
        if d_val >= 0:
            y_val += 1
            d_val -= 2*d_x
        d_val += 2*d_y

    return coordinates
    