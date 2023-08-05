﻿'''_3123.py

BevelDifferentialGearCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2078
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3000
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3128
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'BevelDifferentialGearCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearCompoundSteadyStateSynchronousResponse',)


class BevelDifferentialGearCompoundSteadyStateSynchronousResponse(_3128.BevelGearCompoundSteadyStateSynchronousResponse):
    '''BevelDifferentialGearCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2078.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2078.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3000.BevelDifferentialGearSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3000.BevelDifferentialGearSteadyStateSynchronousResponse))
        return value

    @property
    def component_steady_state_synchronous_response_load_cases(self) -> 'List[_3000.BevelDifferentialGearSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSteadyStateSynchronousResponse]: 'ComponentSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseLoadCases, constructor.new(_3000.BevelDifferentialGearSteadyStateSynchronousResponse))
        return value
