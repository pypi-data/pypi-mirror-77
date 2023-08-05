from configparser import ConfigParser

from simses.commons.data.data_handler import DataHandler
from simses.commons.state.state import State
from simses.commons.state.system_parameters import SystemParameters
from simses.commons.state.system_state import SystemState
from simses.simulation.storage_system.control.equal_power_distributor import EqualPowerDistributor
from simses.simulation.storage_system.control.power_distributor import PowerDistributor
from simses.simulation.storage_system.storage_system_ac import StorageSystemAC
from simses.simulation.storage_system.storage_system_factory import StorageSystemFactory


class StorageCircuit:

    def __init__(self, data_export: DataHandler, config: ConfigParser):
        self.__factory: StorageSystemFactory = StorageSystemFactory(config)
        self.__storage_systems: [StorageSystemAC] = self.__factory.create_storage_systems_ac(data_export)
        self.__power_distributor: PowerDistributor = EqualPowerDistributor(len(self.__storage_systems))
        # self.__power_distributor: PowerDistributor = SocBasedPowerDistributor()

    def update(self, time: float, power: float) -> None:
        states: [State] = list()
        for system in self.__storage_systems:
            states.append(system.state)
        self.__power_distributor.set(states)
        for system in self.__storage_systems:
            local_power: float = self.__power_distributor.get_power_for(power, system.state)
            system.update(local_power, time)

    @property
    def state(self) -> SystemState:
        system_states = list()
        for storage in self.__storage_systems:
            system_states.append(storage.state)
        system_state = SystemState.sum_parallel(system_states)
        system_state.set(SystemState.SYSTEM_AC_ID, 0)
        system_state.set(SystemState.SYSTEM_DC_ID, 0)
        return system_state

    def get_system_parameters(self) -> dict:
        parameters: dict = dict()
        subsystems: list = list()
        for system in self.__storage_systems:
            subsystems.append(system.get_system_parameters())
        parameters[SystemParameters.POWER_DISTRIBUTION] = type(self.__power_distributor).__name__
        parameters[SystemParameters.SUBSYSTEM] = subsystems
        return {SystemParameters.PARAMETERS: parameters}

    def close(self) -> None:
        """Closing all resources in storage systems"""
        self.__factory.close()
        for storage in self.__storage_systems:
            storage.close()
