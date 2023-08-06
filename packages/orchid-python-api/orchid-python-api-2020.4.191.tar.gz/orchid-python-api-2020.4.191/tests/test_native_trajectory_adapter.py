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

import deal
from hamcrest import assert_that, equal_to, empty, contains_exactly

from orchid.native_trajectory_adapter import NativeTrajectoryAdapter
from orchid.net_quantity import unit_abbreviation_to_unit
from tests.stub_net import create_stub_net_project, create_stub_net_trajectory_array

# noinspection PyUnresolvedReferences
from System import Convert

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWellTrajectory, WellReferenceFrameXy

# noinspection PyUnresolvedReferences
import UnitsNet


# Test ideas
# - No, empty or all whitespace reference frame
# - Unrecognized reference frame
class TestNativeTrajectoryAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_get_easting_array_if_empty_easting_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        expected_eastings = []
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_eastings', return_value=expected_eastings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_easting_array('well_head'), empty())

    def test_get_northing_array_if_empty_northing_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        expected_northings = []
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_northings',
                                                                  return_value=expected_northings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_northing_array('absolute'), empty())

    def test_get_easting_array_if_one_item_easting_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='m')
        expected_easting_magnitudes = [789921]
        actual_eastings = create_stub_net_trajectory_array(expected_easting_magnitudes,
                                                           unit_abbreviation_to_unit('m'))
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_eastings', return_value=actual_eastings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_easting_array('absolute'), contains_exactly(*expected_easting_magnitudes))

    def test_get_northing_array_if_one_item_northing_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='ft')
        expected_northing_magnitudes = [6936068]
        actual_northings = create_stub_net_trajectory_array(expected_northing_magnitudes,
                                                            unit_abbreviation_to_unit('ft'))
        stub_trajectory.GetNorthingArray = unittest.mock.MagicMock(name='stub_northings',
                                                                   return_value=actual_northings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_northing_array('project'), contains_exactly(*expected_northing_magnitudes))

    def test_get_easting_array_if_many_items_easting_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='ft')
        expected_easting_magnitudes = [501040, 281770, 289780]
        actual_eastings = create_stub_net_trajectory_array(expected_easting_magnitudes, unit_abbreviation_to_unit('ft'))
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_eastings', return_value=actual_eastings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_easting_array('absolute'), contains_exactly(*expected_easting_magnitudes))

    def test_get_northing_array_if_many_items_northing_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='ft')
        expected_northing_magnitudes = [8332810, 2537900, 9876464]
        actual_northings = create_stub_net_trajectory_array(expected_northing_magnitudes,
                                                            unit_abbreviation_to_unit('ft'))
        stub_trajectory.GetNorthingArray = unittest.mock.MagicMock(name='stub_northings',
                                                                   return_value=actual_northings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_northing_array('well_head'), contains_exactly(*expected_northing_magnitudes))

    def test_send_correct_reference_frame_to_get_easting_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        # When debugging
        # - WellReferenceFrameXy.AbsoluteStatePlane = 0
        # - WellReferenceFrameXy.Project = 1
        # - WellReferenceFrameXy.WellHead = 2
        for (text_reference_frame, net_reference_frame) in [('absolute', WellReferenceFrameXy.AbsoluteStatePlane),
                                                            ('project', WellReferenceFrameXy.Project),
                                                            ('well_head', WellReferenceFrameXy.WellHead)]:
            with self.subTest(text_reference_frame=text_reference_frame, net_reference_frame=net_reference_frame):
                mock_get_easting_array = unittest.mock.MagicMock(name='stub_eastings', return_value=[])
                stub_trajectory.GetEastingArray = mock_get_easting_array
                sut.get_easting_array(text_reference_frame)
                mock_get_easting_array.assert_called_once_with(net_reference_frame)

    def test_send_correct_reference_frame_to_get_northing_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        # When debugging
        # - WellReferenceFrameXy.AbsoluteStatePlane = 0
        # - WellReferenceFrameXy.Project = 1
        # - WellReferenceFrameXy.WellHead = 2
        for (text_reference_frame, net_reference_frame) in [('absolute', WellReferenceFrameXy.AbsoluteStatePlane),
                                                            ('project', WellReferenceFrameXy.Project),
                                                            ('well_head', WellReferenceFrameXy.WellHead)]:
            with self.subTest(text_reference_frame=text_reference_frame, net_reference_frame=net_reference_frame):
                mock_get_northing_array = unittest.mock.MagicMock(name='stub_northings', return_value=[])
                stub_trajectory.GetNorthingArray = mock_get_northing_array
                sut.get_northing_array(text_reference_frame)
                mock_get_northing_array.assert_called_once_with(net_reference_frame)

    def test_send_correct_length_unit_to_get_easting_array_if_no_length_unit_specified(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='m')
        sut = NativeTrajectoryAdapter(stub_trajectory)
        mock_get_easting_array = unittest.mock.MagicMock(name='stub_eastings', return_value=[])
        stub_trajectory.GetEastingArray = mock_get_easting_array
        sut.get_easting_array('absolute')

        mock_get_easting_array.assert_called_once_with(WellReferenceFrameXy.AbsoluteStatePlane)

    def test_send_correct_length_unit_to_get_northing_array_if_no_length_unit_specified(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='m')
        sut = NativeTrajectoryAdapter(stub_trajectory)
        mock_get_northing_array = unittest.mock.MagicMock(name='stub_northings', return_value=[])
        stub_trajectory.GetNorthingArray = mock_get_northing_array
        sut.get_northing_array('absolute')

        mock_get_northing_array.assert_called_once_with(WellReferenceFrameXy.AbsoluteStatePlane)

    def test_get_xyz_array_invalid_reference_frame_raises_exception(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        for method_to_test in [sut.get_easting_array, sut.get_northing_array]:
            for invalid_reference_frame in [None, '', '\f']:
                with(self.subTest(method_to_test=method_to_test, invalid_well_id=invalid_reference_frame)):
                    self.assertRaises(deal.PreContractError, method_to_test, invalid_reference_frame)

    def test_get_xyz_array_unrecognized_reference_frame_raises_exception(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        for method_to_test in [sut.get_easting_array, sut.get_northing_array]:
            with(self.subTest(method_to_test=method_to_test)):
                # noinspection SpellCheckingInspection
                self.assertRaises(deal.PreContractError, method_to_test, 'well_heaf')


if __name__ == '__main__':
    unittest.main()
