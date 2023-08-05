﻿'''_3910.py

CylindricalGearCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2088
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3788
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3920
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'CylindricalGearCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCompoundModalAnalysesAtStiffnesses',)


class CylindricalGearCompoundModalAnalysesAtStiffnesses(_3920.GearCompoundModalAnalysesAtStiffnesses):
    '''CylindricalGearCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2088.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3788.CylindricalGearModalAnalysesAtStiffnesses]':
        '''List[CylindricalGearModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3788.CylindricalGearModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3788.CylindricalGearModalAnalysesAtStiffnesses]':
        '''List[CylindricalGearModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_3788.CylindricalGearModalAnalysesAtStiffnesses))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearCompoundModalAnalysesAtStiffnesses]':
        '''List[CylindricalGearCompoundModalAnalysesAtStiffnesses]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearCompoundModalAnalysesAtStiffnesses))
        return value
