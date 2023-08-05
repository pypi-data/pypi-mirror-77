import pandas

from simses.analysis.data.data import Data
from simses.commons.state.technology.fuel_cell_state import FuelCellState
from simses.config.simulation.general_config import GeneralSimulationConfig


class FuelCellData(Data):

    def __init__(self, config: GeneralSimulationConfig, data: pandas.DataFrame):
        super().__init__(config, data)
        self.__config = config

    @property
    def id(self) -> str:
        return str(int(self._get_first_value(FuelCellState.SYSTEM_AC_ID))) + '.' + \
               str(int(self._get_first_value(FuelCellState.SYSTEM_DC_ID)))

    @property
    def time(self):
        return self._get_data(FuelCellState.TIME)

    @property
    def power(self):
        return self._get_data(FuelCellState.POWER)

    @property
    def dc_power(self):
        return self.power

    @property
    def energy_difference(self):
        pass

    @property
    def soc(self):
        pass

    @property
    def capacity(self):
        pass

    @property
    def storage_fulfillment(self):
        return self._get_data(FuelCellState.FULFILLMENT)

    @property
    def current(self):
        return self._get_data(FuelCellState.CURRENT)

    @property
    def current_density(self):
        return self._get_data(FuelCellState.CURRENT_DENSITY)

    @property
    def pressure_anode(self):
        return self._get_data(FuelCellState.PRESSURE_ANODE)

    @property
    def pressure_cathode(self):
        return self._get_data(FuelCellState.PRESSURE_CATHODE)

    @property
    def temperature(self):
        return self._get_data(FuelCellState.TEMPERATURE)

    @classmethod
    def get_system_data(cls, path: str, config: GeneralSimulationConfig) -> list:
        system_data: [pandas.DataFrame] = cls._get_system_data_for(path, FuelCellState, FuelCellState.TIME,
                                                                   FuelCellState.SYSTEM_AC_ID,
                                                                   FuelCellState.SYSTEM_DC_ID)
        res: [FuelCellData] = list()
        for data in system_data:
            res.append(FuelCellData(config, data))
        return res
