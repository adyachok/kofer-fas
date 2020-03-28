import numpy as np


class AbstractRunner:
    """This class should be always inherited by any runner script."""
    name = None
    description = None
    department = None

    def __init__(self, infer_func):
        self.infer_func = infer_func

    def execute(self):
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


class SimpleRunner(AbstractRunner):
    """It is not important to inherit from AbstractRunner, but it is important
    to implement metadata and execute methods on you class.
    """

    name = 'simple runner'
    description = 'This is simple runner\'s description'
    department = 'biopharma'

    def execute(self):
        result = self.infer_func()
        # Infer function should return list of lists
        # exec("rm -rf /")
        if result:
            yield np.array(result).mean(), 100
        else:
            raise Exception('Inference was not successful. Aborting.')


# !Important: to make you logic work on the platform, please,
# include the line below.
klass = SimpleRunner
