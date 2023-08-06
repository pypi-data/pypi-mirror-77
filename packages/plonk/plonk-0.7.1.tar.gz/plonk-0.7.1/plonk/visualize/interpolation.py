"""Interpolation to a pixel grid.

There are two functions: one for interpolation of scalar fields, and one
for interpolation of vector fields.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

import numpy as np
from numpy import ndarray

from .._logging import logger
from ..utils.geometry import distance_from_plane
from .splash import interpolate_projection, interpolate_slice

if TYPE_CHECKING:
    from ..snap.snap import SnapLike

Extent = Tuple[float, float, float, float]


def interpolate(
    *,
    snap: SnapLike,
    quantity: str,
    x: str = 'x',
    y: str = 'y',
    interp: 'str',
    slice_normal: Tuple[float, float, float] = None,
    slice_offset: float = None,
    extent: Extent,
    **kwargs,
) -> ndarray:
    """Interpolate a quantity on the snapshot to a pixel grid.

    Parameters
    ----------
    snap
        The Snap (or SubSnap) object.
    quantity
        The quantity to visualize. Must be a string to pass to Snap,
    x
        The x-coordinate for the visualization. Must be a string to
        pass to Snap. Default is 'x'.
    y
        The y-coordinate for the visualization. Must be a string to
        pass to Snap. Default is 'y'.
    interp
        The interpolation type. Default is 'projection'.

        - 'projection' : 2d interpolation via projection to xy-plane
        - 'slice' : 3d interpolation via cross-section slice.
    slice_normal
        The normal vector to the plane in which to take the
        cross-section slice as an array (x, y, z).
    slice_offset
        The offset of the cross-section slice. Default is 0.0.
    extent
        The xy extent of the image as (xmin, xmax, ymin, ymax).
    **kwargs
        Additional keyword arguments to pass to scalar_interpolation
        and vector_interpolation.

    Returns
    -------
    ndarray
        The interpolated quantity on a pixel grid as an ndarray. The
        shape for scalar data is (npixx, npixy), and for vector is
        (2, npixx, npixy).

    Examples
    --------
    Interpolate density to grid.

    >>> grid_data = plonk.interpolate(
    ...     snap=snap,
    ...     quantity='density',
    ...     interp='projection',
    ...     extent=(-100, 100, -100, 100),
    ... )
    """
    _quantity, x, y, z = _get_arrays_from_str(snap=snap, quantity=quantity, x=x, y=y)
    h = snap.array_in_code_units('smoothing_length')
    m = snap.array_in_code_units('mass')

    if interp == 'projection':
        dist_from_slice = None
        if slice_normal is not None:
            logger.warning('ignoring slice_normal for projection')
        if slice_offset is not None:
            logger.warning('ignoring slice_offset for projection')
    elif interp == 'slice':
        if slice_offset is None:
            slice_offset = 0.0
        if slice_normal is None:
            slice_normal = np.array([0, 0, 1])
        dist_from_slice = distance_from_plane(x, y, z, slice_normal, slice_offset)

    if _quantity.ndim == 1:
        interpolated_data = scalar_interpolation(
            quantity=_quantity,
            x_coordinate=x,
            y_coordinate=y,
            dist_from_slice=dist_from_slice,
            extent=extent,
            smoothing_length=h,
            particle_mass=m,
            hfact=snap.properties['smoothing_length_factor'],
            **kwargs,
        )

    elif _quantity.ndim == 2:
        interpolated_data = vector_interpolation(
            quantity_x=_quantity[:, 0],
            quantity_y=_quantity[:, 1],
            x_coordinate=x,
            y_coordinate=y,
            dist_from_slice=dist_from_slice,
            extent=extent,
            smoothing_length=h,
            particle_mass=m,
            hfact=snap.properties['smoothing_length_factor'],
            **kwargs,
        )

    else:
        raise ValueError('quantity.ndim > 2: cannot determine quantity')

    return interpolated_data


def scalar_interpolation(
    *,
    quantity: ndarray,
    x_coordinate: ndarray,
    y_coordinate: ndarray,
    dist_from_slice: ndarray = None,
    extent: Extent,
    smoothing_length: ndarray,
    particle_mass: ndarray,
    hfact: float,
    number_of_pixels: Tuple[float, float] = (512, 512),
    density_weighted: bool = None,
) -> ndarray:
    """Interpolate scalar quantity to a pixel grid.

    Parameters
    ----------
    quantity
        A scalar quantity on the particles to interpolate.
    x_coordinate
        Particle coordinate for x-axis in interpolation.
    y_coordinate
        Particle coordinate for y-axis in interpolation.
    dist_from_slice
        The distance from the cross section slice. Only required for
        cross section interpolation.
    extent
        The range in the x- and y-direction as (xmin, xmax, ymin, ymax).
    smoothing_length
        The smoothing length on each particle.
    particle_mass
        The particle mass on each particle.
    hfact
        The smoothing length factor.
    number_of_pixels
        The pixel grid to interpolate the scalar quantity to, as
        (npixx, npixy).
    density_weighted
        Use density weighted interpolation. Default is off.

    Returns
    -------
    ndarray
        An array of scalar quantities interpolated to a pixel grid with
        shape (npixx, npixy).
    """
    return _interpolate(
        quantity=quantity,
        x_coordinate=x_coordinate,
        y_coordinate=y_coordinate,
        dist_from_slice=dist_from_slice,
        extent=extent,
        smoothing_length=smoothing_length,
        particle_mass=particle_mass,
        hfact=hfact,
        number_of_pixels=number_of_pixels,
        density_weighted=density_weighted,
    )


def vector_interpolation(
    *,
    quantity_x: ndarray,
    quantity_y: ndarray,
    x_coordinate: ndarray,
    y_coordinate: ndarray,
    dist_from_slice: ndarray = None,
    extent: Extent,
    smoothing_length: ndarray,
    particle_mass: ndarray,
    hfact: float,
    number_of_pixels: Tuple[float, float] = (512, 512),
    density_weighted: bool = None,
) -> ndarray:
    """Interpolate scalar quantity to a pixel grid.

    Parameters
    ----------
    quantity_x
        The x-component of a vector quantity to interpolate.
    quantity_y
        The y-component of a vector quantity to interpolate.
    x_coordinate
        Particle coordinate for x-axis in interpolation.
    y_coordinate
        Particle coordinate for y-axis in interpolation.
    dist_from_slice
        The distance from the cross section slice. Only required for
        cross section interpolation.
    extent
        The range in the x- and y-direction as (xmin, xmax, ymin, ymax).
    smoothing_length
        The smoothing length on each particle.
    particle_mass
        The particle mass on each particle.
    hfact
        The smoothing length factor.
    number_of_pixels
        The pixel grid to interpolate the scalar quantity to, as
        (npixx, npixy).
    density_weighted
        Use density weighted interpolation. Default is off.

    Returns
    -------
    ndarray
        An array of vector quantities interpolated to a pixel grid with
        shape (2, npixx, npixy).
    """
    vecsmoothx = _interpolate(
        quantity=quantity_x,
        x_coordinate=x_coordinate,
        y_coordinate=y_coordinate,
        dist_from_slice=dist_from_slice,
        extent=extent,
        smoothing_length=smoothing_length,
        particle_mass=particle_mass,
        hfact=hfact,
        number_of_pixels=number_of_pixels,
        density_weighted=density_weighted,
    )
    vecsmoothy = _interpolate(
        quantity=quantity_y,
        x_coordinate=x_coordinate,
        y_coordinate=y_coordinate,
        dist_from_slice=dist_from_slice,
        extent=extent,
        smoothing_length=smoothing_length,
        particle_mass=particle_mass,
        hfact=hfact,
        number_of_pixels=number_of_pixels,
        density_weighted=density_weighted,
    )
    return np.stack((np.array(vecsmoothx), np.array(vecsmoothy)))


def _interpolate(
    *,
    quantity: ndarray,
    x_coordinate: ndarray,
    y_coordinate: ndarray,
    dist_from_slice: ndarray = None,
    extent: Extent,
    smoothing_length: ndarray,
    particle_mass: ndarray,
    hfact: float,
    number_of_pixels: Tuple[float, float],
    density_weighted: bool = None,
) -> ndarray:
    if dist_from_slice is None:
        do_slice = False
    else:
        do_slice = True
    normalise = False
    if density_weighted is None:
        density_weighted = False
    if density_weighted:
        normalise = True

    npixx, npixy = number_of_pixels
    xmin, ymin = extent[0], extent[2]
    pixwidthx = (extent[1] - extent[0]) / npixx
    pixwidthy = (extent[3] - extent[2]) / npixy
    npart = len(smoothing_length)

    itype = np.ones(smoothing_length.shape)
    if density_weighted:
        weight = particle_mass / smoothing_length ** 3
    else:
        weight = hfact ** -3 * np.ones(smoothing_length.shape)

    if do_slice:
        interpolated_data = interpolate_slice(
            x=x_coordinate,
            y=y_coordinate,
            dslice=dist_from_slice,
            hh=smoothing_length,
            weight=weight,
            dat=quantity,
            itype=itype,
            npart=npart,
            xmin=xmin,
            ymin=ymin,
            npixx=npixx,
            npixy=npixy,
            pixwidthx=pixwidthx,
            pixwidthy=pixwidthy,
            normalise=normalise,
        )
    else:
        interpolated_data = interpolate_projection(
            x=x_coordinate,
            y=y_coordinate,
            hh=smoothing_length,
            weight=weight,
            dat=quantity,
            itype=itype,
            npart=npart,
            xmin=xmin,
            ymin=ymin,
            npixx=npixx,
            npixy=npixy,
            pixwidthx=pixwidthx,
            pixwidthy=pixwidthy,
            normalise=normalise,
        )

    return interpolated_data


def _get_arrays_from_str(*, snap, quantity, x, y):

    coords = {'x', 'y', 'z'}
    if x not in coords:
        raise ValueError('x-coordinate must be one of "x", "y", "z"')
    if y not in coords:
        raise ValueError('y-coordinate must be one of "x", "y", "z"')

    quantity_str, x_str, y_str = quantity, x, y
    z_str = coords.difference((x_str, y_str)).pop()

    quantity = snap.array_in_code_units(quantity_str)
    x = snap.array_in_code_units(x_str)
    y = snap.array_in_code_units(y_str)
    z = snap.array_in_code_units(z_str)

    if quantity.ndim > 2:
        raise ValueError('Cannot interpret quantity with ndim > 2')
    if quantity.ndim == 2:
        try:
            quantity_x = snap.array_in_code_units(quantity_str + '_' + x_str)
            quantity_y = snap.array_in_code_units(quantity_str + '_' + y_str)
            quantity = np.stack([quantity_x, quantity_y]).T
        except ValueError:
            raise ValueError(
                '2d quantity must be a vector quantity, e.g. "velocity".\n'
                'For dust quantities, try appending the dust species number,\n'
                'e.g. "dust_density_001".'
            )

    return quantity, x, y, z
