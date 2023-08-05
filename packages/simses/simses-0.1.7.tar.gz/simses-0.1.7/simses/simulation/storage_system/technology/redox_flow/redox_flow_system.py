from configparser import ConfigParser

from simses.commons.data.data_handler import DataHandler
from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary
from simses.simulation.storage_system.technology.redox_flow.battery_management_system.battery_management_system import \
    BatteryManagementSystem
from simses.simulation.storage_system.technology.redox_flow.degradation_model.capacity_degradation_model import \
    CapacityDegradationModel
from simses.simulation.storage_system.technology.redox_flow.electrolyte_system.electrolyte_system import \
    ElectrolyteSystem
from simses.simulation.storage_system.technology.redox_flow.pump_algorithm.pump_algorithm import PumpAlgorithm
from simses.simulation.storage_system.technology.redox_flow.redox_flow_factory import RedoxFlowFactory
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule
from simses.simulation.storage_system.technology.technology import StorageTechnology
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class RedoxFlow(StorageTechnology):
    """The RedoxFlow Class updates the electrochemical model, which includes the battery management system, the
    hydraulic model and the electrolyte model (for the capacity determination)"""

    def __init__(self, stack_type, pump_type, eta_pump, power, voltage, capacity,
                 ambient_thermal_model: AmbientThermalModel, pump_algorithm, degradation_model,
                 data_export: DataHandler, storage_id: int, system_id: int, config: ConfigParser):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__factory: RedoxFlowFactory = RedoxFlowFactory(config)
        self.__max_power = power
        self.__stack_module: StackModule = self.__factory.create_stack_module(stack_type, voltage, power)
        self.__capacity_degradation_model: CapacityDegradationModel = self.__factory.create_degradation_model(
            self.__stack_module, degradation_model)
        self.__electrolyte_system: ElectrolyteSystem = self.__factory.create_electrolyte_system(
            capacity, self.__capacity_degradation_model)
        battery_management_system: BatteryManagementSystem = self.__factory.create_battery_management_system(
            self.__stack_module)
        self.__redox_flow_state: RedoxFlowState = self.__factory.create_redox_flow_state_from(storage_id, system_id,
                                                                                              ambient_thermal_model,
                                                                                              self.__stack_module,
                                                                                              self.__electrolyte_system)
        self.__pump = self.__factory.create_pumps(eta_pump, pump_type)
        self.__pump_algorithm: PumpAlgorithm = self.__factory.create_pump_algorithm(self.__pump, self.__stack_module,
                                                                                    pump_algorithm)
        self.__electrochemical_model = self.__factory.create_electrochemical_model(self.__stack_module,
                                                                                   battery_management_system,
                                                                                   self.__electrolyte_system)
        self.__capacity_degradation_model = self.__factory.create_degradation_model(self.__stack_module,
                                                                                    degradation_model)
        self.__time = self.__redox_flow_state.time
        self.__data_export: DataHandler = data_export
        self.__data_export.transfer_data(self.__redox_flow_state.to_export())

    def update(self):
        """
        Starts updating the calculation for the electrochemical model of the redox flow battery, which includes the
        battery management system requests.

        Returns
        -------
            None

        """
        rfbs = self.__redox_flow_state
        time = self.__time
        power_target = rfbs.power
        self.__electrochemical_model.update(time, rfbs, power_target)
        self.__pump_algorithm.update(rfbs)
        self.__electrolyte_system.update(time, rfbs)
        rfbs.time = time
        self.__data_export.transfer_data(rfbs.to_export())

    def set(self, time: float, current: float, voltage: float):
        """
        Sets the new simulation time an sets the power (current * voltage) of the RedoxFlowState for the next simulation
        time step.

        Parameters
        ----------
        time : float
            current time of the simulation
        current : float
            target current in A
        voltage : float
            target voltage in V

        Returns
        -------
            None
        """
        self.__time = time
        self.__redox_flow_state.power = current * voltage

    def distribute_and_run(self, time: float, current: float, voltage: float):
        self.set(time, current, voltage)
        self.update()

    @property
    def volume(self) -> float:
        return 0

    @property
    def mass(self) -> float:
        return 0

    @property
    def surface_area(self) -> float:
        return 0

    @property
    def specific_heat(self) -> float:
        """
               Specific heat of storage technology in J/(kgK)

               Returns
               -------

               """
        return 0

    @property
    def convection_coefficient(self) -> float:
        """
                determines the convective heat transfer coefficient of a battery cell

                Returns
                -------
                float:
                    convective heat transfer coefficient in W/(m^2*K)
                """
        return 0

    def wait(self):
        pass

    def get_auxiliaries(self) -> [Auxiliary]:
        return [self.__pump]

    @property
    def state(self) -> RedoxFlowState:
        return self.__redox_flow_state

    def get_system_parameters(self) -> dict:
        return dict()

    def close(self):
        """Closing all resources in redox_flow_system"""
        self.__log.close()
        self.__factory.close()
