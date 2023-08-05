# coding=utf-8

import os
from os.path import dirname, isfile, join

_template_folder = join(dirname(__file__), 'templates')


def load_config(fname, **kwargs) -> dict:
    if fname is None or not isfile(fname):
        raise FileNotFoundError("Cannot find configuration file '{}'".format(fname))
    code = compile(open(fname, 'rb').read(), fname, 'exec')
    cfg = {
        "__builtins__": __builtins__,
        "__name__": "__config__",
        "__file__": fname,
        "__doc__": None,
        "__package__": None
    }
    cfg.update(kwargs)
    exec(code, cfg, cfg)
    return cfg


def load_profile_config(conf_dir, name, profiles=None, **kwargs) -> dict:
    pc = load_config(join(conf_dir, name + '.py'), **kwargs)
    if profiles:
        profiles = profiles.split(',')
        for profile in reversed(profiles):
            if profile:
                pc_file = join(conf_dir, name + '_' + profile + '.py')
                if isfile(pc_file):
                    c = load_config(pc_file, **kwargs)
                    _update_config(pc, c)
        pc['active_profiles'] = list(profiles)
    return pc


def _update_config(old: dict, new: dict):
    for k, v in new.items():
        if k not in old:
            old[k] = v
        else:
            if isinstance(v, dict) and isinstance(old[k], dict):
                _update_config(old[k], v)
            else:
                old[k] = v


def load_app_settings(app_name) -> dict:
    c = {}
    conf_dir = os.environ.get('GUNIFLASK_CONF_DIR')
    active_profiles = os.environ.get('GUNIFLASK_ACTIVE_PROFILES')
    kwargs = get_constant_settings_from_env()
    if conf_dir:
        c = load_profile_config(conf_dir, app_name, profiles=active_profiles, **kwargs)
    # builtin settings should not be changed
    _update_config(c, kwargs)
    s = {}
    for name in c:
        if not name.startswith('_'):
            s[name] = c[name]
    return s


def get_constant_settings_from_env() -> dict:
    kwargs = {'home': os.environ.get('GUNIFLASK_HOME'),
              'project_name': os.environ.get('GUNIFLASK_PROJECT_NAME')}
    if os.environ.get('GUNIFLASK_DEBUG'):
        kwargs['debug'] = True
    else:
        kwargs['debug'] = False
    kwargs['host'] = os.environ.get('GUNIFLASK_HOST')
    port = os.environ.get('GUNIFLASK_PORT')
    if port:
        port = int(port)
    kwargs['port'] = port
    return kwargs
