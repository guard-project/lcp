from string import Formatter as StringFormatter


class Formatter(StringFormatter):
    def convert_field(self, value, conversion):
        if conversion == 'c':
            return value.capitalize()
        else:
            return super().convert_field(value, conversion)


format = Formatter().format


def is_str(obj):
    return isinstance(obj, str)
