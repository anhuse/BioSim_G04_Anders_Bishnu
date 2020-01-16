# -*- coding: utf-8 -*-

__author__ = "Anders Huse, Bishnu Poudel"
__email__ = "anhuse@nmbu.no; bipo@nmbu.no"

import seaborn as sns
import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt

# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif

class Visualization:
    """
    Plotting island map , heatmaps and line graph
    """

    def show(self):
        plt.show()
    def __init__(self, object_matrix, img_dir=None,
                 img_name=_DEFAULT_GRAPHICS_NAME,
                 img_fmt='png'):
        """
        :param object_matrix: 2D array of cell objects containing herbivores
        and carnivores
        """
        self.object_matrix = object_matrix
        self._step = 0
        self._final_step = 20
        self._img_ctr = 0

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None
        self._img_fmt = img_fmt




        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._mean_ax = None
        self._mean_line = None
        self._herb_ax = None
        self._carn_ax = None
        self._herb_axis = None
        self._carn_axis = None

    def simulate(self, num_steps, vis_steps=1, img_steps=None):
        """
        Simulates prosess
        :param num_steps:
        :param vis_steps:
        :param img_steps:
        :return:
        """


    def _set_graphics(self):
        """
        sets the graphics
        :return:
        """

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(2, 2, 1)
            self._img_axis = None

        if self._herb_ax is None:
            self._herb_ax = self._fig.add_subplot(2, 2, 2)
            self._herb_axis = None

        if self._carn_ax is None:
            self._carn_ax = self._fig.add_subplot(2, 2, 3)
            self._carn_axis = None

        if self._mean_ax is None:
           self._mean_ax = self._fig.add_subplot(2, 2, 4)
           self._mean_ax.set_ylim(0, 50)

        # needs updating on subsequent calls to simulate()
        self._mean_ax.set_xlim(0, self._final_step + 1)

        if self._mean_line is None:
            mean_plot = self._mean_ax.plot(np.arange(0, self._final_step),
                                           np.full(self._final_step, np.nan))
            self._mean_line = mean_plot[0]
        else:
            xdata, ydata = self._mean_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_step)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._mean_line.set_data(np.hstack((xdata, xnew)),
                                         np.hstack((ydata, ynew)))


    def create_map(self, data):
        """
        Updates map
        :return:
        """
        self._img_axis = self._map_ax.imshow(data, cmap='terrain'
                                             , vmax=20, vmin=1)


    def update_herb_ax(self, herb_data):
        """
        Updates herb_ax
        :return:
        """
        if self._herb_axis is not None:
            self._herb_axis.set_data(herb_data)

        else:
            self._herb_axis = self._herb_ax.imshow(herb_data,
                                                 interpolation='nearest',
                                                 cmap="Greens")


    def update_carn_ax(self, carn_data):
        """
    Updates carn_ax
        :return:
        """
        if self._carn_axis is not None:
            self._carn_axis.set_data(carn_data)

        else:
            # self._carn_axis = sns.heatmap(carn_data, linewidth=0.5,
            #                              cmap="OrRd", ax=self._carn_ax)
            self._carn_axis = self._carn_ax.imshow(carn_data,
                                                 interpolation='nearest',
                                                 cmap="OrRd")


    def update_mean_ax(self, herb_num, carn_num):
        ydata = self._mean_line.get_ydata()
        ydata[self._step] = herb_num
        self._mean_line.set_ydata(ydata)
        self._step += 1
        # plt.show()

    def update_graphics(self, herb_pos, carn_pos, num_animals):
        """
        Updates graphics with current data
        :return:
        """
        # create_map will be called separately
        self.update_herb_ax(herb_pos)
        self.update_carn_ax(carn_pos)
        self.update_mean_ax(num_animals["Herbivore"], num_animals["Carnivore"])

        plt.pause(1e-6)


    def save_graphics(self):
        """
        Saves graphics
        :return:
        """

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        # self._img_ctr += 1



    def make_movie(self):
        """
        Makes a movie of a series of images
        :return:
        """
        subprocess.check_call([_FFMPEG_BINARY,
                               '-i', 'Image-%03d.png',
                               '-y',
                               # '-f','image2',
                               # '-vcodec','mpeg4'
                               '-r', '0.2',
                               '-profile:v', 'baseline',
                               '-level', '3.0',
                               '-pix_fmt', 'yuv420p',
                               'Movie.mp4'])






