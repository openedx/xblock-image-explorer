# Test mocks and helpers
from xblock.runtime import DictKeyValueStore, KvsFieldData
from xblock.test.tools import TestRuntime


class MockRuntime(TestRuntime):
    """
    Provides a mock XBlock runtime object.
    """
    def __init__(self, **kwargs):
        field_data = kwargs.get('field_data', KvsFieldData(DictKeyValueStore()))
        super(MockRuntime, self).__init__(field_data=field_data)
