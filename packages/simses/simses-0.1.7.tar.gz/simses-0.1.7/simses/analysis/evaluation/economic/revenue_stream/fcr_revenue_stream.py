import numpy

from simses.analysis.data.energy_management_data import EnergyManagementData
from simses.analysis.data.system_data import SystemData
from simses.analysis.evaluation.economic.revenue_stream.revenue_stream import RevenueStream
from simses.analysis.evaluation.evaluation_result import EvaluationResult, Unit, Description
from simses.commons.log import Logger
from simses.commons.profile.economic_profile.fcr_market import FcrMarket
from simses.config.analysis.economic_analysis_config import EconomicAnalysisConfig


class FCRRevenue(RevenueStream):

    def __init__(self, energy_management_data: EnergyManagementData, system_data: SystemData,
                 economic_analysis_config: EconomicAnalysisConfig, market: FcrMarket):
        super().__init__(energy_management_data, system_data, economic_analysis_config)
        self._energy_management_data: EnergyManagementData = energy_management_data
        self.__fcr_price_profile: FcrMarket = market
        if economic_analysis_config.fcr_use_price_timeseries:
            self.__fcr_time, self.__fcr_price = self.__fcr_price_profile.profile_data_to_list()
            #self.__fcr_time, self.__fcr_price = self.__fcr_price_profile.read_whole_file_adjusted(
            #    float(self._energy_management_data.time[0]), float(self._energy_management_data.time[-1]),
            #    float(self._energy_management_data.time[1]) - float(self._energy_management_data.time[0]))
        else:
            fcr_price = economic_analysis_config.fcr_price
            self.__fcr_price = [fcr_price for i in range(len(self._energy_management_data.time))]
        self.__system_data: SystemData = system_data
        self.__log: Logger = Logger(type(self).__name__)
        self.__fcr_power_avg = numpy.array([])
        self.__fcr_price_avg = numpy.array([])
        self.__fcr_revenue = numpy.array([])
        self.day_to_sec = 60 * 60 * 24
        self.year_to_sec = self.day_to_sec * 365

    def get_cashflow(self) -> numpy.ndarray:
        time = self._energy_management_data.time
        fcr_power = abs(self._energy_management_data.fcr_max_power)
        fcr_price_list = self.__fcr_price
        t = 0
        t_year_start = 0
        cashflow_fcr = 0
        fcr_power_avg = []
        fcr_price_avg = []
        cashflow_list_fcr = []
        fcr_price_scaling_factor_day_to_second = 1 / 1e3 * 1 / self.day_to_sec
        delta_ts = time[1] - time[0]

        while t < len(time):
            if time[t] - time[t_year_start] >= self.year_to_sec:
                fcr_power_avg.append(sum(fcr_power[t_year_start:t]) / (t - t_year_start + 1))
                fcr_price_avg.append(sum(fcr_price_list[t_year_start:t]) / (t - t_year_start + 1))
                cashflow_list_fcr.append(cashflow_fcr)
                t_year_start = t
                cashflow_fcr = 0
            cashflow_fcr += delta_ts * fcr_power[t] * fcr_price_list[t] * fcr_price_scaling_factor_day_to_second
            t += 1
                
        # Adding non-full year
        fcr_power_avg.append(sum(fcr_power[t_year_start:t]) / (t - t_year_start - 1))
        fcr_price_avg.append(sum(fcr_price_list[t_year_start:t]) / (t - t_year_start - 1))
        cashflow_list_fcr.append(cashflow_fcr)

        self.__fcr_power_avg = numpy.array(fcr_power_avg)
        self.__fcr_price_avg = numpy.array(fcr_price_avg)
        self.__fcr_revenue = numpy.array(cashflow_list_fcr)
        return numpy.array(cashflow_list_fcr)

    def get_evaluation_results(self) -> [EvaluationResult]:
        key_results: [EvaluationResult] = list()
        key_results.append(EvaluationResult(Description.Economical.FCR.REVENUE_YEARLY, Unit.EURO, self.__fcr_revenue))
        return key_results

    def get_assumptions(self) -> [EvaluationResult]:
        assumptions: [EvaluationResult] = list()
        assumptions.append(EvaluationResult(Description.Economical.FCR.PRICE_AVERAGE, Unit.EURO_PER_KWH_DAY, self.__fcr_price_avg))
        assumptions.append(EvaluationResult(Description.Economical.FCR.POWER_BID_AVERAGE, Unit.KILOWATT, self.__fcr_power_avg / 1000.0))
        return assumptions

    def close(self):
        self.__log.close()
