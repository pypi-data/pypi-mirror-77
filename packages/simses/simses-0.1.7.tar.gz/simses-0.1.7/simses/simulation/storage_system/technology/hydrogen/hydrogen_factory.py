from configparser import ConfigParser

from simses.commons.log import Logger
from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.hydrogen_config import HydrogenConfig
from simses.simulation.storage_system.technology.hydrogen.control.management import HydrogenManagementSystem
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.hydrogen_storage import HydrogenStorage
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.pipeline.simple_pipeline import \
    SimplePipeline
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.pressuretank.pressuretank import PressureTank


class HydrogenFactory:

    def __init__(self, config: ConfigParser):
        self.__log: Logger = Logger(type(self).__name__)
        self.__config_general: GeneralSimulationConfig = GeneralSimulationConfig(config)
        self.__config_hydrogen: HydrogenConfig = HydrogenConfig(config)

    def create_hydrogen_state_from(self, system_id: int, storage_id: int) -> HydrogenState:
        hs = HydrogenState(system_id, storage_id)
        hs.time = self.__config_general.start
        return hs

    def create_hydrogen_management_system(self, electrolyzer_maximal_power: float, fuel_cell_maximal_power: float):
        return HydrogenManagementSystem(max_power_electrolyzer=electrolyzer_maximal_power,
                                        max_power_fuel_cell=fuel_cell_maximal_power, config=self.__config_hydrogen)

    def create_hydrogen_storage(self, storage: str, capacity: float, max_pressure: float) -> HydrogenStorage:
        soc: float = self.__config_hydrogen.soc
        if storage == PressureTank.__name__:  # name of the file in which object pressuretank is located
            self.__log.debug('Creating pressuretank as ' + storage)
            return PressureTank(capacity, max_pressure, soc)
        elif storage == SimplePipeline.__name__:
            self.__log.debug('Creating pipeline as ' + storage)
            return SimplePipeline(storage_pressure=max_pressure)
        else:
            options: [str] = list()
            options.append(PressureTank.__name__)
            options.append(SimplePipeline.__name__)
            raise Exception('Specified pressuretank ' + storage + ' is unknown. '
                            'Following options are available: ' + str(options))

    def close(self):
        self.__log.close()
