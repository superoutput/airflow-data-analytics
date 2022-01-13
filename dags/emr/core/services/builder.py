import importlib
import hms_workflow_platform.core.queries.im.encounter_query
import re


class Builder:
    def __init__(self, service):
        self._domain_name_query = re.sub(r'(?<!^)(?=[A-Z])', '_', service.__class__.__name__.replace('Service', '').replace(
            'Query', '')).lower()
        self._domain_name_template = re.sub(r'(?<!^)(?=[A-Z])', '_', service.__class__.__name__.replace('Service', '').replace(
            'Template', '')).lower()

    def getQuery(self, his, site):
        _module_name = f'hms_workflow_platform.core.queries.{his}.{self._domain_name_query.lower()}_query'
        _class_name = f'{self._domain_name_query.capitalize()}Query'
        _module = importlib.import_module(_module_name)
        _class = getattr(_module, _class_name)
        return _class(site)

    def getTemplate(self, his):
        _module_name = f'hms_workflow_platform.core.template.{his}.{self._domain_name_template.lower()}_template'
        _class_name = f'{self._domain_name_template.capitalize()}Template'
        _module = importlib.import_module(_module_name)
        _class = getattr(_module, _class_name)
        return _class()
