from setuptools import setup
from setup_dotnet import DotnetLib, BuildDotnet, PureWheel


setup(
    cmdclass={'build_ext': BuildDotnet, 'bdist_wheel': PureWheel},
    ext_modules={
        DotnetLib(
                   "elan-python-runtime",
                    "src/runtime/Python.Runtime.csproj",
                    output="elan_pythonnet/runtime",
        )
    }
)
