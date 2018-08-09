# Test mocks and helpers
from mock import patch, MagicMock

from xblock.runtime import DictKeyValueStore, KvsFieldData
from xblock.test.tools import TestRuntime


class MockRuntime(TestRuntime):
    """
    Provides a mock XBlock runtime object.
    """
    def __init__(self, **kwargs):
        field_data = kwargs.get('field_data', KvsFieldData(DictKeyValueStore()))
        super(MockRuntime, self).__init__(field_data=field_data)


def patch_static_replace_module():
    """
    patchs platform's `static_replace` module as it's
    unavailable in test environment
    """
    mocked_static_replace = MagicMock()
    mocked_static_replace.replace_static_urls = _mocked_replace_static_urls

    patch.dict('sys.modules', static_replace=mocked_static_replace).start()


def _mocked_replace_static_urls(*args, **kwargs):
    """
    fake `replace_static_urls` method
    """
    return '/a/dynamic/url'
