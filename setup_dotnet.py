import os
from typing import List, Any
from setuptools import Extension, Command

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class PureWheel(_bdist_wheel):
        root_is_pure: bool

        def finalize_options(self):
            super().finalize_options()
            self.root_is_pure = True
except ImportError:
    _bdist_wheel = None
    PureWheel = None


class DotnetLib(Extension):
    def __init__(self, name, path, output, **kwargs):
        self.path = path
        self.args = kwargs
        self.output = output
        super().__init__(name, sources=[])


class BuildDotnet(Command):
    """Build command for dotnet-cli based builds"""
    # required for Command to be run successfully
    extensions: List[Any] = []
    build_dir: str
    inplace: bool
    dotnet_config: str

    description = 'Build DLLs with dotnet-cli'
    user_options = [('dotnet-config=', None, 'dotnet build configuration')]

    def initialize_options(self):
        self.inplace = True
        self.dotnet_config = "release"
        pass

    def finalize_options(self):
        self.build_dir = self.get_finalized_command('build').build_lib
        pass

    # noinspection PyMethodMayBeStatic
    def get_source_files(self):
        return []

    def run(self):
        for lib in self.distribution.ext_modules:
            self.build(lib)

    def build(self, lib):
        if self.inplace:
            dotnet_build_dir = lib.output
        else:
            dotnet_build_dir = os.path.join(self.build_dir, lib.output)
        print(f'Building dotnet in {lib.path} ({self.dotnet_config}) to {dotnet_build_dir}')

        opts = sum(
            [
                ['--' + name.replace('_', '-'), value]
                for name, value in lib.args.items()
            ],
            [],
        )
        opts.append('--configuration')
        opts.append(self.dotnet_config)
        opts.append('--output')
        opts.append(dotnet_build_dir)
        self.spawn(['dotnet', 'build', lib.path] + opts)
