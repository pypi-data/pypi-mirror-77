from abc import abstractmethod, ABC

from simses.commons.state.state import State
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary


class SystemThermalModel(ABC):
    """Thermal model of a sorage system"""

    def __init__(self):
        # Air parameters
        self.air_pressure = 1 * 10 ** 5  # Pa, change if container is pressurized
        self.universal_gas_constant = 8.314  # J/kgK
        self.molecular_weight_air = 28.965 * 10 ** -3  # kg/mol

    @abstractmethod
    def get_temperature(self) -> float:
        """
        Returns the current temperature of the system

        Parameters
        -------

        Returns
        -------
        float
            system temperature in Kelvin
        """

        pass

    # @abstractmethod
    # def get_air_mass(self) -> float:
    #     pass
    #
    # @abstractmethod
    # def get_air_specific_heat(self) -> float:
    #     pass

    @abstractmethod
    def get_auxiliaries(self) -> [Auxiliary]:
        pass

    @abstractmethod
    def update_air_parameters(self):
        pass

    @abstractmethod
    def calculate_temperature(self, time: float, state: State) -> None:
        """
        Calcualtes the current temperature of the system

        Parameters
        ----------
        time : current simulation time
        state : current system state

        Returns
        -------

        """
        pass

    def close(self):
        """
        Closing all open resources in system thermal model

        Parameters
        ----------

        Returns
        -------

        """
        pass
