﻿'''_637.py

ConicalGearBendingStiffness
'''


from mastapy.gears.ltca import _612
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_BENDING_STIFFNESS = python_net_import('SMT.MastaAPI.Gears.LTCA.Conical', 'ConicalGearBendingStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearBendingStiffness',)


class ConicalGearBendingStiffness(_612.GearBendingStiffness):
    '''ConicalGearBendingStiffness

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_BENDING_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearBendingStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
