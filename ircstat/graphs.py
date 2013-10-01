# Copyright 2013 John Reese
# Licensed under the MIT license

import matplotlib.pyplot as plt
import numpy as np

from .ent import Struct


FADED = '#e8e8e8'


class Graph(Struct):
    """Generic graph interface."""

    def __init__(self, title, legend=True, **kwargs):
        Struct.__init__(self, title=title, legend=legend, **kwargs)

    def render(self, filename):
        """Basic framework for rendering a graph to file.  Sets up a figure,
        chains to Graph.plot() for plotting data, and then save the result to
        the given filename as a PNG image."""
        plt.figure()
        plt.title(self.title)

        self.plot()

        if self.legend:
            plt.legend(loc='best', fontsize='x-small',
                       fancybox=True)

        plt.savefig(filename, dpi=200, transparent=False)

    def plot(self):
        """Plot points on the graph. This must be implemented by subclasses."""
        raise NotImplementedError()


class TimeSeries(Struct):
    """Representation of time-based data to be plotted. Data should be in the
    format of sortable x,y pairs/tuples, eg. [(1,1), (2,4), (3,8), ...] """

    def __init__(self, label, pairs, color='k', linestyle='-'):
        Struct.__init__(**locals())


class KeysOverTime(Graph):
    """Time-series graph that will plot multiple TimeSeries objects."""

    def plot(self):
        """Plots a set of data points with the given properties."""
        datasets = self.data()
        assert all(isinstance(d, TimeSeries) for d in datasets)

        for dataset in datasets:
            x, y = zip(*dataset.pairs)

            plt.plot(x, y,
                     label=dataset.label,
                     color=dataset.color,
                     linestyle=dataset.linestyle)

    def data(self):
        """Subclasses should return a set of TimeSeries objects."""
        raise NotImplementedError()


class ValueComparison(Graph):
    """Graph a set of keys/values, as either a bar or pie chart."""
    def __init__(self, bars=False, **kwargs):
        kwargs['legend'] = False
        Graph.__init__(self, bars=bars, **kwargs)

    def plot(self):
        """Plots a bar or pie chart based on key/value data, where keys are
        the labels, and the values are the relative size/amount."""
        dataset = self.data()

        if self.bars:
            ind = np.arange(len(dataset))
            width = 0.8
            pairs = sorted([(k, v) for k, v in dataset.items()])
            labels, values = zip(*pairs)

            plt.bar(ind, values, width)
            plt.xticks(ind + width / 2.0, labels)

        else:
            pairs = sorted([(v, k) for k, v in dataset.items()], reverse=True)
            values, labels = zip(*pairs)

            plt.pie(values, labels=labels)

    def data(self):
        """Subclasses should return a dictionary mapping labels to values."""
        raise NotImplementedError()


class NetworkKeyOverTime(TimeSeries):
    """Graph a single key over time for an entire network."""

    pass


class ChannelKeyOverTime(TimeSeries):
    """Graph a single key over time for a given channel."""

    pass


class NetworkUserComparison(ValueComparison):
    """Graph a comparison of user values at the network level."""

    pass


class ChannelUserComparison(ValueComparison):
    """Graph a comparison of user values at the channel level."""

    pass