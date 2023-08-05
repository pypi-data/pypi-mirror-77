import numpy as np

from simses.analysis.data.system_data import SystemData
from simses.analysis.evaluation.evaluation_result import EvaluationResult, Description, Unit
from simses.analysis.evaluation.plotting.axis import Axis
from simses.analysis.evaluation.plotting.plotly_plotting import PlotlyPlotting
from simses.analysis.evaluation.plotting.plotting import Plotting
from simses.analysis.evaluation.technical.technical_evaluation import TechnicalEvaluation
from simses.analysis.utils import get_positive_values_from, get_sum_for, get_negative_values_from
from simses.commons.log import Logger
from simses.commons.state.system_state import SystemState
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig


class SystemTechnicalEvaluation(TechnicalEvaluation):

    __power_title = 'System power'
    __soc_title = 'System SOC'
    __additional_title = 'Additional DC power'

    def __init__(self, data: SystemData, config: GeneralAnalysisConfig, path: str):
        super().__init__(data, config)
        self.__log: Logger = Logger(type(self).__name__)
        title_extension: str = ' for system ' + self.get_data().id
        self.__power_title += title_extension
        self.__soc_title += title_extension
        self.__additional_title += title_extension
        self.__result_path = path

    def evaluate(self):
        super().evaluate()
        data: SystemData = self.get_data()
        mean_charge_dcdc_efficiency: float = self.mean_dcdc_efficiency_charge()
        mean_discharge_dcdc_efficiency: float = self.mean_dcdc_efficiency_discharge()
        mean_dcdc_efficiency: float = self.__weighted_mean(mean_charge_dcdc_efficiency, mean_discharge_dcdc_efficiency, data.dc_power_storage)
        mean_discharge_pe_efficiency: float = self.mean_acdc_efficiency_discharge()
        mean_charge_pe_efficiency: float = self.mean_acdc_efficiency_charge()
        mean_pe_efficiency: float = self.__weighted_mean(mean_charge_pe_efficiency, mean_discharge_pe_efficiency, data.power)# mean_charge_pe_efficiency * mean_discharge_pe_efficiency / 100.0
        mean_pe_efficiency_overall: float = mean_pe_efficiency * mean_dcdc_efficiency / 100.0
        self.append_result(EvaluationResult(Description.Technical.ACDC_EFFICIENCY_DISCHARGE_MEAN, Unit.PERCENTAGE, mean_discharge_pe_efficiency))
        self.append_result(EvaluationResult(Description.Technical.ACDC_EFFICIENCY_CHARGE_MEAN, Unit.PERCENTAGE, mean_charge_pe_efficiency))
        self.append_result(EvaluationResult(Description.Technical.ACDC_EFFICIENCY_MEAN, Unit.PERCENTAGE, mean_pe_efficiency))
        self.append_result(EvaluationResult(Description.Technical.DCDC_EFFICIENCY_DISCHARGE_MEAN, Unit.PERCENTAGE,mean_discharge_dcdc_efficiency))
        self.append_result(EvaluationResult(Description.Technical.DCDC_EFFICIENCY_CHARGE_MEAN, Unit.PERCENTAGE,mean_charge_dcdc_efficiency))
        self.append_result(EvaluationResult(Description.Technical.DCDC_EFFICIENCY_MEAN, Unit.PERCENTAGE, mean_dcdc_efficiency))
        self.append_result(EvaluationResult(Description.Technical.PE_EFFICIENCY_MEAN, Unit.PERCENTAGE, mean_pe_efficiency_overall))
        # self.append_time_series(SystemState.DC_POWER_STORAGE, data.dc_power_storage)
        self.print_results()

    def plot(self) -> None:
        self.power_plotting()
        self.soc_plotting()
        self.additional_dc_power_plotting()

    def soc_plotting(self):
        data: SystemData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=self.__soc_title, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=SystemState.TIME)
        yaxis: [Axis] = [Axis(data.soc, label=SystemState.SOC)]
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def additional_dc_power_plotting(self):
        data: SystemData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=self.__additional_title, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=SystemState.TIME)
        yaxis: [Axis] = [Axis(data.dc_power_additional, label=SystemState.DC_POWER_ADDITIONAL)]
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def power_plotting(self):
        data: SystemData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=self.__power_title, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=SystemState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(data.dc_power_storage, label=SystemState.DC_POWER_STORAGE,
                          color=PlotlyPlotting.Color.BLACK, linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data.power, label=SystemState.AC_POWER_DELIVERED, color=PlotlyPlotting.Color.GREEN,
                          linestyle=PlotlyPlotting.Linestyle.DASHED))
        yaxis.append(Axis(data.dc_power, label=SystemState.DC_POWER_INTERMEDIATE_CIRCUIT, color=PlotlyPlotting.Color.RED,
                          linestyle=PlotlyPlotting.Linestyle.DASHED))
        yaxis.append(Axis(data.ac_power_target, label=SystemState.AC_POWER, color=PlotlyPlotting.Color.BLUE,
                          linestyle=PlotlyPlotting.Linestyle.DASH_DOT))
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def mean_dcdc_efficiency_discharge(self) -> float:
        """
        Calculates discharge efficiency of dcdc converter

        Returns
        -------
        float:
            average power electronics efficiency (discharge)
        """
        data: SystemData = self.get_data()
        dc_power_intermediate_circuit = data.dc_power + data.dc_power_additional
        return self.__mean_discharge(dc_power_intermediate_circuit, data.dc_power_storage)

    def mean_dcdc_efficiency_charge(self) -> float:
        """
        Calculates charge efficiency of dcdc converter

        Returns
        -------
        float:
            average power electronics efficiency (charge)
        """
        data: SystemData = self.get_data()
        dc_power_intermediate_circuit = data.dc_power + data.dc_power_additional
        return self.__mean_charge(data.dc_power_storage, dc_power_intermediate_circuit)

    def mean_acdc_efficiency_discharge(self) -> float:
        """
        Calculates discharge efficiency of acdc converter

        Returns
        -------
        float:
            average power electronics efficiency (discharge)
        """
        data: SystemData = self.get_data()
        return self.__mean_discharge(data.ac_pe_power, data.dc_power)

    def mean_acdc_efficiency_charge(self) -> float:
        """
        Calculates charge efficiency of acdc converter

        Returns
        -------
        float:
            average power electronics efficiency (charge)
        """
        data: SystemData = self.get_data()
        return self.__mean_charge(data.dc_power, data.ac_pe_power)

    def __mean_charge(self, power_series_numerator: np.ndarray, power_series_denominator: np.ndarray) -> float:
        """
        Calculates the average power electronics efficiency when discharging.
        For every discharging step the efficiency is calculated and in the end the mean value of all efficiencies.

        Parameters
        ----------
        power_series_numerator :
        power_series_denominator :

        Returns
        -------

        """
        power_numerator = power_series_numerator[:].copy()
        power_denominator = power_series_denominator[:].copy()
        power_numerator[power_numerator <= 0] = np.nan
        power_denominator[power_denominator <= 0] = np.nan
        if self.__contains_only_nan(power_numerator):
            self.__log.debug('Only nan in: ' + str(power_numerator))
            return np.nan
        if self.__contains_only_nan(power_denominator):
            self.__log.debug('Only nan in: ' + str(power_denominator))
            return np.nan
        mean_charge = np.nanmean(power_numerator / power_denominator)
        return 100.0 * mean_charge

    def __mean_discharge(self, power_series_numerator: np.ndarray, power_series_denominator: np.ndarray) -> float:
        """
        Calculates the average power electronics efficiency when charging.
        For every charging step the efficiency is calculated and in the end the mean value of all efficiencies.

        Parameters
        ----------
        power_series_numerator :
        power_series_denominator :

        Returns
        -------

        """
        power_numerator = power_series_numerator[:].copy()
        power_denominator = power_series_denominator[:].copy()
        power_numerator[power_numerator >= 0] = np.nan
        power_denominator[power_denominator >= 0] = np.nan
        if self.__contains_only_nan(power_numerator):
            self.__log.debug('Only nan in: ' + str(power_numerator))
            return np.nan
        if self.__contains_only_nan(power_denominator):
            self.__log.debug('Only nan in: ' + str(power_denominator))
            return np.nan
        mean_discharge = np.nanmean(power_numerator / power_denominator)
        return 100.0 * mean_discharge

    def __weighted_mean(self, eta_charge: float, eta_discharge: float, power_series: np.ndarray) -> float:
        """
        Calculates an energy weighted mean value of charge and discharge efficiencies

        Parameters
        ----------
        eta_charge :
        eta_discharge :
        power_series :

        Returns
        -------

        """
        data: SystemData = self.get_data()
        power = power_series[:].copy()
        charge_energy: float = get_sum_for(get_positive_values_from(power) * data.convert_watt_to_kWh)
        discharge_energy: float = get_sum_for(-1 * get_negative_values_from(power) * data.convert_watt_to_kWh)
        energy_throughput: float = charge_energy + discharge_energy
        mean: float = (eta_charge * charge_energy + eta_discharge * discharge_energy) / energy_throughput / 100.0
        return mean**2 * 100.0

    @staticmethod
    def __contains_only_nan(data: np.ndarray) -> bool:
        """
        If data array contains only NaN, method returns True; False otherwise.

        Parameters
        ----------
        data :

        Returns
        -------

        """
        return len(data) == 0 or np.isnan(data).all()

    def close(self) -> None:
        self.__log.close()
        super().close()
