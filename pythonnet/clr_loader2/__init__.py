from clr_loader import Runtime, _maybe_path, find_dotnet_root, StrOrPath
from .util.runtime_spec import DotnetCoreRuntimeCommandLine
from typing import Optional, Dict


def get_coreclr_command_line(
    *,
    entry_dll: StrOrPath,
    dotnet_root: Optional[StrOrPath] = None,
    properties: Optional[Dict[str, str]] = None
) -> Runtime:
    """Get a CoreCLR (.NET Core) runtime instance

    The returned ``DotnetCoreRuntimeCommandLine`` also acts as a mapping of the config
    properties. They can be retrieved using the index operator and can be
    written until the runtime is initialized. The runtime is initialized when
    the first function object is retrieved.

    :param entry_dll:
        The path to the entry dll.
    :param dotnet_root:
        The root directory of the .NET Core installation. If this is not
        specified, we try to discover it using :py:func:`find_dotnet_root`.
    :param properties:
        Additional runtime properties. These can also be passed using the
        ``configProperties`` section in the runtime config."""
    dotnet_root = _maybe_path(dotnet_root)
    if dotnet_root is None:
        dotnet_root = find_dotnet_root()

    impl = DotnetCoreRuntimeCommandLine(entry_dll=_maybe_path(entry_dll), dotnet_root=dotnet_root)
    if properties:
        for key, value in properties.items():
            impl[key] = value

    return impl
