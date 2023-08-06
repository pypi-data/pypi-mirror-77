﻿'''_6272.py

BevelDifferentialGearMeshAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1883
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6085
from mastapy.gears.rating.bevel import _340
from mastapy.gears.rating.zerol_bevel import _171
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.straight_bevel import _201
from mastapy.gears.rating.spiral_bevel import _204
from mastapy.system_model.analyses_and_results.system_deflections import _2241
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6277
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'BevelDifferentialGearMeshAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshAdvancedSystemDeflection',)


class BevelDifferentialGearMeshAdvancedSystemDeflection(_6277.BevelGearMeshAdvancedSystemDeflection):
    '''BevelDifferentialGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1883.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1883.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6085.BevelDifferentialGearMeshLoadCase':
        '''BevelDifferentialGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6085.BevelDifferentialGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_340.BevelGearMeshRating':
        '''BevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _340.BevelGearMeshRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to BevelGearMeshRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_zerol_bevel_gear_mesh_rating(self) -> '_171.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _171.ZerolBevelGearMeshRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to ZerolBevelGearMeshRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_straight_bevel_gear_mesh_rating(self) -> '_201.StraightBevelGearMeshRating':
        '''StraightBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _201.StraightBevelGearMeshRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to StraightBevelGearMeshRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_spiral_bevel_gear_mesh_rating(self) -> '_204.SpiralBevelGearMeshRating':
        '''SpiralBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _204.SpiralBevelGearMeshRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SpiralBevelGearMeshRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2241.BevelDifferentialGearMeshSystemDeflection]':
        '''List[BevelDifferentialGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2241.BevelDifferentialGearMeshSystemDeflection))
        return value
