import json


class json_encoder(json.JSONEncoder):
    def encode(self, obj):
        obj['type'] = str(obj['type'])
        obj['ip_address'] = str(obj['ip_address'])
        obj['public_key'] = str(obj['public_key'])
        obj['private_key'] = str(obj['private_key'])
        obj['address'] = str(obj['address'])

        return super(json_encoder, self).encode(obj)


'''JSON encoder for node information '''


class json_encoder_send(json.JSONEncoder):
    def encode(self, obj):
        obj['type'] = str(obj['type'])
        obj['ip_address'] = str(obj['ip_address'])

        return super(json_encoder_send, self).encode(obj)


class tx_json_encoder(json.JSONEncoder):
    def encode(self, obj):
        obj['timestamp'] = str(obj['timestamp'])
        obj['senderpublickey'] = obj['senderpublickey']
        obj['value'] = obj['value']

        return super(json_encoder, self).encode(obj)