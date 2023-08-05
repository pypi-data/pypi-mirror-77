﻿'''_3551.py

ImportedFEComponentParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2023
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6163
from mastapy.system_model.analyses_and_results.system_deflections import _2299
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3488
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ImportedFEComponentParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentParametricStudyTool',)


class ImportedFEComponentParametricStudyTool(_3488.AbstractShaftOrHousingParametricStudyTool):
    '''ImportedFEComponentParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2023.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2023.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6163.ImportedFEComponentLoadCase':
        '''ImportedFEComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6163.ImportedFEComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ImportedFEComponentParametricStudyTool]':
        '''List[ImportedFEComponentParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentParametricStudyTool))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2299.ImportedFEComponentSystemDeflection]':
        '''List[ImportedFEComponentSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2299.ImportedFEComponentSystemDeflection))
        return value
