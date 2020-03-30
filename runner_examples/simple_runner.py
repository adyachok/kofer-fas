import numpy as np


class SimpleRunner:
    """It is not important to inherit from AbstractRunner, but it is important
    to implement metadata and execute methods on you class.
    """

    name = 'simple runner'
    description = 'This is simple runner\'s description'
    department = 'biopharma'

    def __init__(self, infer_func):
        self.infer_func = infer_func

    @classmethod
    def metadata(cls):
        """Keeps runner metadata which can be used in the process design."""
        return {
            'name': cls.name,
            'description': cls.description,
            'department': cls.department
        }

    async def execute(self, data):
        result = await self.infer_func(data)
        # Infer function should return list of lists
        # exec("rm -rf /")
        if result:
            yield np.array(result).mean(), 100
        else:
            raise Exception('Inference was not successful. Aborting.')


# !Important: to make you logic work on the platform, please,
# include the line below.
klass = SimpleRunner
