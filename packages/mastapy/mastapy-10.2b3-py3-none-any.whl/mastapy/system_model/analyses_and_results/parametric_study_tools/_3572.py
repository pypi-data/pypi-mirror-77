﻿'''_3572.py

ParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools import _3573
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6225, _6211
from mastapy.system_model.analyses_and_results.analysis_cases import _6509
from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyTool',)


class ParametricStudyTool(_6509.AnalysisCase):
    '''ParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def parametric_analysis_options(self) -> '_3573.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3573.ParametricStudyToolOptions)(self.wrapped.ParametricAnalysisOptions) if self.wrapped.ParametricAnalysisOptions else None

    @property
    def time_series_load_case(self) -> '_6225.TimeSeriesLoadCase':
        '''TimeSeriesLoadCase: 'TimeSeriesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6225.TimeSeriesLoadCase)(self.wrapped.TimeSeriesLoadCase) if self.wrapped.TimeSeriesLoadCase else None

    @property
    def load_case(self) -> '_6211.StaticLoadCase':
        '''StaticLoadCase: 'LoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6211.StaticLoadCase)(self.wrapped.LoadCase) if self.wrapped.LoadCase else None
