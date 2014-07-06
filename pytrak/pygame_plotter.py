import time
import threading
import numpy as np
import pygame
from expyriment.stimuli import Canvas
from expyriment.stimuli._visual import Visual
from lock_expyriment import lock_expyriment

Numpy_array_type = type(np.array([]))

def inherit_docs(cls):
    for name, func in vars(cls).items():
        if not func.__doc__:
            for parent in cls.__bases__:
                parfunc = getattr(parent, name)
                if parfunc and getattr(parfunc, '__doc__', None):
                    func.__doc__ = parfunc.__doc__
                    break
    return cls


@inherit_docs
class PGSurface(Canvas):
    """PyGame Surface: Expyriment Stimulus for direct Pygame operations and
    PixelArrays

    In contrast to other Expyriment stimuli the class does not generate temporary
    surfaces.
    """

    def __init__(self, size, position=None, colour=None):
        # TODO: defaults
        Canvas.__init__(self, size, position, colour)
        self._px_array = None

    @property
    def surface(self):
        """todo"""
        if not self.has_surface:
            ok = self._set_surface(self._get_surface())  # create surface
            if not ok:
                raise RuntimeError(Visual._compression_exception_message.format(
                    "surface"))
        return self._surface

    @property
    def pixel_array(self):
        """todo"""
        if self._px_array is None:
            self._px_array = pygame.PixelArray(self.surface)
        return self._px_array

    @pixel_array.setter
    def pixel_array(self, value):
        if self._px_array is None:
            self._px_array = pygame.PixelArray(self.surface)
        self._px_array = value

    def unlock_pixel_array(self):
        """todo"""
        self._px_array = None

    def preload(self, inhibit_ogl_compress=False):
        self.unlock_pixel_array()
        return Canvas.preload(self, inhibit_ogl_compress)

    def compress(self):
        self.unlock_pixel_array()
        return Canvas.compress(self)

    def decompress(self):
        self.unlock_pixel_array()
        return Canvas.decompress(self)

    def plot(self, stimulus):
        self.unlock_pixel_array()
        return Canvas.plot(self, stimulus)

    def clear_surface(self):
        self.unlock_pixel_array()
        return Canvas.clear_surface(self)

    def copy(self):
        self.unlock_pixel_array()
        return Canvas.copy(self)

    def unload(self, keep_surface=False):
        if not keep_surface:
            self.unlock_pixel_array()
        return Canvas.unload(self, keep_surface)

    def rotate(self, degree):
        self.unlock_pixel_array()
        return Canvas.rotate(self, degree)

    def scale(self, factors):
        self.unlock_pixel_array()
        return Canvas.scale(self, factors)

    # expyriment 0.8.0
    # def scale_to_fullscreen(self, keep_aspect_ratio=True):
    #    self.unlock_pixel_array()
    #    return Canvas.scale_to_fullscreen(self, keep_aspect_ratio)

    def flip(self, booleans):
        self.unlock_pixel_array()
        return Canvas.flip(self, booleans)

    def blur(self, level):
        self.unlock_pixel_array()
        return Canvas.blur(self, level)

    def scramble(self, grain_size):
        self.unlock_pixel_array()
        return Canvas.scramble(self, grain_size)

    def add_noise(self, grain_size, percentage, colour):
        self.unlock_pixel_array()
        return Canvas.add_noise(self, grain_size, percentage, colour)


class Plotter(PGSurface):
    """Pygame Plotter"""

    def __init__(self, n_data_rows, data_row_colours,
                 width=600, y_range=(-100, 100),
                 background_colour=(40, 40, 40),
                 marker_colour=(200, 200, 200),
                 position=None,
                 axis_colour=None):
        self.n_data_rows = n_data_rows
        self.data_row_colours = data_row_colours
        self.width = width
        self.y_range = y_range
        self.background_colour = background_colour
        self.marker_colour = marker_colour
        if axis_colour is None:
            self.axis_colour = background_colour
        else:
            self.axis_colour = axis_colour
        self._previous = [None] * n_data_rows
        PGSurface.__init__(self, size=(self.width, self._height),
                           position=position)
        self.clear_area()

    @property
    def y_range(self):
        return self.y_range

    @y_range.setter
    def y_range(self, values):
        """tuple with lower and upper values"""
        self._y_range = values
        self._height = self._y_range[1] - self._y_range[0]
        self._plot_axis = (self._y_range[0] <= 0 and \
                           self._y_range[1] >= 0)

    @property
    def data_row_colours(self):
        return self._data_row_colours

    @data_row_colours.setter
    def data_row_colours(self, values):
        """data_row_colours: list of colour"""
        try:
            if not isinstance(values[0], list) and \
                    not isinstance(values[0], tuple):  # one dimensional
                values = [values]
        except:
            values = [[]]  # values is not listpixel_array
        if len(values) != self.n_data_rows:
            raise RuntimeError('Number of data row colour does not match the ' +
                               'defined number of data rows!')
        self._data_row_colours = values

    def clear_area(self):
        self.pixel_array[:, :] = self.background_colour
        if self._plot_axis:
            self.pixel_array[:, self._y_range[1]:self._y_range[1] + 1] = \
                self.axis_colour

    def write_values(self, position, values, set_marker=False):
        if set_marker:
            self.pixel_array[position, :] = self.marker_colour
        else:
            self.pixel_array[position, :] = self.background_colour
        if self._plot_axis and self.axis_colour != self.background_colour:
            self.pixel_array[position, self._y_range[1]:self._y_range[1] + 1] = \
                self.axis_colour

        for c, plot_value in enumerate(self._y_range[1] - \
                    np.array(values, dtype=int)):
            if plot_value >= 0 and self._previous[c] >= 0 \
                    and plot_value <= self._height and \
                            self._previous[c] <= self._height:
                if self._previous[c] > plot_value:
                    self.pixel_array[position, plot_value:self._previous[c] + 1] = \
                        self._data_row_colours[c]
                else:
                    self.pixel_array[position, self._previous[c]:plot_value + 1] = \
                        self._data_row_colours[c]
            self._previous[c] = plot_value

    def update_values(self, values, set_marker=False):
        """
        """
        if type(values) is not Numpy_array_type and \
                not isinstance(values, tuple) and \
                not isinstance(values, list):
            values = [values]
        if len(values) != self.n_data_rows:
            raise RuntimeError('Number of data values does not match the ' +
                               'defined number of data rows!')

        # move plot one pixel to the left
        self.pixel_array[:-1, :] = self.pixel_array[1:, :]
        self.write_values(position=-1, values=values, set_marker=set_marker)



class PlotterThread(threading.Thread):

    def __init__(self, exp, refesh_time):
        super(PlotterThread, self).__init__()
        self._plotter = Plotter(n_data_rows = 2,
            data_row_colours =[ (255,0,0), (0, 255, 0)],
            width=500,
            background_colour=(0,0,0),
            axis_colour = (100,100,100))
        self._exp = exp
        self._new_values = []
        self.lock_new_values = threading.Lock()
        self._stop_request = threading.Event()
        self.refesh_time = refesh_time

    def stop(self):
        self.join()

    def join(self, timeout=None):
        self._stop_request.set()
        super(PlotterThread, self).join(timeout)

    def is_updated(self):
        self.lock_new_values.acquire()
        if len(self._new_values) > 0:
            rtn = False
        else:
            rtn = True
        self.lock_new_values.release()
        return rtn

    def run(self):
        """the plotter thread is constantly updating the the
        pixel_area and """
        update_screen = True
        last_plot_time = 0

        while not self._stop_request.is_set():
            # get data
            self.lock_new_values.acquire()
            values = self._new_values
            self._new_values = []
            self.lock_new_values.release() # release to receive new values

            n = len(values)
            if n > 0:
                update_screen = True
                if n > self._plotter.width:
                    values = values[-1*self._plotter.width:] #only the last
                    n = len(values)
                self._plotter.pixel_array[:-1*n, :] = \
                        self._plotter.pixel_array[n:, :]
                for x in range(-1*n, 0):
                    self._plotter.write_values(position = x,
                            values = values[x][0],
                            set_marker = values[x][1])

            if update_screen and \
                time.time() - last_plot_time > self.refesh_time:
                # expyriment plot
                lock_expyriment.acquire()
                self._plotter.present(update=False, clear=False)
                self._exp.screen.update_stimuli([self._plotter]) #TODO: update screen outsite, exp not required
                lock_expyriment.release()
                update_screen = False
                last_plot_time = time.time()


    def new_values(self, values, set_marker=False):
        """adds new values to the plotter"""
        self.lock_new_values.acquire()
        self._new_values.append((values, set_marker))
        self.lock_new_values.release()
