# Overview

Jinja2 extension to enable the use of any filter as a custom autoscape filter.

This package allows you to define rules to determine when your custom autoescaping filter will be
enabled using the same 'select_autoescape' method you already use to determine
when the built-in autoescaping filter is enabled.

# Usage
    from jinja2_ext_custom_autoescaping import CustomAutoescapeExtension, enable_custom_autoescaping
    from jinja2 import Environment, select_autoescape, FileSystemLoader

    # Your custom filter...        
    def my_filter(val):
        print(val)
        if isinstance(val, str):
            return val.replace(r"\\", r"\\\\")
        return val
    
        
    # Here you set the rules for when the built-in autoescaping will be enabled
    built_in_select_autoescape = select_autoescape(enabled_extensions=['html', 'htm', 'xml'],
                                                   disabled_extensions=['txt', 'tex'],
                                                   default_for_string=True,
                                                   default=True)

    # - select_autoescape is a closure
    # - enabled_extensions takes precedence over disabled_extensions, so an extension in both lists will be enabled
    # - You most likely do not want to have custom autoescaping on while built-in autoescaping is also on

    # Here you set the rules for when your custom autoescaping will be enabled
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
    
    # Now you are ready to go...
    template = env.get_template('test_template.txt')
    print(template.render(var={'entry 1': 'value 1', 'entry2': r'val\\ue 2'}))
