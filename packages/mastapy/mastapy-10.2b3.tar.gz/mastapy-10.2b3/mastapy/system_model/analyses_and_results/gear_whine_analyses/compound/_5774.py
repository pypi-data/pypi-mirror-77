﻿'''_5774.py

PulleyCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2148
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5382
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5729
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'PulleyCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundGearWhineAnalysis',)


class PulleyCompoundGearWhineAnalysis(_5729.CouplingHalfCompoundGearWhineAnalysis):
    '''PulleyCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2148.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2148.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5382.PulleyGearWhineAnalysis]':
        '''List[PulleyGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5382.PulleyGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5382.PulleyGearWhineAnalysis]':
        '''List[PulleyGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5382.PulleyGearWhineAnalysis))
        return value
