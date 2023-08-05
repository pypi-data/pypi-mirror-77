from simses.config.data.data_config import DataConfig
from simses.constants_simses import ROOT_PATH


class RedoxFlowDataConfig(DataConfig):

    def __init__(self, path: str = None):
        super().__init__(path)
        self.__section: str = 'REDOX_FLOW_DATA'

    @property
    def redox_flow_data_dir(self) -> str:
        """Returns directory of redox flow data files"""
        return ROOT_PATH + self.get_property(self.__section, 'REDOX_FLOW_DATA_DIR')

    @property
    def rfb_rint_file(self) -> str:
        """Returns filename for internal resistance of a RFB stack"""
        return self.redox_flow_data_dir + self.get_property(self.__section, 'RFB_RINT_FILE')

    @property
    def redox_flow_hydrogen_evolution_dir(self) -> str:
        """Returns directory of redox flow hydrogen evolution current data files"""
        return ROOT_PATH + self.get_property(self.__section, 'REDOX_FLOW_HYDROGEN_EVOLUTION_DATA')

    @property
    def rfb_h2_evolution_schweiss_f1_file(self) -> str:
        """Returns filename for the hydrogen evolution of a RFB electrode F1 (source: Schweiss 2016)"""
        return self.redox_flow_hydrogen_evolution_dir + self.get_property(self.__section, 'REDOX_FLOW_HYDROGEN_SCHWEISS_F1')

    @property
    def rfb_h2_evolution_schweiss_f2_file(self) -> str:
        """Returns filename for the hydrogen evolution of a RFB electrode F2 (source: Schweiss 2016)"""
        return self.redox_flow_hydrogen_evolution_dir + self.get_property(self.__section, 'REDOX_FLOW_HYDROGEN_SCHWEISS_F2')

    @property
    def rfb_h2_evolution_schweiss_f3_file(self) -> str:
        """Returns filename for the hydrogen evolution of a RFB electrode F3 (source: Schweiss 2016)"""
        return self.redox_flow_hydrogen_evolution_dir + self.get_property(self.__section, 'REDOX_FLOW_HYDROGEN_SCHWEISS_F3')

    @property
    def rfb_h2_evolution_schweiss_f4_file(self) -> str:
        """Returns filename for the hydrogen evolution of a RFB electrode F4 (source: Schweiss 2016)"""
        return self.redox_flow_hydrogen_evolution_dir + self.get_property(self.__section, 'REDOX_FLOW_HYDROGEN_SCHWEISS_F4')
