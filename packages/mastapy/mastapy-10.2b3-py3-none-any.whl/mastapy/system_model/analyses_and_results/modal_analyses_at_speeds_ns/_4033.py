﻿'''_4033.py

CylindricalGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2089
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6122
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4032, _4031, _4044
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'CylindricalGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetModalAnalysesAtSpeeds',)


class CylindricalGearSetModalAnalysesAtSpeeds(_4044.GearSetModalAnalysesAtSpeeds):
    '''CylindricalGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2089.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2089.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6122.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6122.CylindricalGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def cylindrical_gears_modal_analyses_at_speeds(self) -> 'List[_4032.CylindricalGearModalAnalysesAtSpeeds]':
        '''List[CylindricalGearModalAnalysesAtSpeeds]: 'CylindricalGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsModalAnalysesAtSpeeds, constructor.new(_4032.CylindricalGearModalAnalysesAtSpeeds))
        return value

    @property
    def cylindrical_meshes_modal_analyses_at_speeds(self) -> 'List[_4031.CylindricalGearMeshModalAnalysesAtSpeeds]':
        '''List[CylindricalGearMeshModalAnalysesAtSpeeds]: 'CylindricalMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesModalAnalysesAtSpeeds, constructor.new(_4031.CylindricalGearMeshModalAnalysesAtSpeeds))
        return value
