# Copyright 2013 John Reese
# Licensed under the MIT license

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    pass  # let's be nice and not error out in setup.py

from collections import Counter
from os import path

from .ent import Struct
from .log import logger

log = logger(__name__)
FADED = '#e8e8e8'


class Graph(Struct):
    """Generic graph interface."""

    def __init__(self, title, legend=True, transform=None, **kwargs):
        Struct.__init__(self, title=title, legend=legend,
                        transform=transform, **kwargs)

    def prep(self, plugin, config, network):
        self.plugin = plugin
        self.config = config
        self.network = network

    def filename(self):
        return '{0}_{1}.{2}'.format(self.plugin.name,
                                    self.title.replace(' ', '_'),
                                    self.config.image_format).lower()

    def render(self, output_path):
        """Basic framework for rendering a graph to file.  Sets up a figure,
        chains to Graph.plot() for plotting data, and then save the result to
        the given filename as a PNG image."""
        if self.config.xkcd_mode:
            plt.xkcd()

        plt.figure()
        plt.title(self.title)

        dataset = self.data()
        dataset = self.transformed_data(dataset)
        self.plot(dataset)

        if self.legend:
            plt.legend(loc='best', fontsize='x-small',
                       fancybox=True)

        plt.savefig(path.join(output_path, self.filename()),
                    dpi=200, transparent=False)

    def transformed_data(self, dataset):
        """Subclasses may choose to override this in order to allow for
        more complex options for data transforms."""
        dataset = self.data()

        if self.transform is None:
            return dataset

        if isinstance(dataset, dict):
            return {key: self.transform(key, value, self.network)
                    for key, value in dataset.items()}

        elif isinstance(dataset, list):
            if all(isinstance(d, tuple) for d in dataset):
                return [(key, self.transform(key, value, self.network))
                        for key, value in dataset]
            else:
                return [self.transform(value, self.network)
                        for value in dataset]

        raise ValueError('Unsupported dataset type: %s', type(dataset))

    def data(self):
        """Subclasses should return a set of TimeSeries objects."""
        raise NotImplementedError()

    def plot(self, dataset):
        """Plot points on the graph. This must be implemented by subclasses."""
        raise NotImplementedError()


class TimeSeries(Struct):
    """Representation of time-based data to be plotted. Data should be in the
    format of sortable x,y pairs/tuples, eg. [(1,1), (2,4), (3,8), ...] """

    def __init__(self, label, pairs, color='k', linestyle='-'):
        Struct.__init__(**locals())


class KeysOverTime(Graph):
    """Time-series graph that will plot multiple TimeSeries objects."""

    def plot(self, dataset):
        """Plots a set of data points with the given properties."""
        assert all(isinstance(d, TimeSeries) for d in dataset)

        for timeseries in dataset:
            x, y = zip(*timeseries.pairs)

            plt.plot(x, y,
                     label=timeseries.label,
                     color=timeseries.color,
                     linestyle=timeseries.linestyle)


class ValueComparison(Graph):
    """Graph a set of keys/values, as either a bar or pie chart."""
    def __init__(self, style='bar', **kwargs):
        kwargs['legend'] = False
        Graph.__init__(self, style=style, **kwargs)

    def plot(self, dataset):
        """Plots a bar or pie chart based on key/value data, where keys are
        the labels, and the values are the relative size/amount."""
        if isinstance(dataset, dict):
            dataset = dataset.items()

        if self.style == 'bar':
            ind = np.arange(len(dataset))
            width = 0.8
            pairs = sorted(dataset)
            labels, values = zip(*pairs)

            plt.bar(ind, values, width)
            plt.xticks(ind + width / 2.0, labels)

        elif self.style == 'pie':
            dataset = [(v, k) for k, v in dataset]

            pairs = sorted(dataset, reverse=True)
            values, labels = zip(*pairs)

            plt.pie(values, labels=labels)

        else:
            raise NotImplementedError('Unknown chart style "%s"' % self.style)

    def data(self):
        """Subclasses should return a dictionary mapping labels to values."""
        raise NotImplementedError()


class NetworkKeyOverTime(TimeSeries):
    """Graph a single key over time for an entire network."""

    pass


class ChannelKeyOverTime(TimeSeries):
    """Graph a single key over time for a given channel."""

    pass


class NetworkKeyComparison(ValueComparison):
    """Graph a comparison of user values at the network level."""

    def __init__(self, keys=None, **kwargs):
        ValueComparison.__init__(self, keys=keys, **kwargs)

    def data(self):
        return {self.keys[key]: self.network.stats[key] for key in self.keys}


class NetworkUserComparison(ValueComparison):
    """Graph a comparison of user values at the network level."""

    def __init__(self, key=None, **kwargs):
        ValueComparison.__init__(self, key=key, **kwargs)

    def data(self):
        data = Counter({nick: self.network.users[nick].stats[self.key]
                        for nick in self.network.users})
        return data.most_common(self.config.graph_users)


class ChannelUserComparison(ValueComparison):
    """Graph a comparison of user values at the channel level."""

    pass
