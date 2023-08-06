from abc import ABCMeta, abstractmethod
from copy import copy
from typing import Union, Sequence, Tuple

import h5py
import numpy as np
from matplotlib.patches import Rectangle

from abtem.base_classes import Grid, HasGridMixin
from abtem.device import asnumpy
from abtem.measure import Calibration, Measurement
from abtem.utils import split_integer


class AbstractScan(metaclass=ABCMeta):

    def __init__(self):
        self._batches = None

    def __len__(self):
        return self.num_positions

    @property
    def num_positions(self):
        return len(self.get_positions())

    @property
    @abstractmethod
    def shape(self) -> tuple:
        """
        The shape the scan.
        """
        pass

    @property
    @abstractmethod
    def calibrations(self) -> tuple:
        """
        The measurement calibrations associated with the scan.
        """
        pass

    @abstractmethod
    def get_positions(self):
        """
        Get the scan positions as numpy array.
        """
        pass

    @abstractmethod
    def insert_new_measurement(self, measurement, start, end, new_values):
        """
        Insert new measurement values into a Measurement object or HDF5 file.

        Parameters
        ----------
        measurement : Measurement object
            The measurement to insert new values.
        start : int
            First index of slice.
        end : int
            Last index of slice.
        new_values : ndarray
            New measurement values to be inserted. Length should be (end - start).
        """
        pass

    def generate_positions(self, max_batch):
        positions = self.get_positions()
        self._partition_batches(max_batch)

        while len(self._batches) > 0:
            start, end = self.get_next_batch()
            yield start, end, positions[start:end]

    def get_next_batch(self):
        return self._batches.pop(0)

    def _partition_batches(self, max_batch):
        n = len(self)
        n_batches = (n + (-n % max_batch)) // max_batch
        batch_sizes = split_integer(len(self), n_batches)
        self._batches = [(0, batch_sizes[0])]
        for batch_size in batch_sizes[1:]:
            self._batches.append((self._batches[-1][-1], self._batches[-1][-1] + batch_size))

    @abstractmethod
    def __copy__(self):
        pass

    def copy(self):
        """
        Make a copy.
        """
        return copy(self)


class PositionScan(AbstractScan):
    """
    Position scan object.

    Defines a scan based on user-defined positions.

    Parameters
    ----------
    positions : list of xy-positions
        The scan positions [Å].
    """

    def __init__(self, positions: np.ndarray):

        self._positions = np.array(positions)

        if (len(self._positions.shape) != 2) or (self._positions.shape[1] != 2):
            raise RuntimeError('The shape of the sequence of positions must be (n, 2).')

        super().__init__()

    @property
    def shape(self) -> tuple:
        return (len(self),)

    @property
    def calibrations(self) -> tuple:
        return (None,)

    def insert_new_measurement(self, measurement, start, end, new_measurement):
        if isinstance(measurement, str):
            with h5py.File(measurement, 'a') as f:
                f['array'][start:end] = asnumpy(new_measurement)

        else:
            measurement.array[start:end] = asnumpy(new_measurement)

    def get_positions(self):
        return self._positions

    def __copy__(self):
        return self.__class__(self._positions.copy())


class LineScan(AbstractScan, HasGridMixin):
    """
    Line scan object.

    Defines the scan along a straight line.

    Parameters
    ----------
    start : two float
        Start point of the scan [Å].
    end : two float
        End point of the scan [Å].
    gpts: int
        Number of scan positions.
    sampling: float
        Sampling rate of scan positions [1 / Å].
    endpoint: bool
        If True, end is the last position. Otherwise, it is not included. Default is True.
    """

    def __init__(self, start: Sequence[float], end: Sequence[float],
                 gpts: Union[int, Sequence[int]] = None,
                 sampling: Union[float, Sequence[float]] = None,
                 endpoint: bool = True):

        super().__init__()

        start = np.array(start)
        end = np.array(end)

        if (start.shape != (2,)) | (end.shape != (2,)):
            raise ValueError('Scan start/end has incorrect shape')

        if (gpts is None) & (sampling is None):
            raise RuntimeError('Grid gpts or sampling must be set')

        self._grid = Grid(gpts=gpts, sampling=sampling, endpoint=endpoint, dimensions=1)
        self._start = start
        self._direction, self.extent = self._direction_and_extent(start, end)

    def _direction_and_extent(self, start, end):
        extent = np.linalg.norm((end - start), axis=0)
        direction = (end - start) / extent
        return direction, extent

    @property
    def shape(self) -> Tuple[int]:
        return (self.gpts[0],)

    @property
    def calibrations(self) -> Tuple[Calibration]:
        return (Calibration(offset=0, sampling=self.sampling[0], units='Å', name='x'),)

    @property
    def start(self) -> np.ndarray:
        """
        Start point of the scan [Å].
        """
        return self._start

    @start.setter
    def start(self, start: Sequence[float]):
        self._start = np.array(start)
        self._direction, self.extent = self._direction_and_extent(self._start, self.end)

    @property
    def end(self) -> np.ndarray:
        """
        End point of the scan [Å].
        """
        return self.start + self.direction * self.extent

    @end.setter
    def end(self, end: Sequence[float]):
        self._direction, self.extent = self._direction_and_extent(self.start, end)

    @property
    def direction(self) -> np.ndarray:
        """
        Direction of the scan line.
        """
        return self._direction

    def insert_new_measurement(self,
                               measurement: Measurement,
                               start: int,
                               end: int,
                               new_measurement_values: np.ndarray):

        if isinstance(measurement, str):
            with h5py.File(measurement, 'a') as f:
                f['array'][start:end] += asnumpy(new_measurement_values)

        else:
            measurement.array[start:end] += asnumpy(new_measurement_values)

    def get_positions(self) -> np.ndarray:
        x = np.linspace(self.start[0], self.start[0] + np.array(self.extent) * self.direction[0], self.gpts[0],
                        endpoint=self.grid.endpoint)
        y = np.linspace(self.start[1], self.start[1] + np.array(self.extent) * self.direction[1], self.gpts[0],
                        endpoint=self.grid.endpoint)
        return np.stack((np.reshape(x, (-1,)), np.reshape(y, (-1,))), axis=1)

    def add_to_mpl_plot(self, ax, linestyle: str = '-', color: str = 'r', **kwargs):
        """
        Add a visualization of the scan line to a matplotlib axes.

        Parameters
        ----------
        ax : matplotlib Axes
            The axes of the matplotlib plot the visualization should be added to.
        linestyle : str
            Linestyle of scan line.
        color : str
            Color of the scan line.
        kwargs :
            Additional options for matplotlib.pyplot.plot as keyword arguments.
        """
        ax.plot([self.start[0], self.end[0]], [self.start[1], self.end[1]], linestyle=linestyle, color=color, **kwargs)

    def __copy__(self):
        return self.__class__(start=self.start, end=self.end, gpts=self.gpts, endpoint=self.grid.endpoint)


def unravel_slice_2d(start: int, end: int, shape: Tuple[int, int]):
    slices = []
    rows = []
    slices_1d = []
    n = 0
    n_accum = 0
    for index in range(start, end):
        index_in_row = index % shape[-1]
        n += 1
        if index_in_row == shape[-1] - 1:
            slices_1d.append(slice(n_accum, n_accum + n))
            slices.append(slice(index_in_row - n + 1, index_in_row + 1))
            rows.append(index // shape[-1])
            n_accum += n
            n = 0
    if n > 0:
        slices_1d.append(slice(n_accum, n_accum + n))
        slices.append(slice(index_in_row - n + 1, index_in_row + 1))
        rows.append(index // shape[-1])
    return rows, slices, slices_1d


class GridScan(AbstractScan, HasGridMixin):
    """
    Grid scan object.

    Defines the scan on a regular grid.

    Parameters
    ----------
    start : two float
        Start corner of the scan [Å].
    end : two float
        End corner of the scan [Å].
    gpts: two int
        Number of scan positions in the x- and y-direction of the scan.
    sampling: two float
        Sampling rate of scan positions [1 / Å].
    endpoint: bool
        If True, end is the last position. Otherwise, it is not included. Default is True.
    """

    def __init__(self, start, end, gpts=None, sampling=None, endpoint=False):

        super().__init__()

        self._start = np.array(start)
        end = np.array(end)

        if (self._start.shape != (2,)) | (end.shape != (2,)):
            raise ValueError('Scan start/end has incorrect shape')

        if (gpts is None) & (sampling is None):
            raise RuntimeError('Grid gpts or sampling must be set')

        self._grid = Grid(extent=end - start, gpts=gpts, sampling=sampling, dimensions=2, endpoint=endpoint)

    @property
    def shape(self):
        return tuple(self.gpts)

    @property
    def calibrations(self) -> tuple:
        return (Calibration(offset=0, sampling=self.sampling[0], units='Å', name='x'),
                Calibration(offset=0, sampling=self.sampling[1], units='Å', name='y'))

    @property
    def start(self) -> np.ndarray:
        """
        Start corner of the scan [Å].
        """
        return self._start

    @start.setter
    def start(self, start: Sequence[float]):
        self._start = np.array(start)
        self.extent = self.end - self._start

    @property
    def end(self) -> np.ndarray:
        """
        End corner of the scan [Å].
        """
        return self.start + self.extent

    @end.setter
    def end(self, end: Sequence[float]):
        self.extent = np.array(end) - self.start

    def get_scan_area(self) -> float:
        """
        Get the area of the scan.
        """
        height = abs(self.start[0] - self.end[0])
        width = abs(self.start[1] - self.end[1])
        return height * width

    def get_positions(self) -> np.ndarray:
        x = np.linspace(self.start[0], self.end[0], self.gpts[0], endpoint=self.grid.endpoint)
        y = np.linspace(self.start[1], self.end[1], self.gpts[1], endpoint=self.grid.endpoint)
        x, y = np.meshgrid(x, y, indexing='ij')
        return np.stack((np.reshape(x, (-1,)),
                         np.reshape(y, (-1,))), axis=1)

    def insert_new_measurement(self, measurement, start, end, new_measurement):
        for row, slic, slic_1d in zip(*unravel_slice_2d(start, end, self.shape)):
            if isinstance(measurement, str):
                with h5py.File(measurement, 'a') as f:
                    f['array'][row, slic] += asnumpy(new_measurement[slic_1d])
            else:
                measurement.array[row, slic] += asnumpy(new_measurement[slic_1d])

    def add_to_mpl_plot(self, ax, alpha=.33, facecolor='r', edgecolor='r', **kwargs):
        """
        Add a visualization of the scan area to a matplotlib axes.

        Parameters
        ----------
        ax : matplotlib Axes
            The axes of the matplotlib plot the visualization should be added to.
        alpha : float
            Transparency of the scan area visualization.
        color : str
            Color of the scan area visualization.
        kwargs :
            Additional options for matplotlib.patches.Rectangle used for the scan area visualization as keyword arguments.
        """
        rect = Rectangle(tuple(self.start), *self.extent, alpha=alpha, facecolor=facecolor, edgecolor=edgecolor,
                         **kwargs)
        ax.add_patch(rect)

    def __copy__(self):
        return self.__class__(start=self.start, end=self.end, gpts=self.gpts, endpoint=self.grid.endpoint)