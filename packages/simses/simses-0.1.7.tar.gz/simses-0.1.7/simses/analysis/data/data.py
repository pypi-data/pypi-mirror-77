from abc import ABC, abstractmethod
from datetime import datetime

import numpy
import pandas

from simses.analysis.utils import get_mean_for, get_positive_values_from, get_sum_for, get_negative_values_from, \
    get_min_for, get_max_for
from simses.commons.data.csv_data_handler import CSVDataHandler
from simses.commons.log import Logger
from simses.config.simulation.general_config import GeneralSimulationConfig


class Data(ABC):

    __log: Logger = Logger(__name__)

    def __init__(self, config: GeneralSimulationConfig, data: pandas.DataFrame):
        self.__W_to_kWh = config.timestep / 3600 / 1000
        self.__data: pandas.DataFrame = data

    @property
    def convert_watt_to_kWh(self) -> float:
        """
        conversion coefficient in order to transform power in W to energy in kWh

        Returns
        -------
        float:
            conversion coefficient
        """
        return self.__W_to_kWh

    def _get_data(self, key: str) -> numpy.ndarray:
        """
        Returns data series for key as numpy array

        Parameters
        ----------
        key :

        Returns
        -------

        """
        return self.__data[key].to_numpy()

    def _get_first_value(self, key: str) -> float:
        """
        Returns fist value for data series of key

        Parameters
        ----------
        key :

        Returns
        -------

        """
        return float(self._get_data(key)[0])

    def _get_last_value(self, key: str) -> float:
        """
        Returns last value for data series of key

        Parameters
        ----------
        key :

        Returns
        -------

        """
        return float(self._get_data(key)[-1])

    def _get_difference(self, key: str) -> float:
        """

        Parameters
        ----------
        key :

        Returns
        -------

        """
        return self._get_last_value(key) - self._get_first_value(key)

    @property
    @abstractmethod
    def id(self) -> str:
        """

        Returns
        -------
        str:
            Data id as string
        """
        pass

    @property
    @abstractmethod
    def time(self):
        """
        Time series in s

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def power(self):
        """
        Series of power values in W

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def dc_power(self):
        """
        Series of power values in W

        Returns
        -------

        """
        pass

    @property
    def average_power(self) -> float:
        """
        Mean value of power series in W

        Returns
        -------

        """
        return get_mean_for(self.power)

    @property
    def charge_energy(self) -> float:
        """
        Charge energy in kWh (as positive values)

        Returns
        -------

        """
        return get_sum_for(self.charge_energy_series)

    @property
    def charge_energy_series(self) -> numpy.ndarray:
        """
        Series of charge energy in kWh (as positive values)

        Returns
        -------

        """
        return get_positive_values_from(self.power) * self.__W_to_kWh

    @property
    def discharge_energy(self) -> float:
        """
        Discharge energy in kWh (as positive values)

        Returns
        -------

        """
        return get_sum_for(self.discharge_energy_series)

    @property
    def discharge_energy_series(self) -> numpy.ndarray:
        """
        Series of discharge energy in kWh (as positive values)

        Returns
        -------

        """
        return -1 * get_negative_values_from(self.power) * self.__W_to_kWh

    @property
    def discharge_energy_per_year(self) -> numpy.ndarray:
        """
        Series of yearly discharge energy in kWh (as positive values)

        Returns
        -------

        """
        return self.__energy_per_year(self.discharge_energy_series)

    @property
    def charge_energy_per_year(self) -> numpy.ndarray:
        """
        Series of yearly charge energy in kWh (as positive values)

        Returns
        -------

        """
        return self.__energy_per_year(self.charge_energy_series)

    def __energy_per_year(self, energy: numpy.ndarray) -> numpy.ndarray:
        time: numpy.ndarray = self.time
        energy: numpy.ndarray = numpy.column_stack([time, energy])
        start: float = time[0]
        end: float = time[-1]
        slice_start: float = start
        energy_per_year: list = list()
        while slice_start <= end:
            date = datetime.fromtimestamp(slice_start)
            slice_end: float = date.replace(year=date.year + 1).timestamp()
            # 0: Column index for time series, 1: Column index for energy series
            yearly_energy = energy[numpy.where((energy[:, 0] >= slice_start) * (energy[:, 0] < slice_end))]
            energy_per_year.append(yearly_energy[:, 1].sum())
            slice_start = slice_end
        return numpy.array(energy_per_year)

    @property
    @abstractmethod
    def energy_difference(self):
        """
        Energy difference of start and end point in kWh

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def soc(self):
        """
        Series of soc values in p.u.

        Returns
        -------

        """
        pass


    @property
    def average_soc(self):
        """
        Mean soc in p.u.

        Returns
        -------

        """
        return get_mean_for(self.soc)

    @property
    def max_soc(self):
        """
        Maximal soc of series in p.u.

        Returns
        -------

        """
        return get_max_for(self.soc)

    @property
    def min_soc(self):
        """
        Minimum soc of series in p.u.

        Returns
        -------

        """
        return get_min_for(self.soc)

    @property
    @abstractmethod
    def capacity(self):
        """
        Series of capacity in kWh

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def storage_fulfillment(self):
        """
        Percentage of time the system or battery can fulfill the desired power

        Returns
        -------

        """
        pass

    @property
    def initial_capacity(self):
        """
        First value of capacity series in kWh

        Returns
        -------

        """
        return self.capacity[0]

    @classmethod
    @abstractmethod
    def get_system_data(cls, path: str, config: GeneralSimulationConfig) -> list:
        """
        Extracts unique systems data from storage data files in path

        Parameters
        ----------
        path : value folder
        config : simulation data_config in value folder

        Returns
        -------

        """
        pass

    @classmethod
    def _get_system_data_for(cls, path, state_cls, time_key: str, system_key: str = None, storage_key: str = None) -> [pandas.DataFrame]:
        """
        Extracts unique systems from storage data files

        Parameters
        ----------
        path : value folder
        state_cls : storage data state class
        system_key : Key for system id of storage data state class
        storage_key : Key for storage id of storage data state class
        time_key : Key for time of storage data state class

        Returns
        -------
            List of device data
        """
        # data_import: DataImport = DataImport(path, state_cls)
        # data: pandas.DataFrame = data_import.return_data()
        try:
            data: pandas.DataFrame = CSVDataHandler.get_data_from(path, state_cls)
            # return data without id selection
            if system_key is None or storage_key is None:
                data.sort_values(by=[time_key], inplace=True)
                return [data]
            # get unique systems
            systems: pandas.DataFrame = data[[system_key, storage_key]].copy()
            systems.drop_duplicates(inplace=True)
            # get data for unique systems
            res: [pandas.DataFrame] = list()
            for row in range(len(systems.index)):
                system = systems.iloc[row]
                system_id = system[system_key]
                storage_id = system[storage_key]
                system_data: pandas.DataFrame = data.loc[
                    (data[system_key] == system_id) & (data[storage_key] == storage_id)].copy()
                system_data.sort_values(by=[system_key, storage_key, time_key], inplace=True)
                if system_data.isna().values.any():
                    cls.__log.error('Data with system id ' + str(int(system_id)) + ' and storage id '
                                    + str(int(storage_id)) + ' has NaN values! This data will be neglected for analysis!')
                else:
                    res.append(system_data)
            return res
        except FileNotFoundError:
            cls.__log.warn('File could not be found for ' + path + state_cls.__name__)
            return list()

    @classmethod
    def close(cls):
        cls.__log.close()
