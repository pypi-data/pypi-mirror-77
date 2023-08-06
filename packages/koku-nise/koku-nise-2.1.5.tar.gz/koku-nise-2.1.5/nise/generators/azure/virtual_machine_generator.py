#
# Copyright 2018 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Module for azure bandwidth data generation."""
from nise.generators.azure.azure_generator import AzureGenerator


class VMGenerator(AzureGenerator):
    """Generator for Virtual Machine data."""

    SERVICE_METER = (("A Series", "A Series", "A0", "100 Hours"), ("BS Series", "BS Series", "B2s", ""))
    SERVICE_INFO_2 = ("Canonical", "")
    EXAMPLE_RESOURCE = (
        ("RG1", "mysa1"),
        ("RG1", "costmgmtacct1234"),
        ("RG2", "mysa1"),
        ("RG2", "costmgmtacct1234"),
        ("costmgmt", "mysa1"),
        ("costmgmt", "costmgmtacct1234"),
        ("hccm", "mysa1"),
        ("hccm", "costmgmtacct1234"),
    )
    ADDITIONAL_INFO = (
        {
            "ImageType": "Canonical",
            "ServiceType": "Standard_A0",
            "VMName": None,
            "VMProperties": None,
            "VCPUs": 1,
            "UsageType": "ComputeHR",
        },
        {
            "UsageType": "ComputeHR",
            "ImageType": "Canonical",
            "ServiceType": "Standard_B2s",
            "VMName": None,
            "VMProperties": "Microsoft.AKS.Compute.AKS.Linux.Billing",
            "VCPUs": 2,
        },
    )
    SERVICE_NAME = "Virtual Machines"

    def _gen_fake_data(self, count):
        """Populate TEMPLATE_KWARGS with fake values.

        The base template has defaults for most values. The values set here have extra requirements.
        """
        self.TEMPLATE_KWARGS["vmachine_gens"] = []
        while len(self.TEMPLATE_KWARGS["vmachine_gens"]) < count:
            # this might look strange, but because the Azure template has defaults for each element, we don't need to
            # populate the dict with anything. The list just needs to have the right number of elements.
            #
            # If a future change needs to push default values into the template, the values may be added here.
            self.TEMPLATE_KWARGS["vmachine_gens"].append({})
