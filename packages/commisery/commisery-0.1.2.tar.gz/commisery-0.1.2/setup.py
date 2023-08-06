# Copyright (c) 2018 - 2020 TomTom N.V. (https://tomtom.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(
    name='commisery',
    packages=('commisery',),
    py_modules=('commisery',),
    python_requires='>=3.6.5',
    install_requires=(
      'regex',
      'stemming>=1,<2',
    ),
    setup_requires=(
      'pytest-runner',
      'setuptools_scm',
      'setuptools_scm_git_archive',
    ),
    tests_require=(
      'pytest',
    ),
    use_scm_version={"relative_to": __file__},
    entry_points={
      'console_scripts': [
        'commisery-verify-msg = commisery.checking:main',
      ],
    },
    zip_safe=True,
    project_urls={
      'Source Code': 'https://github.com/tomtom-international/commisery',
    },
    classifiers=(
      'License :: OSI Approved :: Apache Software License',
    ),
    license='Apache License 2.0',
    license_file='LICENSE',
)
