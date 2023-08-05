from simses.commons.log import Logger
from simses.commons.profile.technical_profile.frequency_profile import FrequencyProfile
from simses.commons.profile.technical_profile.technical_profile import TechnicalProfile
from simses.commons.state.energy_management_state import EnergyManagementState
from simses.commons.state.system_state import SystemState
from simses.config.simulation.energy_management_config import EnergyManagementConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.profile_config import ProfileConfig
from simses.simulation.energy_management.operation_strategy.operation_priority import OperationPriority
from simses.simulation.energy_management.operation_strategy.operation_strategy import OperationStrategy


class FcrOperationStrategy(OperationStrategy):

    def __init__(self, config: GeneralSimulationConfig, config_ems: EnergyManagementConfig, profile_config: ProfileConfig):
        super().__init__(OperationPriority.HIGH)
        self.__log: Logger = Logger(type(self).__name__)
        self.__frequency: TechnicalProfile = FrequencyProfile(config, profile_config)
        self.__max_fcr_power = config_ems.max_fcr_power  # Watt
        self.__soc_set = config_ems.soc_set  # pu

        self.__target_frequency = 50.0  # Hz
        self.__max_frequency_deviation = 0.2  # Hz
        self.__frequency_dead_band = 0.01  # Hz
        self.__frequency_dead_time = 30  # s
        self.__power_fcr_last_step = 0  # W

        if config.timestep > 1:
            self.__log.warn('Timestep is > 1s. Thus, the results are distorted and are not valid. '
                             'Rethink your timestep')

        self.__max_frequency = self.__target_frequency + self.__max_frequency_deviation  # Hz
        self.__min_frequency = self.__target_frequency - self.__max_frequency_deviation  # Hz

    def next(self, time: float, system_state: SystemState, power: float = 0) -> float:
        frequency = self.__frequency.next(time)

        # Determine FCR power with power to frequency static in pu
        power_fcr = (frequency - self.__target_frequency) / self.__max_frequency_deviation
        # Limit FCR power in pu [-1,1]
        power_fcr = max(min(power_fcr, 1), -1)

        ''' Degree of freedom 1: Slope (neglected) '''
        # frequencySlope = np.sign(
        #     power_fcr - self.__power_fcr_last_step) / self.__frequency_dead_time  # frequencySlope > 0: more power charged / discharged than in the step before
        #
        # self.__frequency_dead_time -= 1
        # if battery_system_state.get_soc() < self.__soc_set and power_fcr < 0 and frequencySlope > 0:  # if SOC is less than optimum, try to discharge as little as possible
        #     power_fcr = max(self.__power_fcr_last_step - frequencySlope, power_fcr)
        # elif battery_system_state.get_soc() < self.__soc_set and power_fcr > 0 and frequencySlope < 0:  # if SOC is less than optimum, try to charge as much as possible
        #     power_fcr = max(self.__power_fcr_last_step + frequencySlope, power_fcr)
        # elif battery_system_state.get_soc() > self.__soc_set and power_fcr > 0 and frequencySlope > 0:  # if SOC is higher than optimum, try to charge as little as possible
        #     power_fcr = min(self.__power_fcr_last_step + frequencySlope, power_fcr)
        # elif battery_system_state.get_soc() > self.__soc_set and power_fcr < 0 and frequencySlope < 0:  # if SOC is higher than optimum, try to discharge as much as possible
        #     power_fcr = min(self.__power_fcr_last_step - frequencySlope, power_fcr)
        # else:
        #     self.__frequency_dead_time = 30  # reset dead time
        # self.__power_fcr_last_step = power_fcr  # Save last value before using further degrees of freedom

        ''' Degree of freedom 2: Overfulfillment until 120% if soc > soc_set and charging vice versa '''
        if (system_state.soc > self.__soc_set and power_fcr < 0) or \
                (system_state.soc < self.__soc_set and power_fcr > 0):
            power_fcr = power_fcr * 1.2

        ''' Degree of freedom 3: Using frequency dead band around 50 Hz with +/-10 mHz '''
        # Use dead band if soc > soc_set and charging is necessary according to the frequency
        # Use dead band if soc < soc_set and discharging is necessary according to the frequency
        if abs(frequency - self.__target_frequency) <= self.__frequency_dead_band:
            if (system_state.soc >= self.__soc_set and power_fcr > 0) or \
                    (system_state.soc <= self.__soc_set and power_fcr < 0):
                power_fcr = 0

        return power_fcr * self.__max_fcr_power

    def update(self, energy_management_state: EnergyManagementState) -> None:
        energy_management_state.fcr_max_power = self.__max_fcr_power

    def close(self) -> None:
        self.__frequency.close()
