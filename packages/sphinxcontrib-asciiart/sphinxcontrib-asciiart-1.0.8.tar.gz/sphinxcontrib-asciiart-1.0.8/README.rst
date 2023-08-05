#######################
sphinxcontrib-asciiart
#######################

http://packages.python.org/sphinxcontrib-asciiart

A Sphinx_ extension, which turns ascii art color sequences in Sphinx documents
into colored HTML or .png or other output.

.. _`Sphinx`: http://sphinx.pocoo.org/latest

Installation
============

This extension can be installed from the Python Package Index::

   pip install sphinxcontrib-asciiart

Usage
=====

Just add ``sphinxcontrib.asciiart`` to the list of extensions in the
``conf.py`` file. For example::

    extensions = ['sphinxcontrib.asciiart']

And then use the asciiart block to include your ascii art code::

    .. asciiart::

        [31m                                              :. ,..[0m
        [31m                                            .' :~.':_.,[0m
        [31m                                          .'   ::.::'.'[0m
        [31m                                         :     ::'  .:[0m
        [31m                                       `.:    .:  .:/[0m
        [31m                                        `::--.:'.::'[0m
        [31m                                          |. _:===-'[0m
        [32m                                        / /[0m
        [32m                       ,---.---.    __,','[0m
        [32m                      (~`.  \   )   )','.,---..[0m
        [32m                       `v`\ | ,' .-'.:,'_____   `.[0m
        [32m                           )|/.-~.--~~--.   ~~~-. \[0m
        [32m                         _/-'_.-~        ""---.._`.|[0m
        [32m                    _.-~~_.-~                    ""'[0m
        [32m             _..--~~_.(~~[0m
        [32m  __...---~~~_..--~~[0m
        [32m'___...---~~~[0m


Then it would be rendered as a colorful literal block or image. To show the
content of the pypi webpage, I remove the colors::

                                                  :. ,..
                                                .' :~.':_.,
                                              .'   ::.::'.'
                                             :     ::'  .:
                                           `.:    .:  .:/
                                            `::--.:'.::'
                                              |. _:===-'
                                             / /
                            ,---.---.    __,','
                           (~`.  \   )   )','.,---..
                            `v`\ | ,' .-'.:,'_____   `.
                                )|/.-~.--~~--.   ~~~-. \
                              _/-'_.-~        ""---.._`.|
                         _.-~~_.-~                    ""'
                  _..--~~_.(~~
       __...---~~~_..--~~
    ,'___...---~~~

Options
=======

sphinxcontrib-asciiart provide rich options to custimize the output. You can
configure the global setting, you also can change the behavior for only one
ascii art literal block.

When the global setting and literal block based setting are change, or if the
content of the literal block is changed, it would re-build the target image
even there is target image cache already.

global setting
--------------

First of all, you should configure the sphinxcontrib-asciiart in the conf.py
to enable the sphinxcontrib-asciiart::

    extensions = ['sphinxcontrib-asciiart']

Then you can configure many other global configuration:

ascii_art_output_format
+++++++++++++++++++++++

ascii_art_output_format give the output format of the ascii art block. We use
the suffix to control the build output foramt. The default value is as below
and you can change it in your conf.py in the following format::

    ascii_art_output_format = dict(html='.html', latex='.png', text='.txt')

That means when you build html output, the ascii art block is built as html
file and then linked to the whole document. When you build latex output,
it's .png file and .txt when building plain text output. the .html format is
only supported when you building html output.

Besides tht .html and .txt format, we support many other kinds of output
format::

    bmp
    dib
    eps
    gif
    icns
    ico
    im
    jpg
    jpeg
    msp
    pcx
    png
    ppm
    sgi
    spider
    tga
    tiff
    webp
    xbm
    palm
    pdf
    xv
    bufr
    fits
    grib
    hdf5
    mpeg

ascii_art_image_font
+++++++++++++++++++++++

When we render the image instead of ".html" and ".txt", which font name we
use, It's a list of font name that we want to use to render the ascii art. The
front one have high priority to be used. the default is::

    ascii_art_image_font = 'NSimSun, simsun, monospace'

ascii_art_image_fontsize
+++++++++++++++++++++++++

When we render the image instead of ".html" and ".txt", the font size we want
to use, it's an integer, the default value is::

    ascii_art_image_fontsize = 14

block specific setting
----------------------

* 'spacing': int, The space between each lines. The default value is -1.
* 'font': str, A list of font name that we want to use to render the ascii art. The front one have high priority to be used.
* 'fontsize': int, The font size we want to use to render the ascii art.

For example::

    .. asciiart::
        :font: simsun, monospace, "Times new roman"
        :fontsize: 14
        :spacing: 0

        .· .·.   [1;35m/╲     /|[0m
                ·[1;35m│  \  ╱ |[0m
           [1;35m\-.___ / \  \/ / /[0m
            [1;35m\ __ ╲  [1;33m.,.[1;35m| ╱__[0m
            [1;35m╱  乁  [1;33m'\|)[1;35m╱￣  ╲[0m
        [1;35m-＜`︶╲__╱ [1;33m︶[1;35m╲    ╲ \[0m
            [35m￣￣ /   /  ╱﹀乀 \│[0m
                 [1;35m╲  ' /[1;30m╲  ·╲/[0m
                   [1;35m\| /   [1;30m\  ; ｀[0m
                    [1;35m\/     [1;30m\  ·,[0m
        .----/[1;35m      ′      [1;30m︳  ·__,[0m


Changelog
============

1.0.0 Initial upload.

1.0.1 Automatically add the img["height"] to keep the original height x width to avoid to magnify in pdf if there is no height, width and scale option in the image attribute. We'd want to show the original font in the PDF.

1.0.2 Adjust the box-shadow of the html output.

1.0.3 bug fix: if there is already .png, didn't insert the img["height"].

1.0.4 bug fix: 1) Wrongly configured suffix might cause crash. 2) there is
parse error in occasionaly cases.

1.0.5 Minor typo error fix.

1.0.6 Enhance the target image algrithm, Only when the global setting and
literal block based setting are change, or when the content of the literal
block is changed, it would re-build the target image even there is target
image cache already.

1.0.7 Bug fix: bg_magenta might fail to be parsed.
1.0.8 text output won't include the options.
