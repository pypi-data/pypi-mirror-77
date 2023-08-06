#  Copyright 2017-2020 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#

import unittest.mock

from hamcrest import assert_that, equal_to
import toolz.curried as toolz

from orchid.project import Project
from orchid.project_loader import ProjectLoader
from tests.stub_net import create_stub_net_project


class TestProjectUnits(unittest.TestCase):

    def test_returns_correct_unit_for_project(self):
        about_units = [('length', 'project_length_unit_abbreviation', ('ft', 'm'), ('ft', 'm')),
                       ('mass', 'project_mass_unit_abbreviation', ('lb', 'kg'), ('lb', 'kg')),
                       ('pressure', 'project_pressure_unit_abbreviation', ('psi', 'kPa'), ('psi', 'kPa')),
                       ('slurry rate', 'slurry_rate_unit_abbreviation',
                        ('bbl/min', 'm^3/min'), ('bbl/min', 'm\u00b3/min')),
                       ('proppant concentration', 'proppant_concentration_unit_abbreviation',
                        ('lb/gal (U.S.)', 'kg/m^3'), ('lb/gal (U.S.)', 'kg/m\u00b3')),
                       ('temperature', 'project_temperature_unit_abbreviation', ('F', 'C'), ('\u00b0F', '\u00b0C'))]
        default_options = {'well_names': ['dont-care-well']}
        for quantity, abbreviation_name, abbreviations, units in about_units:
            for abbreviation, unit in zip(abbreviations, units):
                with self.subTest(unit=unit):
                    options = toolz.assoc(default_options, abbreviation_name, abbreviation)
                    stub_net_project = create_stub_net_project(**options)
                    sut = create_sut(stub_net_project)

                    assert_that(sut.unit(quantity), equal_to(unit))


def create_sut(stub_net_project):
    patched_loader = ProjectLoader('dont_care')
    patched_loader.native_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = Project(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
