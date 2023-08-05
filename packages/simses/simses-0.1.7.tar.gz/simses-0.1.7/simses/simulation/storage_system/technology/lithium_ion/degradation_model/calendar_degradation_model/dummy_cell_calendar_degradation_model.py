import math

from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.config.simulation.battery_config import BatteryConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.calendar_degradation_model.calendar_degradation_model import \
    CalendarDegradationModel


class DummyCellCalendarDegradationModel(CalendarDegradationModel):

    def __init__(self, cell_type: CellType, battery_config: BatteryConfig):
        super().__init__(cell_type)
        self.__total_capacity_decrease = 0
        self.__capacity_decrease = 0
        self.__total_time_passed = 0

        self.__initial_capacity = self._cell.get_capacity()

        self.__end_of_life_duration = 5 * 365 * 24 * 60 * 60 # Sec till EOL (=xy%) is reached. 5 years in this case
        self.__end_of_life = battery_config.eol # EOL criteria xy%.

    def calculate_degradation(self, time: float, battery_state: LithiumIonState) -> None:
        # Calendar degradation in dummy cell is a function of sqrt(t)
        self.__total_time_passed += time - battery_state.time
        self.__capacity_decrease = math.sqrt(self.__total_time_passed) * (1 - self.__end_of_life) / \
                                   math.sqrt(self.__end_of_life_duration) # in p.u

        self.__capacity_decrease = self.__capacity_decrease * self.__initial_capacity

    def calculate_resistance_increase(self, time: float, battery_state: LithiumIonState) -> None:
        pass # No resistance increase in dummy cell model

    def get_degradation(self) -> float:
        degradation = self.__capacity_decrease - self.__total_capacity_decrease
        # Update total capacity decrease
        self.__total_capacity_decrease = self.__capacity_decrease
        return degradation

    def get_resistance_increase(self) -> float:
        return 0 # No resistance increase in dummy cell model

    def reset(self, battery_state: LithiumIonState) -> None:
        self.__capacity_decrease = 0
        self.__total_capacity_decrease = 0
        self.__total_time_passed = 0

    def close(self) -> None:
        pass
