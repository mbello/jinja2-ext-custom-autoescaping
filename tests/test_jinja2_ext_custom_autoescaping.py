from jinja2_ext_custom_autoescaping import __version__
from jinja2_ext_custom_autoescaping import CustomAutoescapeExtension, enable_custom_autoescaping
from jinja2 import Environment, select_autoescape, FileSystemLoader


def my_filter(val):
    print(val)
    if isinstance(val, str):
        return val.replace(r"\\", r"\\\\")
    return val


def basic_test():

    # - select_autoescape is a closure
    # - enabled_extensions takes precedence over disabled_extensions, so an extension in both lists will be enabled
    # - You most likely do not want to have custom autoescaping on while built-in autoescaping is also on
    built_in_select_autoescape = select_autoescape(enabled_extensions=['html', 'htm', 'xml'],
                                                   disabled_extensions=['txt', 'tex'],
                                                   default_for_string=True,
                                                   default=True)

    custom_select_autoescape = select_autoescape(enabled_extensions=['tex', 'txt'],
                                                 disabled_extensions=[],
                                                 default_for_string=False,
                                                 default=False)
    
    # Just focusing on the important parts of your Environment construction.
    env = Environment(extensions=[CustomAutoescapeExtension],
                      loader=FileSystemLoader(['.']),
                      autoescape=built_in_select_autoescape)

    opts = {'custom_select_autoescape': custom_select_autoescape,
            'custom_autoescape_filter_name': 'my_filter',
            'custom_autoescape_filter_func': my_filter}

    # Register the filter and enables autoescaping
    enable_custom_autoescaping(env, **opts)
    
    template = env.get_template('test_template.txt')
    print(template.render(var={'entry 1': 'value 1', 'entry2': r'val\\ue 2'}))


def test_version():
    assert __version__ == '0.1.0'

basic_test()