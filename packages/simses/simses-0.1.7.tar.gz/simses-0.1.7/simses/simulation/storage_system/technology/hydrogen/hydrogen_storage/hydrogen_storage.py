from abc import ABC, abstractmethod

from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.commons.state.technology.fuel_cell_state import FuelCellState
from simses.simulation.storage_system.auxiliary.compressor.hydrogen_isentrop_compressor import \
    HydrogenIsentropCompressor


class HydrogenStorage(ABC):

    __TEMPERATURE: float = 40  # C

    def __init__(self):
        super().__init__()
        self.__compressor = HydrogenIsentropCompressor()

    def update_from(self, time: float, electrolyzer_state: ElectrolyzerState, fuel_cell_state: FuelCellState) -> None:
        """

        Parameters
        ----------
        time :
        electrolyzer_state :
        fuel_cell_state :

        Returns
        -------

        """
        self.calculate_soc(time - electrolyzer_state.time, electrolyzer_state.hydrogen_production - fuel_cell_state.hydrogen_use)
        self.__compressor.calculate_compression_power(electrolyzer_state.hydrogen_outflow, electrolyzer_state.pressure_anode + 1,
                                                      self.get_tank_pressure(), self.__TEMPERATURE)
        electrolyzer_state.power_compressor = self.__compressor.get_compression_power()

    @abstractmethod
    def calculate_soc(self, time_diff: float, hydrogen_net_flow: float) -> None:
        pass

    @abstractmethod
    def get_soc(self) -> float:
        pass

    @abstractmethod
    def get_capacity(self) -> float:
        pass

    @abstractmethod
    def get_tank_pressure(self) -> float:
        pass

    def get_auxiliaries(self):
        return [self.__compressor]

    @abstractmethod
    def close(self) -> None:
        pass
