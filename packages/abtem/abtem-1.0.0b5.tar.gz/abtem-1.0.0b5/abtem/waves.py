from copy import copy
from typing import Union, Sequence, Tuple

import h5py
import numpy as np
from ase import Atoms

from abtem.base_classes import Grid, Accelerator, cache_clear_callback, Cache, cached_method, HasGridAndAcceleratorMixin
from abtem.detect import AbstractDetector, _crop_to_center
from abtem.device import get_array_module, get_device_function, asnumpy, get_array_module_from_device, \
    copy_to_device, get_available_memory, HasDeviceMixin
from abtem.measure import calibrations_from_grid, Measurement
from abtem.plot import show_line
from abtem.potentials import Potential, AbstractPotential, AbstractTDSPotentialBuilder, AbstractPotentialBuilder, \
    ProjectedPotentialArray
from abtem.scan import AbstractScan
from abtem.transfer import CTF
from abtem.utils import polargrid, ProgressBar, cosine_window, spatial_frequencies, coordinates, split_integer


class FresnelPropagator:
    """
    Fresnel propagator class.

    This class is used for propagating a wave function object using the near-field approximation (Fresnel diffraction).
    The array representing the Fresnel propagator function is cached.
    """

    def __init__(self):
        self._cache = Cache(1)

    @classmethod
    def _antialiasing_aperture(cls, gpts: Tuple[int]) -> np.ndarray:
        x = 1 - cosine_window(np.abs(np.fft.fftfreq(gpts[0])), .25, .1, 'high')
        y = 1 - cosine_window(np.abs(np.fft.fftfreq(gpts[1])), .25, .1, 'high')
        return x[:, None] * y[None]

    @cached_method('_cache')
    def _evaluate_propagator_array(self, gpts: Tuple[int], sampling: Tuple[float], wavelength: float, dz: float,
                                   xp) -> np.ndarray:
        complex_exponential = get_device_function(xp, 'complex_exponential')
        kx = xp.fft.fftfreq(gpts[0], sampling[0]).astype(xp.float32)
        ky = xp.fft.fftfreq(gpts[1], sampling[1]).astype(xp.float32)
        f = (complex_exponential(-(kx ** 2)[:, None] * np.pi * wavelength * dz) *
             complex_exponential(-(ky ** 2)[None] * np.pi * wavelength * dz))
        f *= xp.asarray(self._antialiasing_aperture(gpts))
        return f

    def propagate(self, waves: Union['Waves', 'SMatrixArray'], dz: float) -> Union['Waves', 'SMatrixArray']:
        """
        Propgate wave function or scattering matrix.

        Parameters
        ----------
        waves: Waves or SMatrixArray object
            Wave function or scattering matrix to propagate.
        dz: float
            Propagation distance [Å].
        """
        propagator_array = self._evaluate_propagator_array(waves.grid.gpts,
                                                           waves.grid.sampling,
                                                           dz,
                                                           waves.wavelength,
                                                           get_array_module(waves.array))

        fft2_convolve = get_device_function(get_array_module(waves.array), 'fft2_convolve')

        fft2_convolve(waves._array, propagator_array, overwrite_x=True)
        return waves


def transmit(waves: Union['Waves', 'SMatrixArray'], potential_slice: ProjectedPotentialArray):
    """
    Transmit wave function or scattering matrix.

    Parameters
    ----------
    waves: Waves object
        Wave function or scattering matrix to propagate.
    potential_slice: ProjectedPotential object
        Projected potential to transmit the wave function through.
    """
    xp = get_array_module(waves.array)
    complex_exponential = get_device_function(xp, 'complex_exponential')
    dim_padding = len(waves._array.shape) - len(potential_slice.array.shape)
    slice_array = potential_slice.array.reshape((1,) * dim_padding + potential_slice.array.shape)

    if np.iscomplexobj(slice_array):
        waves._array *= copy_to_device(slice_array, xp)
    else:
        waves._array *= complex_exponential(copy_to_device(waves.accelerator.sigma * slice_array, xp))

    return waves


def _multislice(waves: Union['Waves', 'SMatrixArray'],
                potential: AbstractPotential,
                propagator: FresnelPropagator = None,
                pbar: Union[ProgressBar, bool] = True) -> Union['Waves', 'SMatrixArray']:
    waves.grid.match(potential)

    waves.accelerator.check_is_defined()
    waves.grid.check_is_defined()

    if propagator is None:
        propagator = FresnelPropagator()

    if isinstance(pbar, bool):
        pbar = ProgressBar(total=len(potential), desc='Multislice', disable=not pbar)

    pbar.reset()
    for potential_slice in potential:
        transmit(waves, potential_slice)
        waves = propagator.propagate(waves, potential_slice.thickness)
        pbar.update(1)

    pbar.refresh()
    return waves


class Waves(HasGridAndAcceleratorMixin):
    """
    Waves object.

    The waves object can define a batch of arbitrary 2D wavefunctions defined by a complex numpy array.

    Parameters
    ----------
    extent: one or two float
        Lateral extent of wavefunction [Å].
    gpts: one or two int
        Number of grid points describing the wave function.
    sampling: one or two float
        Lateral sampling of wavefunctions [1 / Å].
    energy: float
        Electron energy [eV].
    """

    def __init__(self,
                 array: np.ndarray,
                 extent: Union[float, Sequence[float]] = None,
                 sampling: Union[float, Sequence[float]] = None,
                 energy: float = None):

        if len(array.shape) < 2:
            raise RuntimeError('Wave function array should be have 2 dimensions or more')

        self._array = array
        self._grid = Grid(extent=extent, gpts=array.shape[-2:], sampling=sampling, lock_gpts=True)
        self._accelerator = Accelerator(energy=energy)

    @property
    def array(self) -> np.ndarray:
        """
        Array representing the wave functions.
        """
        return self._array

    def intensity(self) -> Measurement:
        """
        Calculate the intensity of the wave functions at the image plane.

        Returns
        -------
        Measurement
            The wave function intensity.
        """
        calibrations = calibrations_from_grid(self.grid.gpts, self.grid.sampling, ['x', 'y'])
        calibrations = (None,) * (len(self.array.shape) - 2) + calibrations

        abs2 = get_device_function(get_array_module(self.array), 'abs2')
        return Measurement(abs2(self.array), calibrations)

    def diffraction_pattern(self) -> Measurement:
        """
        Calculate the intensity of the wave functions at the diffraction plane.

        Returns
        -------
        Measurement
            The intensity of the diffraction patterns.
        """
        calibrations = calibrations_from_grid(self.grid.antialiased_gpts,
                                              self.grid.antialiased_sampling,
                                              names=['alpha_x', 'alpha_y'],
                                              units='mrad',
                                              scale_factor=self.wavelength * 1000,
                                              fourier_space=True)

        calibrations = (None,) * (len(self.array.shape) - 2) + calibrations

        xp = get_array_module(self.array)
        abs2 = get_device_function(xp, 'abs2')
        fft2 = get_device_function(xp, 'fft2')
        pattern = asnumpy(abs2(_crop_to_center(xp.fft.fftshift(fft2(self.array, overwrite_x=False)))))
        return Measurement(pattern, calibrations)

    def apply_ctf(self, ctf: CTF = None, **kwargs):
        """
        Apply the aberrations defined by a CTF object to wave function.

        Parameters
        ----------
        ctf: CTF
            Contrast Transfer Function object to be applied.
        kwargs:
            Provide the aberration coefficients as keyword arguments.

        Returns
        -------
        Wave object
            The wave functions with aberrations applied.
        """
        xp = get_array_module(self.array)
        fft2_convolve = get_device_function(get_array_module(self.array), 'fft2_convolve')

        if ctf is None:
            ctf = CTF(**kwargs)

        ctf.accelerator.match(self.accelerator)
        kx, ky = spatial_frequencies(self.grid.gpts, self.grid.sampling)
        alpha, phi = polargrid(xp.asarray(kx * self.wavelength), xp.asarray(ky * self.wavelength))
        kernel = ctf.evaluate(alpha, phi)

        return self.__class__(fft2_convolve(self.array, kernel, overwrite_x=False),
                              extent=self.extent,
                              energy=self.energy)

    def multislice(self,
                   potential: AbstractPotential,
                   reduce_tds: str = None,
                   pbar: Union[ProgressBar, bool] = True) -> 'Waves':
        """
        Propagate and transmit wave function through the provided potential.

        Parameters
        ----------
        potential: Potential
            The potential through which to propagate the wave function.
        pbar: bool
            If true, display a progress bar.

        Returns
        -------
        Wave object
            Wave function at the exit plane of the potential.
        """
        self.grid.match(potential)

        propagator = FresnelPropagator()

        if isinstance(potential, AbstractTDSPotentialBuilder):
            xp = get_array_module(self.array)
            N = len(potential.frozen_phonons)

            out_array = xp.zeros((N,) + self.array.shape, dtype=xp.complex64)

            # TODO : implement reduction operation
            tds_pbar = ProgressBar(total=N, desc='TDS', disable=(not pbar) or (N == 1))
            multislice_pbar = ProgressBar(total=len(potential), desc='Multislice', disable=not pbar)

            for i, potential_config in enumerate(potential.generate_frozen_phonon_potentials(pbar=pbar)):
                multislice_pbar.reset()

                exit_waves = _multislice(copy(self), potential_config, propagator=propagator, pbar=multislice_pbar)
                out_array[i] = exit_waves.array

                tds_pbar.update(1)

            tds_waves = self.__class__(out_array, extent=self.extent, energy=self.energy)

            multislice_pbar.close()
            tds_pbar.close()

            return tds_waves
        else:
            return _multislice(self, potential, propagator, pbar)

    def write(self, path: str):
        """
        Write wave functions to a hdf5 file.

        path: str
            The path to write the file.
        """
        with h5py.File(path, 'w') as f:
            f.create_dataset('array', data=self.array)
            f.create_dataset('energy', data=self.energy)
            f.create_dataset('extent', data=self.extent)

    @classmethod
    def read(cls, path: str) -> 'Waves':
        """
        Read wave functions from a hdf5 file.

        path: str
            The path to read the file.
        """

        with h5py.File(path, 'r') as f:
            datasets = {}
            for key in f.keys():
                datasets[key] = f.get(key)[()]

        return cls(array=datasets['array'], extent=datasets['extent'], energy=datasets['energy'])

    def __getitem__(self, item):
        if len(self.array.shape) <= self.grid.dimensions:
            raise RuntimeError()
        return self.__class__(array=self._array[item], extent=self.extent, energy=self.energy)

    def show(self, **kwargs):
        """
        Show the wave function.

        kwargs:
            Additional keyword arguments for the abtem.plot.show_image function.
        """
        self.intensity().show(**kwargs)

    def __copy__(self):
        new_copy = self.__class__(array=self._array.copy())
        new_copy._grid = copy(self.grid)
        new_copy._accelerator = copy(self.accelerator)
        return new_copy

    def copy(self):
        """
        Return a copy.
        """
        return copy(self)


class PlaneWave(HasGridAndAcceleratorMixin, HasDeviceMixin):
    """
    Plane wave object.

    The plane wave object is used for building plane waves.

    Parameters
    ----------
    extent: two float
        Lateral extent of wavefunction [Å].
    gpts: two int
        Number of grid points describing the wave function.
    sampling: two float
        Lateral sampling of wavefunctions [1 / Å].
    energy: float
        Electron energy [eV].
    device: str
        The plane waves will be build on this device.
    """

    def __init__(self,
                 extent: Union[float, Sequence[float]] = None,
                 gpts: Union[int, Sequence[int]] = None,
                 sampling: Union[float, Sequence[float]] = None,
                 energy: float = None,
                 device: str = 'cpu'):
        self._grid = Grid(extent=extent, gpts=gpts, sampling=sampling)
        self._accelerator = Accelerator(energy=energy)
        self._device = device

    def multislice(self, potential: Union[AbstractPotential, Atoms], pbar: bool = True) -> Waves:
        """
        Build plane wave function and propagate it through the potential.

        The grid of the potential will be matched to the wave function.

        Parameters
        ----------
        potential: Potential or Atoms object
            The potential through which to propagate the wave function.
        pbar: bool
            If true, display a progress bar.

        Returns
        -------
        Waves object
            Wave function at the exit plane of the potential.
        """
        if isinstance(potential, Atoms):
            potential = Potential(atoms=potential)
        potential.grid.match(self)

        return self.build().multislice(potential, pbar=pbar)

    def build(self) -> Waves:
        """
        Build the plane wave function as a Waves object.
        """
        xp = get_array_module_from_device(self._device)
        self.grid.check_is_defined()
        array = xp.ones((self.gpts[0], self.gpts[1]), dtype=xp.complex64)
        return Waves(array, extent=self.extent, energy=self.energy)

    def __copy__(self, a) -> 'PlaneWave':
        return self.__class__(extent=self.extent, gpts=self.gpts, sampling=self.sampling, energy=self.energy)

    def copy(self):
        """
        Make a copy.
        """
        return copy(self)


class Probe(HasGridAndAcceleratorMixin, HasDeviceMixin):
    """
    Probe wave function object.

    The probe object can represent a stack of electron probe wave function for simulating scanning transmission
    electron microscopy.

    See the docs of abtem.transfer.CTF for a description of the parameters related to the contrast transfer function.

    Parameters
    ----------
    semiangle_cutoff: float
        Convergence semi-angle [mrad.].
    rolloff: float
        Softens the cutoff. A value of 0 gives a hard cutoff, while 1 gives the softest possible cutoff.
    focal_spread: float
        The focal spread of the probe.
    angular_spread: float
        The angular spread of the probe
    ctf_parameters: dict
        The parameters describing the phase aberrations using polar notation or an alias.
    extent: two float, optional
        Lateral extent of wave functions [Å].
    gpts: two int, optional
        Number of grid points describing the wave functions.
    sampling: two float, optional
        Lateral sampling of wave functions [1 / Å].
    energy: float, optional
        Electron energy [eV].
    device: str
        The probe wave functions will be build on this device.
    kwargs:
        Provide the aberration coefficients as keyword arguments.
    """

    def __init__(self,
                 semiangle_cutoff: float = np.inf,
                 rolloff: float = 0.1,
                 focal_spread: float = 0.,
                 angular_spread: float = 0.,
                 ctf_parameters: dict = None,
                 extent: Union[float, Sequence[float]] = None,
                 gpts: Union[int, Sequence[int]] = None,
                 sampling: Union[float, Sequence[float]] = None,
                 energy: float = None,
                 device='cpu',
                 **kwargs):

        self._ctf = CTF(semiangle_cutoff=semiangle_cutoff, rolloff=rolloff, focal_spread=focal_spread,
                        angular_spread=angular_spread, parameters=ctf_parameters, energy=energy, **kwargs)
        self._accelerator = self._ctf._accelerator
        self._grid = Grid(extent=extent, gpts=gpts, sampling=sampling)
        self._ctf_cache = Cache(1)

        self._ctf.changed.register(cache_clear_callback(self._ctf_cache))
        self._grid.changed.register(cache_clear_callback(self._ctf_cache))
        self._accelerator.changed.register(cache_clear_callback(self._ctf_cache))

        self._device = device

    @property
    def ctf(self) -> CTF:
        """
        Probe contrast transfer function.
        """
        return self._ctf

    @ctf.setter
    def ctf(self, new_ctf):
        self._ctf = new_ctf
        self._ctf_cache.clear()

    def _fourier_translation_operator(self, positions):
        xp = get_array_module(positions)
        complex_exponential = get_device_function(xp, 'complex_exponential')

        kx, ky = spatial_frequencies(self.grid.gpts, self.grid.sampling)
        kx = kx.reshape((1, -1, 1))
        ky = ky.reshape((1, 1, -1))
        kx = xp.asarray(kx)
        ky = xp.asarray(ky)
        positions = xp.asarray(positions)
        x = positions[:, 0].reshape((-1,) + (1, 1))
        y = positions[:, 1].reshape((-1,) + (1, 1))

        return complex_exponential(2 * np.pi * kx * x) * complex_exponential(2 * np.pi * ky * y)

    @cached_method('_ctf_cache')
    def _evaluate_ctf(self, xp):
        kx, ky = spatial_frequencies(self.grid.gpts, self.grid.sampling)
        alpha, phi = polargrid(xp.asarray(kx * self.wavelength), xp.asarray(ky * self.wavelength))
        return self._ctf.evaluate(alpha, phi)

    def build(self, positions: Sequence[Sequence[float]] = None) -> Waves:
        """
        Build probe wave functions at the provided positions.

        Parameters
        ----------
        positions: Array of xy-positions
            Positions of the probe wave functions

        Returns
        -------
        Waves object
            Probe wave functions as a Waves object.
        """

        self.grid.check_is_defined()
        self.accelerator.check_is_defined()
        xp = get_array_module_from_device(self._device)
        fft2 = get_device_function(xp, 'fft2')

        if positions is None:
            positions = xp.zeros((1, 2), dtype=xp.float32)
        else:
            positions = xp.array(positions, dtype=xp.float32)

        if len(positions.shape) == 1:
            positions = xp.expand_dims(positions, axis=0)

        array = fft2(self._evaluate_ctf(xp) * self._fourier_translation_operator(positions), overwrite_x=True)
        return Waves(array, extent=self.extent, energy=self.energy)

    def multislice(self, positions: Sequence[Sequence[float]], potential: AbstractPotential, pbar=True) -> Waves:
        """
        Build probe wave functions at the provided positions and propagate them through the potential.

        Parameters
        ----------
        positions: Array of xy-positions
            Positions of the probe wave functions.
        potential: Potential or Atoms object
            The probe batch size. Larger batches are faster, but require more memory.
        pbar: bool
            If true, display progress bars.

        Returns
        -------
        Waves object
            Probe exit wave functions as a Waves object.
        """

        if isinstance(potential, Atoms):
            potential = Potential(potential)

        self.grid.match(potential)
        return _multislice(self.build(positions), potential, None, pbar)

    def _generate_probes(self, scan: AbstractScan, potential: Union[AbstractPotential, Atoms], max_batch: int):
        if not isinstance(max_batch, int):
            memory_per_wave = 2 * 4 * np.prod(self.gpts)
            available_memory = get_available_memory(self._device)
            max_batch = min(int(available_memory * .5 / memory_per_wave), 64)

        for start, end, positions in scan.generate_positions(max_batch=max_batch):
            yield start, end, self.multislice(positions, potential, pbar=False)

    def _generate_tds_probes(self, scan, potential, max_batch, pbar):
        tds_bar = ProgressBar(total=len(potential.frozen_phonons), desc='TDS',
                              disable=(not pbar) or (len(potential.frozen_phonons) == 1))
        potential_pbar = ProgressBar(total=len(potential), desc='Potential', disable=not pbar)

        for potential_config in potential.generate_frozen_phonon_potentials(pbar=potential_pbar):
            yield self._generate_probes(scan, potential_config, max_batch)
            tds_bar.update(1)

        potential_pbar.close()
        tds_bar.refresh()
        tds_bar.close()

    def scan(self,
             scan: AbstractScan,
             detectors: Union[AbstractDetector, Sequence[AbstractDetector]],
             potential: Union[Atoms, AbstractPotential],
             max_batch: int = None,
             pbar: bool = True) -> dict:

        """
        Raster scan the probe across the potential and record a measurement for each detector.

        Parameters
        ----------
        scan: Scan object
            Scan object defining the positions of the probe wave functions.
        detectors: List of detector objects
            The detectors recording the measurements.
        potential: Potential
            The potential to scan the probe over.
        max_batch: int
            The probe batch size. Larger batches are faster, but require more memory.
        pbar: bool
            If true, display progress bars.

        Returns
        -------
        dict
            Dictionary of measurements with keys given by the detector.
        """

        self.grid.match(potential.grid)
        self.grid.check_is_defined()

        if isinstance(detectors, AbstractDetector):
            detectors = [detectors]

        measurements = {}
        for detector in detectors:
            measurements[detector] = detector.allocate_measurement(self.grid, self.wavelength, scan)

        scan_bar = ProgressBar(total=len(scan), desc='Scan', disable=not pbar)

        if isinstance(potential, AbstractTDSPotentialBuilder):
            probe_generators = self._generate_tds_probes(scan, potential, max_batch, pbar)
        else:
            if isinstance(potential, AbstractPotentialBuilder):
                potential = potential.build(pbar=True)

            probe_generators = [self._generate_probes(scan, potential, max_batch)]

        for probe_generator in probe_generators:
            scan_bar.reset()
            for start, end, exit_probes in probe_generator:

                for detector, measurement in measurements.items():
                    new_measurement = detector.detect(exit_probes)

                    if isinstance(potential, AbstractTDSPotentialBuilder):
                        # TODO : this should be more efficient
                        new_measurement /= len(potential.frozen_phonons)

                    scan.insert_new_measurement(measurement, start, end, new_measurement)

                scan_bar.update(end - start)

            scan_bar.refresh()

        scan_bar.close()
        return measurements

    def show_profile(self, **kwargs):
        """
        Show the profile of the probe wave function.

        Parameters
        ----------
        kwargs: Additional keyword arguments for the abtem.plot.show_image function.
        """
        self.grid.check_is_defined()
        measurement = self.build((self.extent[0] / 2, self.extent[1] / 2)).intensity()

        array = measurement.array[0]
        array = array[array.shape[0] // 2, :]
        calibration = calibrations_from_grid(gpts=(self.grid.gpts[1],),
                                             sampling=(self.grid.sampling[1],),
                                             names=['x'])[0]
        show_line(array, calibration, **kwargs)

    def show(self, **kwargs):
        """
        Show the probe wave function.

        Parameters
        ----------
        kwargs: Additional keyword arguments for the abtem.plot.show_image function.
        """
        self.grid.check_is_defined()
        measurement = self.build((self.extent[0] / 2, self.extent[1] / 2)).intensity()
        return measurement.show(**kwargs)

    def __copy__(self) -> 'Probe':
        new_copy = self.__class__()
        new_copy._grid = copy(self.grid)
        new_copy._ctf = copy(self.ctf)
        new_copy._accelerator = copy(self._ctf._accelerator)
        return new_copy

    def copy(self):
        """
        Make a copy.
        """
        return copy(self)


class SMatrixArray(HasGridAndAcceleratorMixin, HasDeviceMixin):
    """
    Scattering matrix array object.

    The scattering matrix array object represents a plane wave expansion of a probe, it is used for STEM simulations
    with the PRISM algorithm.

    Parameters
    ----------
    array: 3d array
        The array representation of the scattering matrix.
    expansion_cutoff: float
        The angular cutoff of the plane wave expansion [mrad].
    interpolation: one or two int
        Interpolation factor.
    k: 2d array
        The spatial frequencies of each plane in the plane wave expansion.
    ctf: CTF object
        The probe contrast transfer function.
    extent: one or two float
        Lateral extent of wave functions [Å].
    gpts: one or two int
        Number of grid points describing the wave functions.
    sampling: one or two float
        Lateral sampling of wave functions [1 / Å].
    energy: float
        Electron energy [eV].
    device: str
        The calculations will be carried out on this device.
    """

    def __init__(self,
                 array: np.ndarray,
                 expansion_cutoff: float,
                 interpolation: int,
                 k: np.ndarray,
                 ctf: CTF = None,
                 extent: Union[float, Sequence[float]] = None,
                 sampling: Union[float, Sequence[float]] = None,
                 energy: float = None,
                 device: str = 'cpu'):

        self._array = array
        self._interpolation = interpolation
        self._expansion_cutoff = expansion_cutoff
        self._k = k
        self._grid = Grid(extent=extent, gpts=array.shape[1:], sampling=sampling, lock_gpts=True)

        self._accelerator = Accelerator(energy=energy)

        if ctf is None:
            ctf = CTF(semiangle_cutoff=expansion_cutoff, rolloff=.1)

        self.ctf = ctf
        self._device = device

    @property
    def ctf(self) -> CTF:
        """
        Probe contrast transfer function.
        """
        return self._ctf

    @ctf.setter
    def ctf(self, new_ctf: CTF):
        self._ctf = new_ctf.copy()
        self._ctf._accelerator = self._accelerator

    @property
    def array(self) -> np.ndarray:
        """
        Array representing the scattering matrix.
        """
        return self._array

    @property
    def k(self) -> np.ndarray:
        """
        The spatial frequencies of each wave in the plane wave expansion.
        """
        return self._k

    @property
    def expansion_cutoff(self) -> float:
        """
        Expansion cutoff.
        """
        return self._expansion_cutoff

    @property
    def interpolation(self) -> int:
        """
        Interpolation factor.
        """
        return self._interpolation

    @property
    def interpolated_grid(self) -> Grid:
        """
        The grid of the interpolated scattering matrix.
        """
        interpolated_gpts = tuple(n // self.interpolation for n in self.gpts)
        return Grid(gpts=interpolated_gpts, sampling=self.sampling, lock_gpts=True)

    def _evaluate_ctf(self):
        xp = get_array_module(self._array)
        alpha = xp.sqrt(self.k[:, 0] ** 2 + self.k[:, 1] ** 2) * self.wavelength
        phi = xp.arctan2(self.k[:, 0], self.k[:, 1])
        return self._ctf.evaluate(alpha, phi)

    def __len__(self) -> int:
        """
        Number of plane waves in expansion.
        """
        return len(self._array)

    def _generate_partial(self, max_batch: int = None, pbar: bool = True):
        if max_batch is None:
            n_batches = 1
        else:
            n_batches = (len(self) + (-len(self) % max_batch)) // max_batch

        batch_pbar = ProgressBar(total=len(self), desc='Plane waves', disable=(not pbar) or (n_batches == 1))
        batch_sizes = split_integer(len(self), n_batches)

        N = 0
        for batch_size in batch_sizes:
            start = N
            end = N + batch_size
            yield start, end, Waves(copy_to_device(self._array[start:end], self._device), extent=self.extent,
                                    energy=self.energy)
            N += batch_size
            batch_pbar.update(batch_size)

        batch_pbar.refresh()
        batch_pbar.close()

    def _max_batch_expansion(self):
        memory_per_wave = 2 * 4 * np.prod(self.gpts)
        available_memory = .5 * get_available_memory(self._device)
        return min(int(available_memory / memory_per_wave), len(self))

    def _max_batch_probes(self):
        max_batch_plane_waves = self._max_batch_expansion()
        memory_per_wave = 2 * 4 * np.prod(self.interpolated_grid.gpts)
        memory_per_plane_wave_batch = 2 * 4 * np.prod(self.gpts) * max_batch_plane_waves
        available_memory = .4 * get_available_memory(self._device) - memory_per_plane_wave_batch
        return max(min(int(available_memory / memory_per_wave), 1024), 1)

    def multislice(self,
                   potential: AbstractPotential,
                   max_batch=None,
                   multislice_pbar: Union[ProgressBar, bool] = True,
                   plane_waves_pbar: Union[ProgressBar, bool] = True):
        """
        Propagate the scattering matrix through the provided potential.

        Parameters
        ----------
        positions: Array of xy-positions
            Positions of the probe wave functions
        max_batch: int
            The probe batch size. Larger batches are faster, but require more memory.
        pbar: bool
            If true, display progress bars.

        Returns
        -------
        Waves object.
            Probe exit wave functions for the provided positions.
        """

        if not isinstance(max_batch, int):
            max_batch = self._max_batch_expansion()

        propagator = FresnelPropagator()

        storage = get_array_module(self._array)

        if isinstance(multislice_pbar, bool):
            multislice_pbar = ProgressBar(total=len(potential), desc='Multislice', disable=not multislice_pbar)

        for start, end, partial_s_matrix in self._generate_partial(max_batch, pbar=plane_waves_pbar):
            _multislice(partial_s_matrix, potential, propagator=propagator, pbar=multislice_pbar)
            self._array[start: end] = copy_to_device(partial_s_matrix.array, storage)

        multislice_pbar.close()
        return self

    def collapse(self, positions: Sequence[float], max_batch_expansion: int = None) -> Waves:
        """
        Collapse the scattering matrix to probe wave functions centered on the provided positions.

        Parameters
        ----------
        positions: List of xy-positions
            The positions of the probe wave functions.
        max_batch_expansion: int, optional
            The maximum number of plane waves the reduction is applied to simultanously.

        Returns
        -------
        Wave object
            Probe wave functions for the provided positions.
        """
        xp = get_array_module(self.array)
        complex_exponential = get_device_function(xp, 'complex_exponential')
        scale_reduce = get_device_function(xp, 'scale_reduce')
        windowed_scale_reduce = get_device_function(xp, 'windowed_scale_reduce')

        positions = np.array(positions, dtype=xp.float32)

        if positions.shape == (2,):
            positions = positions[None]
        elif (len(positions.shape) != 2) or (positions.shape[-1] != 2):
            raise RuntimeError()

        interpolated_grid = self.interpolated_grid
        W = np.floor_divide(interpolated_grid.gpts, 2)
        corners = np.rint(positions / self.sampling - W).astype(np.int)
        corners = np.asarray(corners, dtype=xp.int)
        corners = np.remainder(corners, np.asarray(self.gpts))
        corners = xp.asarray(corners)

        window = xp.zeros((len(positions), interpolated_grid.gpts[0], interpolated_grid.gpts[1],), dtype=xp.complex64)

        positions = xp.asarray(positions)
        k = xp.asarray(self.k)
        translation = (complex_exponential(2. * np.pi * k[:, 0][None] * positions[:, 0, None]) *
                       complex_exponential(2. * np.pi * k[:, 1][None] * positions[:, 1, None]))

        coefficients = translation * self._evaluate_ctf()

        for start, end, partial_s_matrix in self._generate_partial(max_batch_expansion, pbar=False):
            partial_coefficients = coefficients[:, start:end]

            if self.interpolation > 1:
                windowed_scale_reduce(window, partial_s_matrix.array, corners, partial_coefficients)
            else:
                scale_reduce(window, partial_s_matrix.array, partial_coefficients)

        return Waves(window, extent=interpolated_grid.extent, energy=self.energy)

    def _generate_probes(self, scan: AbstractScan, max_batch_probes, max_batch_expansion):

        if not isinstance(max_batch_expansion, int):
            max_batch_expansion = self._max_batch_expansion()

        if not isinstance(max_batch_probes, int):
            max_batch_probes = self._max_batch_probes()

        for start, end, positions in scan.generate_positions(max_batch=max_batch_probes):
            yield start, end, self.collapse(positions, max_batch_expansion=max_batch_expansion)

    def scan(self,
             scan: AbstractScan,
             detectors: Sequence[AbstractDetector],
             max_batch_probes=None,
             max_batch_expansion=None,
             pbar: Union[ProgressBar, bool] = True):

        """
        Raster scan the probe across the potential and record a measurement for each detector.

        Parameters
        ----------
        scan: Scan object
            Scan defining the positions of the probe wave functions.
        detectors: List of Detector objects
            The detectors recording the measurements.
        potential:
            The potential to scan the probe over.
        max_batch_probes: int
            The probe batch size. Larger batches are faster, but require more memory.
        max_batch_expansion: int
            The expansion plane wave batch size.
        pbar: bool
            If true, display progress bars.

        Returns
        -------
        dict
            Dictionary of measurements with keys given by the detector.
        """

        measurements = {}
        for detector in detectors:
            measurements[detector] = detector.allocate_measurement(self.interpolated_grid, self.wavelength, scan)

        if isinstance(pbar, bool):
            pbar = ProgressBar(total=len(scan), desc='Scan', disable=not pbar)

        for start, end, exit_probes in self._generate_probes(scan, max_batch_probes, max_batch_expansion):
            for detector, measurement in measurements.items():
                scan.insert_new_measurement(measurement, start, end, detector.detect(exit_probes))
            pbar.update(end - start)

        pbar.refresh()
        pbar.close()
        return measurements

    def show_profile(self, **kwargs):
        """
        Show the profile of the probe wave function.

        Parameters
        ----------
        kwargs:
            Additional keyword arguments for the abtem.plot.show_line function.
        """

    def show(self, **kwargs):
        """
        Show the probe wave function.

        Parameters
        ----------
        kwargs:
            Additional keyword arguments for the abtem.plot.show_image function.
        """
        measurement = self.collapse((self.extent[0] / 2, self.extent[1] / 2)).intensity()
        measurement.show(**kwargs)

    def __copy__(self):
        return self.__class__(array=self.array.copy(),
                              expansion_cutoff=self._expansion_cutoff,
                              interpolation=self.interpolation,
                              k=self.k.copy(),
                              ctf=self.ctf,
                              extent=self.extent,
                              sampling=self.sampling,
                              energy=self.energy,
                              device=self.device)

    def copy(self):
        """
        Make a copy.
        """
        return copy(self)


class SMatrix(HasGridAndAcceleratorMixin, HasDeviceMixin):
    """
    Scattering matrix builder class

    The scattering matrix builder object is used for creating scattering matrices and simulating STEM experiments using
    the PRISM algorithm.

    Parameters
    ----------
    expansion_cutoff: float
        The angular cutoff of the plane wave expansion [mrad].
    interpolation: ont or two int
        Interpolation factor.
    ctf: CTF object
        The probe contrast transfer function.
    extent: one or two float
        Lateral extent of wave functions [Å].
    gpts: one or two int
        Number of grid points describing the wave functions.
    sampling: one or two float
        Lateral sampling of wave functions [1 / Å].
    energy: float
        Electron energy [eV].
    device: str
        The calculations will be carried out on this device.
    storage: str
        The scattering matrix will be stored on this device.
    kwargs:
        The parameters of a new CTF object as keyword arguments.
    """

    def __init__(self,
                 expansion_cutoff: float,
                 interpolation: int = 1,
                 ctf: CTF = None,
                 extent: Union[float, Sequence[float]] = None,
                 gpts: Union[int, Sequence[int]] = None,
                 sampling: Union[float, Sequence[float]] = None,
                 energy: float = None,
                 device: str = 'cpu',
                 storage: str = None,
                 **kwargs):

        if not isinstance(interpolation, int):
            raise ValueError('Interpolation factor must be int')

        self._interpolation = interpolation
        self._expansion_cutoff = expansion_cutoff

        if ctf is None:
            self._ctf = CTF(**kwargs)
        else:
            self._ctf = ctf

        self._grid = Grid(extent=extent, gpts=gpts, sampling=sampling)
        self._accelerator = Accelerator(energy=energy)

        self._device = device

        if storage is None:
            storage = device

        self._storage = storage

    @property
    def ctf(self):
        """
        The contrast transfer function of the probes.
        """
        return self._ctf

    @ctf.setter
    def ctf(self, value):
        self._ctf = value

    @property
    def expansion_cutoff(self) -> float:
        """
        Plane wave expansion cutoff.
        """
        return self._expansion_cutoff

    @expansion_cutoff.setter
    def expansion_cutoff(self, value: float):
        self._expansion_cutoff = value

    @property
    def interpolation(self) -> int:
        """
        Interpolation factor.
        """
        return self._interpolation

    @interpolation.setter
    def interpolation(self, value: int):
        self._interpolation = value

    @property
    def interpolated_grid(self) -> Grid:
        """
        The grid of the interpolated probe wave functions.
        """
        interpolated_gpts = tuple(n // self.interpolation for n in self.gpts)
        return Grid(gpts=interpolated_gpts, sampling=self.sampling, lock_gpts=True)

    def _generate_tds_probes(self,
                             scan: AbstractScan,
                             potential: AbstractTDSPotentialBuilder,
                             max_batch_probes: int,
                             max_batch_expansion: int,
                             potential_pbar: Union[ProgressBar, bool] = True,
                             multislice_pbar: Union[ProgressBar, bool] = True):

        if isinstance(potential_pbar, bool):
            potential_pbar = ProgressBar(total=len(potential), desc='Potential', disable=not potential_pbar)

        if isinstance(multislice_pbar, bool):
            multislice_pbar = ProgressBar(total=len(potential), desc='Multislice', disable=not multislice_pbar)

        for potential_config in potential.generate_frozen_phonon_potentials(pbar=potential_pbar):
            S = self.multislice(potential_config, max_batch=max_batch_expansion, pbar=multislice_pbar)
            yield S._generate_probes(scan, max_batch_probes, max_batch_expansion)

        multislice_pbar.refresh()
        multislice_pbar.close()

        potential_pbar.refresh()
        potential_pbar.close()

    def multislice(self, potential: AbstractPotential, max_batch: int = None,
                   pbar: Union[ProgressBar, bool] = True):
        """
        Build scattering matrix and propagate the scattering matrix through the provided potential.

        Parameters
        ----------
        positions: Array of xy-positions
            Positions of the probe wave functions
        max_batch: int, optional
            The probe batch size. Larger batches are faster, but require more memory.
        pbar: bool
            If true, display progress bars.

        Returns
        -------
        Waves object
            Probe exit wave functions as a Waves object.
        """
        self.grid.match(potential)
        return self.build().multislice(potential, max_batch=max_batch, multislice_pbar=pbar, plane_waves_pbar=pbar)

    def scan(self,
             scan: AbstractScan,
             detectors: Sequence[AbstractDetector],
             potential: Union[Atoms, AbstractPotential],
             max_batch_probes: int = None,
             max_batch_expansion: int = None,
             pbar: bool = True):
        """
        Build the scattering matrix. Raster scan the probe across the potential and record a measurement for each detector.

        Parameters
        ----------
        scan: Scan object
            Scan defining the positions of the probe wave functions.
        detectors: List of Detector objects
            The detectors recording the measurements.
        potential:
            The potential to scan the probe over.
        max_batch_probes: int
            The probe batch size. Larger batches are faster, but require more memory.
        max_batch_expansion: int
            The expansion plane wave batch size.
        pbar: bool
            If true, display progress bars.

        Returns
        -------
        dict
            Dictionary of measurements with keys given by the detector.
        """
        self.grid.match(potential.grid)
        self.grid.check_is_defined()

        measurements = {}
        for detector in detectors:
            measurements[detector] = detector.allocate_measurement(self.interpolated_grid, self.wavelength, scan)

        if isinstance(potential, AbstractTDSPotentialBuilder):
            probe_generators = self._generate_tds_probes(scan,
                                                         potential,
                                                         max_batch_probes=max_batch_probes,
                                                         max_batch_expansion=max_batch_expansion,
                                                         potential_pbar=pbar,
                                                         multislice_pbar=pbar)
        else:
            if isinstance(potential, AbstractPotentialBuilder):
                potential = potential.build(pbar=True)

            S = self.multislice(potential, max_batch=max_batch_expansion, pbar=pbar)
            probe_generators = [S._generate_probes(scan,
                                                   max_batch_probes=max_batch_probes,
                                                   max_batch_expansion=max_batch_expansion)]

        if isinstance(potential, AbstractTDSPotentialBuilder):
            tds_bar = ProgressBar(total=len(potential.frozen_phonons), desc='TDS',
                                  disable=(not pbar) or (len(potential.frozen_phonons) == 1))
        else:
            tds_bar = None

        scan_bar = ProgressBar(total=len(scan), desc='Scan', disable=not pbar)

        for probe_generator in probe_generators:
            scan_bar.reset()

            for start, end, exit_probes in probe_generator:
                for detector, measurement in measurements.items():
                    new_measurement = detector.detect(exit_probes)

                    if isinstance(potential, AbstractTDSPotentialBuilder):
                        # TODO : this should be more efficient
                        new_measurement /= len(potential.frozen_phonons)

                    scan.insert_new_measurement(measurement, start, end, new_measurement)

                scan_bar.update(end - start)

            scan_bar.refresh()
            if tds_bar:
                tds_bar.update(1)

        scan_bar.close()

        if tds_bar:
            tds_bar.refresh()
            tds_bar.close()

        return measurements

    def build(self) -> SMatrixArray:
        """
        Build the scattering matrix.
        """

        self.grid.check_is_defined()
        self.accelerator.check_is_defined()

        xp = get_array_module_from_device(self._device)
        storage_xp = get_array_module_from_device(self._storage)
        complex_exponential = get_device_function(xp, 'complex_exponential')

        n_max = int(
            xp.ceil(self.expansion_cutoff / 1000. / (self.wavelength / self.extent[0] * self.interpolation)))
        m_max = int(
            xp.ceil(self.expansion_cutoff / 1000. / (self.wavelength / self.extent[1] * self.interpolation)))

        n = xp.arange(-n_max, n_max + 1, dtype=xp.float32)
        w = xp.asarray(self.extent[0], dtype=xp.float32)
        m = xp.arange(-m_max, m_max + 1, dtype=xp.float32)
        h = xp.asarray(self.extent[1], dtype=xp.float32)

        kx = n / w * xp.float32(self.interpolation)
        ky = m / h * xp.float32(self.interpolation)

        mask = kx[:, None] ** 2 + ky[None, :] ** 2 < (self.expansion_cutoff / 1000. / self.wavelength) ** 2
        kx, ky = xp.meshgrid(kx, ky, indexing='ij')
        kx = kx[mask]
        ky = ky[mask]

        x, y = coordinates(extent=self.extent, gpts=self.gpts, endpoint=self.grid.endpoint)
        x = xp.asarray(x)
        y = xp.asarray(y)

        array = storage_xp.zeros((len(kx),) + (self.gpts[0], self.gpts[1]), dtype=np.complex64)

        for i in range(len(kx)):
            array[i] = copy_to_device(complex_exponential(-2 * np.pi * kx[i, None, None] * x[:, None]) *
                                      complex_exponential(-2 * np.pi * ky[i, None, None] * y[None, :]),
                                      self._storage)

        k = xp.asarray((kx, ky)).T

        return SMatrixArray(array,
                            expansion_cutoff=self.expansion_cutoff,
                            interpolation=self.interpolation,
                            extent=self.extent,
                            energy=self.energy,
                            k=k,
                            ctf=self.ctf,
                            device=self._device)

    def show_profile(self, **kwargs):
        """
        Show the profile of the probe wave function.

        Parameters
        ----------
        kwargs:
            Additional keyword arguments for the abtem.plot.show_line function.
        """
        self.build().show_profile(**kwargs)

    def show(self, **kwargs):
        """
        Show the probe wave function.

        Parameters
        ----------
        kwargs:
            Additional keyword arguments for the abtem.plot.show_image function.
        """
        self.build().show(**kwargs)

    def __copy__(self):
        return self.__class__(expansion_cutoff=self.expansion_cutoff,
                              interpolation=self.interpolation,
                              ctf=copy(self.ctf),
                              extent=self.extent,
                              gpts=self.gpts,
                              energy=self.energy,
                              device=self._device,
                              storage=self._storage)

    def copy(self):
        """
        Make a copy.
        """
        return copy(self)
