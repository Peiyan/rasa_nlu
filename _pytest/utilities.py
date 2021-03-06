import tempfile

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.server import __create_interpreter
from rasa_nlu.train import do_train


def base_test_conf(backend):
    return {
        'write': temp_log_file_location(),
        'port': 5022,
        "backend": backend,
        "path": tempfile.mkdtemp(),
        "data": "./data/examples/rasa/demo-rasa.json"
    }


def interpreter_for(config):
    (trained, path) = run_train(config)
    interpreter = load_interpreter_for_model(config, path)
    return interpreter


def temp_log_file_location():
    return tempfile.mkstemp(suffix="_rasa_nlu_logs.json")[1]


def run_train(_config):
    config = RasaNLUConfig(cmdline_args=_config)
    (trained, path) = do_train(config)
    return trained, path


def load_interpreter_for_model(config, persisted_path):
    config['server_model_dir'] = persisted_path
    return __create_interpreter(config)
