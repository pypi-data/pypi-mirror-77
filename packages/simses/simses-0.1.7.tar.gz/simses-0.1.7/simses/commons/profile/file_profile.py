import sys
from datetime import datetime

from pytz import timezone

from simses.commons.log import Logger
from simses.commons.timeseries.average.average import Average
from simses.commons.timeseries.average.mean_average import MeanAverage
from simses.commons.timeseries.interpolation.interpolation import Interpolation
from simses.commons.timeseries.interpolation.linear_interpolation import LinearInterpolation
from simses.commons.timeseries.timevalue import TimeValue
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.error import EndOfFileError


class FileProfile:

    class Header:
        TIMEZONE: str = 'Timezone'
        UNIT: str = 'Unit'
        TIME: str = 'Time'
        SAMPLING: str = 'Sampling in s'

    UNITS: dict = {'W': 1, 'kW': 1e3, 'MW': 1e6, 'GW': 1e9, 's': 1, 'ms': 0.001, 'EUR': 1, 'TEUR': 1e3, 'Hz': 1, '%': 0.01}

    __TIME_IDX: int = 0

    __EPOCH_FORMAT: str = 'epoch'
    __DATE_FORMATS: [str] = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%d.%m.%Y %H:%M:%S', '%d.%m.%Y %H:%M',
                             __EPOCH_FORMAT]

    __UTC: timezone = timezone('UTC')
    __BERLIN: timezone = timezone('Europe/Berlin')

    def __init__(self, config: GeneralSimulationConfig, filename: str, delimiter: str = ',', scaling_factor: float = 1,
                 value_index: int = 1):
        self.__log: Logger = Logger(type(self).__name__)
        self.__filename: str = filename
        self.__delimiter: str = delimiter
        self.__scaling_factor: float = scaling_factor
        self.__VALUE_IDX: int = value_index
        self.__timestep: float = config.timestep
        self.__start: float = config.start
        self.__end: float = config.end
        self.__time_offset: int = 0
        self.__date_format = None
        self.__last_data: [TimeValue] = list()
        self.__last_time: float = self.__start
        self.__interpolation: Interpolation = LinearInterpolation()
        self.__average: Average = MeanAverage()
        header: dict = self.get_header_from(self.__filename)
        self.__unit_factor: float = self.__get_value_unit_from(header)
        self.__time_factor: float = self.__get_time_unit_from(header)
        self.__timezone: timezone = self.__get_timezone_from(header)
        self.__sampling_time: float = self.__get_sampling_time_from(header)
        self.__time_generator = self.__get_time_generator()
        self.__initialize_file()

    def next(self, time: float) -> float:
        try:
            data: [TimeValue] = self.__get_data_until(time)
            values: [TimeValue] = self.__filter_current_values(time, data)
            if not values and len(data) < 2:
                value: float = self.__average.average(data)
            elif not values:
                value: float = self.__interpolation.interpolate(time, data[-1], data[-2])
            else:
                value: float = self.__average.average(values)
            self.__last_data = self.__filter_last_values(data)
            self.__last_time = time
            return value * self.__scaling_factor
        except EndOfFileError as err:
            self.__log.warn(str(err))
            return 0.0

    def __filter_current_values(self, time: float, data: [TimeValue]) -> [TimeValue]:
        values: [TimeValue] = list()
        data_iterator = iter(data)
        try:
            while True:
                value = next(data_iterator)
                if self.__last_time < value.time <= time:
                    values.append(value)
        except StopIteration:
            pass
        return values

    def __filter_last_values(self, data: [TimeValue]) -> [TimeValue]:
        return data[-2:]
        # values: [TimeValue] = list()
        # data_iterator = iter(data)
        # try:
        #     while True:
        #         value = next(data_iterator)
        #         if self.__last_time < value.time:
        #             values.append(value)
        # except StopIteration:
        #     pass
        # return values

    def __get_data_until(self, time: float) -> [TimeValue]:
        values: list = list()
        data = self.__last_data[-1]
        while data.time < time:
            data = self.__get_next_data()
            values.append(data)
        values.extend(self.__last_data)
        TimeValue.sort_by_time(values)
        return values

    def __get_next_data(self) -> TimeValue:
        while True:
            line: str = ''
            try:
                line = self.__file.readline()
                if line.startswith('#') or line.startswith('"""') or line in ['\r\n', '\n']:# or self.__delimiter not in line:
                    continue
                if line == '':  # end of file_name
                    raise EndOfFileError('End of Profile ' + self.__filename + ' reached.')
                data = line.split(self.__delimiter)
                if len(data) < 2:
                    time: float = next(self.__time_generator) + self.__time_offset
                    value: float = float(data[self.__VALUE_IDX - 1]) * self.__unit_factor
                else:
                    time: float = self.__format_time(data[self.__TIME_IDX]) * self.__time_factor + self.__time_offset
                    value: float = float(data[self.__VALUE_IDX]) * self.__unit_factor
                return TimeValue(time, value)
            except ValueError:
                self.__log.error('No value found for ' + line)

    def __get_time_generator(self):
        time: float = self.__start
        while True:
            yield time
            time += self.__sampling_time

    def __format_time(self, time: str) -> float:
        if self.__date_format is None:
            self.__date_format = self.__find_date_format_for(time)
            self.__log.info('Found format: ' + str(self.__date_format))
        if self.__date_format == self.__EPOCH_FORMAT:
            return float(time)
        else:
            return self.__extract_timestamp_from(time, self.__date_format)

    def __find_date_format_for(self, time: str) -> str:
        for date_format in self.__DATE_FORMATS:
            try:
                if date_format == self.__EPOCH_FORMAT:
                    float(time)
                    return date_format
                else:
                    self.__extract_timestamp_from(time, date_format)
                    return date_format
            except ValueError:
                pass
        raise Exception('Unknown date format for ' + time)

    def __extract_timestamp_from(self, time: str, date_format: str) -> float:
        date: datetime = datetime.strptime(time, date_format)
        date = self.__get_local_datetime_from(date=date)
        return date.timestamp()

    def __get_local_datetime_from(self, date: datetime = None, tstmp: float = None) -> datetime:
        if date is None:
            if tstmp is None:
                tstmp = datetime.now()
            date = datetime.fromtimestamp(tstmp)
        return self.__timezone.localize(date, is_dst=None)

    def __initialize_file(self) -> None:
        self.__file = open(self.__filename, 'r', newline='')
        self.__last_data = self.__get_initial_data()

    def __get_initial_data(self) -> [TimeValue]:
        timestamp: float = self.__start
        data = self.__get_next_data()
        self.__set_time_offset(data.time, timestamp)
        data.time += self.__time_offset
        while data.time < timestamp:
            data = self.__get_next_data()
        return [data]

    def __set_time_offset(self, file_tstmp: float, simulation_tstmp: float) -> None:
        #Set profile year to simulation year
        file_date = self.__get_local_datetime_from(tstmp=file_tstmp)
        simulation_date = self.__get_local_datetime_from(tstmp=simulation_tstmp)
        if file_date.year == simulation_date.year:
            return
        adapted_file_tstmp = file_date.replace(year=simulation_date.year).timestamp()
        self.__time_offset = adapted_file_tstmp - file_tstmp
        if not self.__time_offset == 0:
            self.__log.warn('Time offset is ' + str(self.__time_offset) + ' s. \n'
                            'File time: ' + str(self.__get_local_datetime_from(tstmp=file_tstmp)) + ', \n'
                            'Simulation time: ' + str(self.__get_local_datetime_from(tstmp=simulation_tstmp)))

    def __get_timezone_from(self, header: dict) -> timezone:
        try:
            tz: str = header[self.Header.TIMEZONE]
            return timezone(tz)
        except KeyError:
            return self.__UTC

    def __get_unit_from(self, header: dict, identifier: str) -> float:
        try:
            unit: str = header[identifier]
            return self.UNITS[unit]
        except KeyError:
            self.__log.warn('Unit for ' + self.__filename + ' is unknown. Valid types are ' +
                            str(self.UNITS.keys()) + '.')
            return 1

    def __get_value_unit_from(self, header: dict) -> float:
        return self.__get_unit_from(header, self.Header.UNIT)

    def __get_time_unit_from(self, header: dict) -> float:
        return self.__get_unit_from(header, self.Header.TIME)

    def __get_sampling_time_from(self, header: dict) -> float:
        try:
            sampling_time: str = header[self.Header.SAMPLING]
            return float(sampling_time)
        except KeyError:
            return self.__timestep

    def profile_data_to_list(self, sign_factor=1) -> ([float], [float]):
        """
        Extracts the whole time series as a list and resets the pointer of the (internal) file afterwards

        Parameters
        ----------
        sign_factor :

        Returns
        -------
        list:
            profile values as a list

        """
        profile_data: [float] = list()
        time_data: [float] = list()
        time_generator = self.__get_time_generator()
        time: float = next(time_generator)
        while time <= self.__end:
            time_data.append(time)
            profile_data.append(self.next(time) * sign_factor)
            time = next(time_generator)
        self.__initialize_file()
        return time_data, profile_data

    @staticmethod
    def get_header_from(filename: str) -> dict:
        """
        Extracts header from given file

        Attention: Only searches in the first ten lines for a header!

        Parameters
        ----------
        filename :

        Returns
        -------
        dict:
            header with key/value pairs

        """
        header: dict = dict()
        with open(filename, 'r', newline='') as file:
            line = file.readline()
            line_count: int = 0
            while True:
                if '#' in line:
                    try:
                        key_raw, entry_raw = line.split(sep=':', maxsplit=1)
                        key = key_raw.strip('# ')
                        entry = entry_raw.strip()
                        header[key] = entry
                    except ValueError:
                        sys.stderr.write('WARNING: Could not interpret ' + line)
                        sys.stderr.flush()
                line = file.readline()
                if line_count > 10:
                    break
                else:
                    line_count += 1
        return header

    def close(self):
        self.__log.close()
        self.__file.close()
