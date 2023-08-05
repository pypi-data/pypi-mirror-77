#!/usr/bin/env python3
# thoth-adviser
# Copyright(C) 2019, 2020 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A step to filter out packages that are pinned to a specific version."""

import logging
from typing import Optional
from typing import Dict
from typing import Any
from typing import Generator
from typing import TYPE_CHECKING

import attr
from thoth.python import PackageVersion

from ..sieve import Sieve

if TYPE_CHECKING:
    from ..pipeline_builder import PipelineBuilderContext

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class CutLockedSieve(Sieve):
    """Cut-off packages that are locked to a specific version.

    If a project pins down a package to a specific release, respect that. Otherwise
    resolver does not need to find any resolved stack, especially considering only
    N latest versions and the pinned version is >=N+1 version.
    """

    @classmethod
    def should_include(cls, builder_context: "PipelineBuilderContext") -> Optional[Dict[str, Any]]:
        """Include cut-locked pipeline sieve for adviser or Dependency Monkey, always."""
        if not builder_context.is_included(cls):
            return {}

        return None

    def run(self, package_versions: Generator[PackageVersion, None, None]) -> Generator[PackageVersion, None, None]:
        """Cut-off locked versions to a specific version."""
        packages = self.context.project.pipfile.packages.packages
        dev_packages = self.context.project.pipfile.dev_packages.packages

        for package_version in package_versions:
            direct_package = packages.get(package_version.name)
            direct_dev_package = dev_packages.get(package_version.name)

            if direct_package is None and direct_dev_package is None:
                yield package_version

            if (
                direct_package
                and direct_package.is_locked()
                and direct_package.locked_version != package_version.locked_version
            ) or (
                direct_dev_package
                and direct_dev_package.is_locked()
                and direct_dev_package.locked_version != package_version.locked_version
            ):
                _LOGGER.debug(
                    "Removing package %s - it does not correspond to package version locked by direct dependencies",
                    package_version.to_tuple(),
                )
                continue

            yield package_version
