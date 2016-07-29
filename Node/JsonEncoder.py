import json

class json_encoder(json.JSONEncoder):
    def encode(self, obj):

        obj['ip_address'] = str(obj['ip_address'])
        obj['public_key'] = obj['public_key']._asdict()
        obj['private_key'] = obj['private_key']._asdict()
        obj['is_disabled'] = str(obj['is_disabled'])

        return super(json_encoder, self).encode(obj)

class tx_json_encoder(json.JSONEncoder):
    def encode(self, obj):
        obj['timestamp'] = str(obj['timestamp'])
        obj['senderpublickey'] = obj['senderpublickey']
        obj['value'] = obj['value']

        return super(json_encoder, self).encode(obj)