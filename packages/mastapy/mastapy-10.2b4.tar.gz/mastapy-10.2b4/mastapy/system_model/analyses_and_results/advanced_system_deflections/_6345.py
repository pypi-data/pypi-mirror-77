﻿'''_6345.py

PointLoadAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2036
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6192
from mastapy.system_model.analyses_and_results.system_deflections import _2323
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6381
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'PointLoadAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadAdvancedSystemDeflection',)


class PointLoadAdvancedSystemDeflection(_6381.VirtualComponentAdvancedSystemDeflection):
    '''PointLoadAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2036.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2036.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6192.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6192.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2323.PointLoadSystemDeflection]':
        '''List[PointLoadSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2323.PointLoadSystemDeflection))
        return value
