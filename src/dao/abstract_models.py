from typing import Dict, Generator, Any


class AbstractRunner:
    """This class should be always inherited by any runner script."""

    def execute(self) -> Generator[Any, None, int]:
        """Executes data-science logic.
           :returns result object, readiness state (from 0 to 100)
        """
        raise NotImplementedError

    @classmethod
    def metadata(cls):
        """Keeps runner metadata which can be used in the process design."""
        return {
            'name': cls.name,
            'description': cls.description,
            'department': cls.department
        }
