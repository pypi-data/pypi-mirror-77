# TODO (SNMP trap, validate output config)

from functools import partial
from types import SimpleNamespace
from .beacons import beacon_eva_datapuller

oprint = partial(print, flush=True)

output_params = {}

_d = SimpleNamespace()


def output_devnull(*args, **kwargs):
    pass


def output_stdout(o, value):
    oprint(f'{o} {value}')


def output_stdout_ndjson(o, value):
    q = '' if isinstance(value, int) or isinstance(value, float) else '"'
    oprint(f'{{"id":"{o}","v":{q}{value}{q}}}')


def output_webhook(o, value):
    try:
        s = _d.webs
    except AttributeError:
        import requests
        _d.webs = requests.Session()
        s = _d.webs
    from pulr import config
    r = s.post(output_params['url'],
               json={
                   'id': o,
                   'v': value
               },
               headers=output_params.get('headers'),
               timeout=output_params['timeout'])
    if not r.ok:
        raise RuntimeError(
            f'webhook {output_params["url"]} response {r.status_code}')


def output_eva_datapuller(o, value):
    s = f'{o[0]} u '
    oprint(s + (str(value) if o[1] == 's' else f'None {value}'))


def send_beacon_eva_datapuller():
    oprint()


OUTPUT_METHODS = {
    'stdout': {
        'output': output_stdout
    },
    'stdout/ndjson': {
        'output': output_stdout_ndjson
    },
    'stdout/eva-datapuller': {
        'output': output_eva_datapuller,
        'beacon': beacon_eva_datapuller
    },
    'webhook': {
        'output': output_webhook
    }
}
