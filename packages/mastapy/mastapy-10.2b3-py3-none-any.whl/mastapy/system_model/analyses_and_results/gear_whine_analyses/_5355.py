﻿'''_5355.py

HypoidGearMeshGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1897
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6161
from mastapy.system_model.analyses_and_results.system_deflections import _2296
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5280
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'HypoidGearMeshGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshGearWhineAnalysis',)


class HypoidGearMeshGearWhineAnalysis(_5280.AGMAGleasonConicalGearMeshGearWhineAnalysis):
    '''HypoidGearMeshGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1897.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1897.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6161.HypoidGearMeshLoadCase':
        '''HypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6161.HypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2296.HypoidGearMeshSystemDeflection':
        '''HypoidGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2296.HypoidGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
