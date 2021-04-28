import json


class AgentTypeForCBHelper:
    def __init__(self, agent_type):
        self.data = agent_type
        self.od = {}
        self.load_into_dict('id')
        self.load_into_dict('description')
        self.load_into_dict('partner')
        self.load_actions_dict()
        self.load_parameters_dict()

    def dumps(self):
        return json.dumps(self.od)

    def load_into_dict(self, key):
        if key in self.data:
            self.od[key] = self.data[key]

    def load_actions_dict(self):
        if not 'actions' in self.data:
            return

        actions = self.data['actions']
        oda = []
        self.od['actions'] = oda
        source = self.data['source']

        for a in actions:
            da = {'config': {'cmd': a['cmd']},
                  'id': a['id'],
                  'status': a['status'],
                  'source': source}
            oda.append(da)

    def load_parameters_dict(self):
        if not 'parameters' in self.data:
            return

        parameters = self.data['parameters']
        source = self.data['source']
        schema = self.data['schema']

        odp = []
        self.od['parameters'] = odp

        for p in parameters:
            dp = {
                'config': {
                    'path': p['path'].split('.'),
                    'schema': schema,
                    'source': source
                },
                'id': p['path'],
                'type': p['type']
            }
            if 'description' in p:
                dp['description'] = p['description']
            if 'list' in p:
                dp['list'] = p['list']
            if 'example' in p:
                dp['example'] = p['example']
            if 'type' in p:
                dp['type'] = p['type']
            odp.append(dp)
