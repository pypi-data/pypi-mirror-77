﻿'''_5042.py

FaceGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2092
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6142
from mastapy.system_model.analyses_and_results.mbd_analyses import _5041, _5040, _5047
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'FaceGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetMultiBodyDynamicsAnalysis',)


class FaceGearSetMultiBodyDynamicsAnalysis(_5047.GearSetMultiBodyDynamicsAnalysis):
    '''FaceGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2092.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2092.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6142.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6142.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5041.FaceGearMultiBodyDynamicsAnalysis]':
        '''List[FaceGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5041.FaceGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def face_gears_multi_body_dynamics_analysis(self) -> 'List[_5041.FaceGearMultiBodyDynamicsAnalysis]':
        '''List[FaceGearMultiBodyDynamicsAnalysis]: 'FaceGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsMultiBodyDynamicsAnalysis, constructor.new(_5041.FaceGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def face_meshes_multi_body_dynamics_analysis(self) -> 'List[_5040.FaceGearMeshMultiBodyDynamicsAnalysis]':
        '''List[FaceGearMeshMultiBodyDynamicsAnalysis]: 'FaceMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesMultiBodyDynamicsAnalysis, constructor.new(_5040.FaceGearMeshMultiBodyDynamicsAnalysis))
        return value
