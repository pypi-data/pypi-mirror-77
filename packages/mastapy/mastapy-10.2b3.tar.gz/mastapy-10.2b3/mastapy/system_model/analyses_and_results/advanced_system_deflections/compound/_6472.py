﻿'''_6472.py

RollingRingCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2154
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6348
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _6425
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'RollingRingCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundAdvancedSystemDeflection',)


class RollingRingCompoundAdvancedSystemDeflection(_6425.CouplingHalfCompoundAdvancedSystemDeflection):
    '''RollingRingCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2154.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2154.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6348.RollingRingAdvancedSystemDeflection]':
        '''List[RollingRingAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6348.RollingRingAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_6348.RollingRingAdvancedSystemDeflection]':
        '''List[RollingRingAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_6348.RollingRingAdvancedSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundAdvancedSystemDeflection]':
        '''List[RollingRingCompoundAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundAdvancedSystemDeflection))
        return value
