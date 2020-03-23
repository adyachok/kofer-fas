from typing import Dict, Generator, Any


class AbstractRunner:
    """This class should be always inherited by any runner script."""

    def execute(self) -> Generator[Any, int]:
        """Executes data-science logic.
           :returns result object, readiness state (from 0 to 100)
        """
        raise NotImplementedError

    def metadata(self) -> Dict:
        """Keeps runner metadata which can be used in the process design."""
        raise NotImplementedError


class AbstractRunnerMetadata:

    @property
    def name(self):
        return NotImplementedError

    @property
    def description(self):
        return NotImplementedError

    @property
    def department(self):
        return NotImplementedError
