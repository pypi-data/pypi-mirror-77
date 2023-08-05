from abc import ABC, abstractmethod

from simses.commons.state.technology.redox_flow_state import RedoxFlowState


class ElectrochemicalModel(ABC):
    """Model that calculates the current and voltage of the redox flow stack module."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def update(self, time: float, redox_flow_state: RedoxFlowState, power_target: float) -> None:
        """
        Updating power (if changes due to battery management), current, voltage, power loss and soc of redox_flow_state.
        In the update function the battery management system requests are implemented.

        Parameters
        ----------
        time : float
            current simulation time in s
        redox_flow_state : RedoxFlowState
            current state of redox flow battery
        power_target : float
            target power in W

        Returns
        -------
            None
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Closing all resources in electrochemical losses model."""
        pass
