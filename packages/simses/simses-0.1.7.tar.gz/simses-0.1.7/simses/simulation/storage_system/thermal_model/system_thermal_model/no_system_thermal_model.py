import numpy

from simses.commons.state.system_state import SystemState
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel
from simses.simulation.storage_system.thermal_model.system_thermal_model.system_thermal_model import SystemThermalModel


class NoSystemThermalModel(SystemThermalModel):
    """This model does nothing - keeps the system air temperature equal to ambient temperature"""

    LARGE_NUMBER = numpy.finfo(numpy.float64).max * 1e-100

    def __init__(self, ambient_thermal_model: AmbientThermalModel, general_config: GeneralSimulationConfig):
        super().__init__()
        self.start_time = general_config.start
        self.__ambient_thermal_model = ambient_thermal_model
        self.__system_temperature = self.__ambient_thermal_model.get_initial_temperature()  # K
        self.__air_specific_heat = 1006  # J/kgK, cp (at constant pressure)
        # this is the internal air temperature within the container. Initialized with ambient temperature

    def calculate_temperature(self, time, state: SystemState):
        self.__system_temperature = self.__ambient_thermal_model.get_temperature(time)

    def get_auxiliaries(self) -> [Auxiliary]:
        return list()

    def get_temperature(self):
        return self.__system_temperature

    def update_air_parameters(self):
        pass

    # def get_air_mass(self) -> float:
    #     return self.LARGE_NUMBER
    #
    # def get_air_specific_heat(self) -> float:
    #     return self.__air_specific_heat
