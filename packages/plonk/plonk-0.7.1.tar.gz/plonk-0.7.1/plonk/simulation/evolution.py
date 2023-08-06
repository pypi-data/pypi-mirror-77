"""Time series data for global or sink quantites.

This module contains a function for loading global quantities and sink
particle time series data typical of Phantom simulations. These files
track averaged quantities that are more frequently output than snapshot
files.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, List, Tuple, Union

from pandas import DataFrame

from ._phantom_evolution import evolution_units as evolution_units_phantom
from ._phantom_evolution import load_data_from_file as load_data_from_file_phantom

if TYPE_CHECKING:
    from .simulation import Simulation


def load_ev(
    filenames: Union[str, Path, Tuple[str], Tuple[Path], List[str], List[Path]],
    data_source: str = 'Phantom',
    config: Union[str, Path] = None,
) -> DataFrame:
    """Load time evolution data from file(s).

    Evolution files track global quantities, such as energy, momentum,
    and density, over time. The time increments in these files is
    smaller than the snapshot file output time. These files are
    typically stored as text files.

    The data is stored as a pandas DataFrame.

    Parameters
    ----------
    filename(s)
        Collection of paths to evolution file(s) in chronological order.
        These should all contain the same columns.
    data_source : optional
        The code used to produce the data. Default is 'Phantom'.
    config : optional
        The path to a Plonk config.toml file.

    Returns
    -------
    dataframe
        A pandas DataFrame with the time evolution data.

    Examples
    --------
    Reading a single evolution file into a pandas DataFrame.

    >>> file_name = 'simulation.ev'
    >>> ev = plonk.load_ev(file_name)

    Reading a collection of evolution files into a pandas DataFrame.

    >>> file_names = ('sim01.ev', 'sim02.ev', 'sim03.ev')
    >>> ev = plonk.load_ev(file_names)
    """
    if data_source == 'Phantom':
        return load_data_from_file_phantom(filenames=filenames, config=config)
    raise ValueError('Cannot determine code used to produce evolution data')


def evolution_units(
    sim: Simulation, data_source: str = 'Phantom', config: Union[str, Path] = None
):
    """Get units of time series data from Simulation object.

    Parameters
    ----------
    sim
        The Simulation object.
    data_source : optional
        The code used to produce the data. Default is 'Phantom'.
    config : optional
        The path to a Plonk config.toml file.

    Returns
    -------
    Dict
    """
    if data_source == 'Phantom':
        return evolution_units_phantom(sim=sim, config=config)
    raise ValueError('Cannot determine code used to produce evolution data')
