from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.simulation.storage_system.technology.hydrogen.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.pem_electrolyzer_multi_dim_analytic_model.pem_membrane_model import PemMembraneModel


class PemFluidModel:

    def __init__(self, membrane_model: PemMembraneModel):
        self.__membrane_model: PemMembraneModel = membrane_model

    def get_h2_net_cathode(self, state: ElectrolyzerState, current_cell: float) -> float:
        return self.__h2_generation_cell(current_cell) - \
               self.__membrane_model.get_h2_permeation_for_cell(state, current_cell) - \
               2 * self.__membrane_model.get_o2_permeation_for_cell(state, current_cell)  # mol/s

    def get_o2_net_anode(self, state: ElectrolyzerState, current_cell: float) -> float:
        return self.__o2_generation_cell(current_cell) - \
               self.__membrane_model.get_o2_permeation_for_cell(state, current_cell / self.__membrane_model.get_geometric_area_cell())  # mol/s

    def get_h2o_net_use_cell(self, state: ElectrolyzerState, current_cell: float) -> float:
        return - (self.__h2o_net_anode(current_cell) +
                  self.__h2o_net_cathode(state, current_cell))  # mol/s

    def __h2_generation_cell(self, current_cell) -> float:
        return current_cell / (2 * ConstantsHydrogen.FARADAY_CONST)  # mol/s

    def __o2_generation_cell(self, current_cell) -> float:
        return current_cell / (4 * ConstantsHydrogen.FARADAY_CONST)  # mol/s

    def __h2o_use_cell(self, current_cell) -> float:
        return current_cell / (2 * ConstantsHydrogen.FARADAY_CONST)  # mol/s

    def __h2o_net_cathode(self, state: ElectrolyzerState, current_cell: float) -> float:
        return self.__membrane_model.get_h2o_permeation_for_cell(current_cell) + \
               2 * self.__membrane_model.get_o2_permeation_for_cell(state, current_cell)  # mol/s

    def __h2o_net_anode(self, current_cell) -> float:
        return - self.__h2o_use_cell(current_cell) - \
               self.__membrane_model.get_h2o_permeation_for_cell(current_cell)  # mol/s

    def get_h2_generation_cell(self, current_cell) -> float:
        return self.__h2_generation_cell(current_cell)

    def get_o2_generation_cell(self, current_cell) -> float:
        return self.__o2_generation_cell(current_cell)

    def get_h2o_use_cell(self, current_cell) -> float:
        return self.__h2o_use_cell(current_cell)
