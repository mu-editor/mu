"""
Contains definitions for the Pygame Zero related APIs so they can be
used in the editor for autocomplete and call tips.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


PYGAMEZERO_APIS = [
    _(
        "actor.Actor(image, pos=None, anchor=None, **kwargs) \nRect(left, top, width, height) -> Rect\nRect((left, top), (width, height)) -> Rect\nRect(object) -> Rect\nPygame Zero object for storing rectangular coordinates"
    ),
    _(
        "actor.atan2() \natan2(y, x)\n\nReturn the arc tangent (measured in radians) of y/x.\nUnlike atan(y/x), the signs of both x and y are considered."
    ),
    _("actor.cos() \ncos(x)\n\nReturn the cosine of x (measured in radians)."),
    _(
        "actor.degrees() \ndegrees(x)\n\nConvert angle x from radians to degrees."
    ),
    _(
        "actor.pygame() \nPygame Zero is a set of Python modules designed for writing games.\nIt is written on top of the excellent SDL library. This allows you\nto create fully featured games and multimedia programs in the python\nlanguage. The package is highly portable, with games running on\nWindows, MacOS, OS X, BeOS, FreeBSD, IRIX, and Linux."
    ),
    _(
        "actor.radians() \nradians(x)\n\nConvert angle x from degrees to radians."
    ),
    _("actor.sin() \nsin(x)\n\nReturn the sine of x (measured in radians)."),
    _("actor.sqrt() \nsqrt(x)\n\nReturn the square root of x."),
    _(
        "actor.transform_anchor(ax, ay, w, h, angle) \nTransform anchor based upon a rotation of a surface of size w x h."
    ),
    _(
        'animation.Animation(object, tween=\'linear\', duration=1, on_finished=None, **targets) \nAn animation manager for object attribute animations.\n\nEach keyword argument given to the Animation on creation (except\n"type" and "duration") will be *tweened* from their current value\non the object to the target value specified.\n\nIf the value is a list or tuple, then each value inside that will\nbe tweened.\n\nThe update() method is automatically scheduled with the clock for\nthe duration of the animation.'
    ),
    _(
        "animation.each_tick(callback) \nSchedule a callback to be called every tick.\n\nUnlike the standard scheduler functions, the callable is passed the\nelapsed clock time since the last call (the same value passed to tick)."
    ),
    _("animation.pow() \npow(x, y)\n\nReturn x**y (x to the power of y)."),
    _(
        "animation.sin() \nsin(x)\n\nReturn the sine of x (measured in radians)."
    ),
    _(
        "animation.unschedule(callback) \nUnschedule the given callback.\n\nIf scheduled multiple times all instances will be unscheduled."
    ),
    _(
        "clock.Clock() \nA clock used for event scheduling.\n\nWhen tick() is called, all events scheduled for before now will be called\nin order.\n\ntick() would typically be called from the game loop for the default clock.\n\nAdditional clocks could be created - for example, a game clock that could\nbe suspended in pause screens. Your code must take care of calling tick()\nor not. You could also run the clock at a different rate if desired, by\nscaling dt before passing it to tick()."
    ),
    _(
        "clock.Event(time, cb, repeat=None) \nAn event scheduled for a future time.\n\nEvents are ordered by their scheduled execution time."
    ),
    _(
        "clock.each_tick(callback) \nSchedule a callback to be called every tick.\n\nUnlike the standard scheduler functions, the callable is passed the\nelapsed clock time since the last call (the same value passed to tick)."
    ),
    _(
        "clock.heapq() \nHeap queue algorithm (a.k.a. priority queue).\n\nHeaps are arrays for which a[k] <= a[2*k+1] and a[k] <= a[2*k+2] for\nall k, counting elements from 0.  For the sake of comparison,\nnon-existing elements are considered to be infinite.  The interesting\nproperty of a heap is that a[0] is always its smallest element.\n\nUsage:\n\nheap = []            # creates an empty heap\nheappush(heap, item) # pushes a new item on the heap\nitem = heappop(heap) # pops the smallest item from the heap\nitem = heap[0]       # smallest item on the heap without popping it\nheapify(x)           # transforms list into a heap, in-place, in linear time\nitem = heapreplace(heap, item) # pops and returns smallest item, and adds\n                               # new item; the heap size is unchanged\n\nOur API differs from textbook heap algorithms as follows:\n\n- We use 0-based indexing.  This makes the relationship between the\n  index for a node and the indexes for its children slightly less\n  obvious, but is more suitable since Python uses 0-based indexing.\n\n- Our heappop() method returns the smallest item, not the largest.\n\nThese two make it possible to view the heap as a regular Python list\nwithout surprises: heap[0] is the smallest item, and heap.sort()\nmaintains the heap invariant!"
    ),
    _(
        "clock.method() \nmethod(function, instance)\n\nCreate a bound instance method object."
    ),
    _(
        "clock.schedule(callback, delay) \nSchedule callback to be called once, at `delay` seconds from now.\n\n:param callback: A parameterless callable to be called.\n:param delay: The delay before the call (in clock time / seconds)."
    ),
    _(
        "clock.schedule_interval(callback, delay) \nSchedule callback to be called every `delay` seconds.\n\nThe first occurrence will be after `delay` seconds.\n\n:param callback: A parameterless callable to be called.\n:param delay: The interval in seconds."
    ),
    _(
        "clock.schedule_unique(callback, delay) \nSchedule callback to be called once, at `delay` seconds from now.\n\nIf it was already scheduled, postpone its firing.\n\n:param callback: A parameterless callable to be called.\n:param delay: The delay before the call (in clock time / seconds)."
    ),
    _(
        "clock.tick(dt) \nUpdate the clock time and fire all scheduled events.\n\n:param dt: The elapsed time in seconds."
    ),
    _(
        "clock.total_ordering(cls) \nClass decorator that fills in missing ordering methods"
    ),
    _(
        "clock.unschedule(callback) \nUnschedule the given callback.\n\nIf scheduled multiple times all instances will be unscheduled."
    ),
    _(
        "clock.weak_method(method) \nQuick weak method ref in case users aren't using Python 3.4"
    ),
    _(
        "draw.circle(position, radius, (r, g, b)) \nDraw the outline of a circle."
    ),
    _(
        "draw.filled_circle(position, radius, (r, g, b)) \nDraw a filled circle."
    ),
    _(
        "draw.filled_rect(rect, (r, g, b)) \nDraw a filled rectangle. Takes a Rect object. For example, Rect((20, 20), (100, 100))"
    ),
    _("draw.line(start, end, (r, g, b)) \nDraw a line from start to end."),
    _(
        "draw.rect(rect, (r, g, b)) \nDraw the outline of a rectangle. Takes a Rect object. For example, Rect((20, 20), (100, 100))"
    ),
    _(
        "draw.text(text, [pos, ]**kwargs) \nDraw text. There’s an extremely rich API for positioning and formatting text; see Pygame Zero Text Formatting for full details."
    ),
    _(
        "draw.textbox(text, rect, **kwargs) \nDraw text, sized to fill the given Rect. There’s an extremely rich API for positioning and formatting text; see Pygame Zero Text Formatting for full details."
    ),
    _(
        "keyboard.Keyboard() \nThe current state of the keyboard.\n\nEach attribute represents a key. For example, ::\n\n    keyboard.a\n\nis True if the 'A' key is depressed, and False otherwise."
    ),
    _(
        "keyboard.keys(value, names=None, *, module=None, qualname=None, type=None, start=1) \nAn enumeration."
    ),
    _("keyboard.re() \nSupport for regular expressions (RE)."),
    _(
        "keyboard.warn() \nIssue a warning, or maybe ignore it or raise an exception."
    ),
    _(
        "music.ResourceLoader(subpath) \nAbstract resource loader.\n\nA resource loader is a singleton; resources are loaded from a named\nsubdirectory of the global 'root'. The `.load()` method actually loads\na resource.\n\nAdditionally, attribute access can be used to access and cache resources.\nDotted paths can be used to traverse directories."
    ),
    _(
        "music.fadeout(seconds) \nFade out and eventually stop the music playback.\n\n:param seconds: The duration in seconds over which the sound will be faded\n                out. For example, to fade out over half a second, call\n                ``music.fadeout(0.5)``."
    ),
    _("music.get_pos() \nget_pos() -> time\nget the music play time"),
    _("music.get_volume() \nget_volume() -> value\nget the music volume"),
    _(
        "music.is_playing(name) \nReturn True if the music is playing and not paused."
    ),
    _(
        "music.pause() \nTemporarily stop playback of the music stream.\n\nCall `unpause()` to resume."
    ),
    _(
        "music.pgzero.constants() \nNames for constants returned by Pygame Zero."
    ),
    _(
        "music.play(name) \nPlay a music file from the music/ directory.\n\nThe music will loop when it finishes playing."
    ),
    _("music.play_once(name) \nPlay a music file from the music/ directory."),
    _(
        "music.queue(name) \nQueue a music file to follow the current track.\n\nThis will load a music file and queue it. A queued music file will begin as\nsoon as the current music naturally ends. If the current music is ever\nstopped or changed, the queued song will be lost."
    ),
    _("music.rewind() \nrewind() -> None\nrestart music"),
    _("music.set_pos() \nset_pos(pos) -> None\nset position to play from"),
    _("music.set_volume() \nset_volume(value) -> None\nset the music volume"),
    _("music.stop() \nstop() -> None\nstop the music playback"),
    _(
        "music.unpause() \nResume playback of the music stream after it has been paused."
    ),
    _(
        "screen.blit(image, (left, top)) \nDraw the image to the screen at the given position. \nblit() accepts either a Surface or a string as its image parameter. If image is a str then the named image will be loaded from the images/ directory."
    ),
    _("screen.clear() \nReset the screen to black."),
    _("screen.fill((red, green, blue)) \nFill the screen with a solid color."),
    _("screen.Screen(surface) \nInterface to the screen."),
    _(
        "screen.SurfacePainter(screen) \nInterface to pygame.draw that is bound to a surface."
    ),
    _(
        "screen.pgzero.ptext() \npygame-text - high-level text rendering with Pygame Zero.\n\nThis module is directly copied from\n\n    https://github.com/cosmologicon/pygame-text\n\nat revision c04e59b7382a832e117f0598cdcbc1bb3eb26db5\nand used under CC0."
    ),
    _(
        "screen.pygame() \nPygame Zero is a set of Python modules designed for writing games.\nIt is written on top of the excellent SDL library. This allows you\nto create fully featured games and multimedia programs in the python\nlanguage. The package is highly portable, with games running on\nWindows, MacOS, OS X, BeOS, FreeBSD, IRIX, and Linux."
    ),
    _(
        "screen.round_pos(pos) \nRound a tuple position so it can be used for drawing."
    ),
]
