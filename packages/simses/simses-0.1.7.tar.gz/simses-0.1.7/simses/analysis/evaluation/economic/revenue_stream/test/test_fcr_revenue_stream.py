import pandas
import numpy as np
import pytest
from configparser import ConfigParser
from simses.analysis.data.energy_management_data import EnergyManagementData
from simses.analysis.data.system_data import SystemData
from simses.analysis.evaluation.economic.revenue_stream.fcr_revenue_stream import FCRRevenue
from simses.commons.state.energy_management_state import EnergyManagementState
from simses.commons.state.system_state import SystemState
from simses.config.analysis.economic_analysis_config import EconomicAnalysisConfig
from simses.config.simulation.general_config import GeneralSimulationConfig

# fixed input parameters
fcr_price = 0.3  # EUR / (kW * day)
years = 5
timestep = 3600


def create_general_config() -> GeneralSimulationConfig:
    simulation_config: ConfigParser = ConfigParser()
    simulation_config.add_section('GENERAL')
    simulation_config.set('GENERAL', 'TIME_STEP', str(timestep))
    return GeneralSimulationConfig(simulation_config)


def create_economic_analysis_config() -> EconomicAnalysisConfig:
    analysis_config: ConfigParser = ConfigParser()
    analysis_config.add_section('ECONOMIC_ANALYSIS')
    analysis_config.set('ECONOMIC_ANALYSIS', 'FCR_PRICE', str(fcr_price))
    analysis_config.set('ECONOMIC_ANALYSIS', 'FCR_USE_PRICE_TIMESERIES', 'False')
    return EconomicAnalysisConfig(analysis_config)


@pytest.mark.parametrize('fcr_power_const', [-1e6, 1e6])
def test_fcr_revenue_stream(fcr_power_const):
    """Performs a unit test by comparing the expected result for a generic
    time series with the actual result."""

    # set up test data
    n = int(years * 365 * 24 * 60 * 60 / timestep)
    unix_timestamp_start_2020 = 1577836800
    time_test = pandas.array([unix_timestamp_start_2020 + timestep * i for i in range(n)])
    fcr_power = pandas.array([fcr_power_const] * n)
    battery_power = pandas.array([0] * n)

    # calculate expected result:
    expected_result = np.array([abs(fcr_power_const) * 365 * fcr_price / 1000] * years)

    # build configs for testing
    gen_sim_config = create_general_config()
    economic_config = create_economic_analysis_config()

    # create data for testing
    energy_management_dict = {EnergyManagementState.TIME: time_test, EnergyManagementState.FCR_MAX_POWER: fcr_power}
    energy_management_data = EnergyManagementData(gen_sim_config, pandas.DataFrame(energy_management_dict))
    system_dict = {SystemState.TIME: time_test, SystemState.AC_POWER_DELIVERED: battery_power}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    fcr_revenue_stream = FCRRevenue(energy_management_data, system_data, economic_config, None)
    result1 = fcr_revenue_stream.get_cashflow()
    assert list(result1.round(0)) == list(expected_result.round(0))