﻿'''_5537.py

StraightBevelGearMeshSingleMeshWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1909
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6216
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5449
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'StraightBevelGearMeshSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshSingleMeshWhineAnalysis',)


class StraightBevelGearMeshSingleMeshWhineAnalysis(_5449.BevelGearMeshSingleMeshWhineAnalysis):
    '''StraightBevelGearMeshSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1909.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1909.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6216.StraightBevelGearMeshLoadCase':
        '''StraightBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6216.StraightBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
