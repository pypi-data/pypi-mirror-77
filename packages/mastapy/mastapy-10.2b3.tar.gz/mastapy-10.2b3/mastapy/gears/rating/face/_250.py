﻿'''_250.py

FaceGearRating
'''


from mastapy.gears.gear_designs.face import _755
from mastapy._internal import constructor
from mastapy.gears.rating import _163
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Face', 'FaceGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearRating',)


class FaceGearRating(_163.GearRating):
    '''FaceGearRating

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_gear(self) -> '_755.FaceGearDesign':
        '''FaceGearDesign: 'FaceGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_755.FaceGearDesign)(self.wrapped.FaceGear) if self.wrapped.FaceGear else None
