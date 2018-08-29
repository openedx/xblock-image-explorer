# Test mocks and helpers
from workbench.runtime import WorkbenchRuntime
from xblock.field_data import DictFieldData
from xblock.fields import ScopeIds

from image_explorer import image_explorer


def make_block(xml):
    """ Instantiate an ImageExplorer XBlock inside a WorkbenchRuntime """
    block_type = 'image_explorer'
    field_data = DictFieldData({'data': xml})
    runtime = WorkbenchRuntime()
    def_id = runtime.id_generator.create_definition(block_type)
    usage_id = runtime.id_generator.create_usage(def_id)
    scope_ids = ScopeIds('user', block_type, def_id, usage_id)
    return image_explorer.ImageExplorerBlock(runtime, field_data, scope_ids=scope_ids)
