import jinja2.ext
from jinja2.lexer import Token


def enable_custom_autoescaping(env: jinja2.Environment,
                               custom_select_autoescape: callable,
                               custom_autoescape_filter_name: str,
                               custom_autoescape_filter_func: callable):
    # register the filter
    env.filters[custom_autoescape_filter_name] = custom_autoescape_filter_func
    env.extend(**{'custom_autoescape_filter_name': custom_autoescape_filter_name})
    env.extend(**{'custom_select_autoescape': custom_select_autoescape})
    

class CustomAutoescapeExtension(jinja2.ext.Extension):
    def __init__(self, environment: jinja2.environment.Environment):
        super().__init__(environment)
        self.environment = environment
        self.custom_autoescape_enabled = False

    def parse(self, parser):
        pass

    # This is based on https://github.com/indico/indico/blob/master/indico/web/flask/templating.py.
    def filter_stream(self, stream):
        if not self.custom_autoescape_enabled:
            if hasattr(self.environment, 'custom_autoescape_filter_name'):
                if hasattr(self.environment, 'custom_select_autoescape'):
                    self.custom_autoescape_enabled = True
        
        autoescape = self.custom_autoescape_enabled and self.environment.custom_select_autoescape(stream.name)
        
        for token in stream:
            if token.type == 'variable_end' and autoescape:
                yield Token(token.lineno, 'pipe', '|')
                yield Token(token.lineno, 'name', self.environment.custom_autoescape_filter_name)
            yield token
