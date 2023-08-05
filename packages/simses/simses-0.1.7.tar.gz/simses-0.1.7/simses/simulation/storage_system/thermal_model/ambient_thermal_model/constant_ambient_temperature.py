from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class ConstantAmbientTemperature(AmbientThermalModel):

    def __init__(self, temperature: float = 25):
        super().__init__()
        self.__temperature = 273.15 + temperature  # K

    def get_temperature(self, time) -> float:
        return self.__temperature

    def get_initial_temperature(self) -> float:
        """
        Returns the ambient temperature

        Parameters
        -------
        time : current simulation time

        Returns
        -------
        float
            ambient temperature in Kelvin
        """
        return self.__temperature

    def close(self):
        pass
