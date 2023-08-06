from enum import Enum
from typing import Any, Callable, Dict
from inspect import Parameter, signature
import functools

import click
from click_help_colors import HelpColorsCommand

"""
# TODO

- [ ] Enum support.
- [ ] Parse python docstring to display help.
"""

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    max_content_width=120,
)
DEFAULT_COLOR_OPTIONS = dict(
    help_headers_color='white',
    help_options_color='cyan',
)


def get_enum_map(f: Callable[..., None]) -> Dict[str, Dict[str, Any]]:
    sig = signature(f)

    # pick enum from signature
    enum_map: Dict[str, Dict[str, Any]] = {}
    for param in sig.parameters.values():
        if issubclass(param.annotation, Enum):
            enum_class = param.annotation
            enum_map.setdefault(param.name, {})
            for enum_entry in enum_class:
                enum_map[param.name][enum_entry.value] = enum_entry
    return enum_map


def water_wrap(
    f: Callable[..., None],
    enum_map: Dict[str, Dict[str, Any]],
) -> Callable[..., None]:
    """
    Return the new function which is click-compatible
    (has no enum signature arguments) from the arbitrary water compatible
    function
    """

    # Implemented the argument convert logic
    @functools.wraps(f)
    def wrapped(*args: Any, **kwargs: Any) -> None:
        # convert args and kwargs
        converted_kwargs = {}
        for name, value in kwargs.items():
            if name in enum_map:
                converted_kwargs[name] = enum_map[name][value]
            else:
                converted_kwargs[name] = value

        return f(*args, **converted_kwargs)

    return wrapped


def _get_click_command(f: Callable[..., None]) -> click.BaseCommand:
    docstring = f.__doc__
    if docstring:
        description = '\n'.join(docstring.splitlines()[:2])
        f.__doc__ = description
    sig = signature(f)
    enum_map = get_enum_map(f)
    click_f: Any = water_wrap(f, enum_map)
    for param in sig.parameters.values():
        if param.name.startswith('_'):
            # Positional argument
            click_f = click.argument(
                param.name,
                type=param.annotation,
                nargs=1,
            )(click_f)
        else:
            if param.default == Parameter.empty:
                common_kwargs = dict(required=True)
            else:
                common_kwargs = dict()
            if param.annotation == bool:
                # Boolean flag
                click_f = click.option(  # type: ignore
                    '--' + param.name.replace('_', '-'),
                    is_flag=True,
                    type=bool,
                    **common_kwargs,
                )(click_f)
            elif param.annotation == str or param.annotation == int:
                # string or boolean option
                click_f = click.option(  # type: ignore
                    '--' + param.name.replace('_', '-'),
                    type=param.annotation,
                    **common_kwargs,
                )(click_f)
            elif issubclass(param.annotation, Enum):
                click_f = click.option(  # type: ignore
                    '--' + param.name.replace('_', '-'),
                    type=click.Choice(enum_map[param.name].keys()),
                    **common_kwargs,
                )(click_f)

    return click.command(  # type: ignore
        cls=HelpColorsCommand,
        context_settings=CONTEXT_SETTINGS,
        **DEFAULT_COLOR_OPTIONS,  # type: ignore
    )(click_f)


def water(f: Callable[..., None]) -> None:
    """
    Main function making function to command line entrypoint
    """
    _get_click_command(f)()
