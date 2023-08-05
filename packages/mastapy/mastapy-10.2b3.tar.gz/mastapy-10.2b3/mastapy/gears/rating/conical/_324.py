﻿'''_324.py

ConicalGearDutyCycleRating
'''


from typing import List

from mastapy.gears.rating.conical import _327, _326
from mastapy._internal import constructor, conversion
from mastapy.gears.rating import _161, _160
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Conical', 'ConicalGearDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearDutyCycleRating',)


class ConicalGearDutyCycleRating(_160.GearDutyCycleRating):
    '''ConicalGearDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_design_duty_cycle(self) -> '_327.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_327.ConicalGearSetDutyCycleRating)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def conical_gear_set_design_duty_cycle(self) -> '_327.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'ConicalGearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_327.ConicalGearSetDutyCycleRating)(self.wrapped.ConicalGearSetDesignDutyCycle) if self.wrapped.ConicalGearSetDesignDutyCycle else None

    @property
    def left_flank_rating(self) -> '_161.GearFlankRating':
        '''GearFlankRating: 'LeftFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_161.GearFlankRating)(self.wrapped.LeftFlankRating) if self.wrapped.LeftFlankRating else None

    @property
    def concave_flank_rating(self) -> '_161.GearFlankRating':
        '''GearFlankRating: 'ConcaveFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_161.GearFlankRating)(self.wrapped.ConcaveFlankRating) if self.wrapped.ConcaveFlankRating else None

    @property
    def right_flank_rating(self) -> '_161.GearFlankRating':
        '''GearFlankRating: 'RightFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_161.GearFlankRating)(self.wrapped.RightFlankRating) if self.wrapped.RightFlankRating else None

    @property
    def convex_flank_rating(self) -> '_161.GearFlankRating':
        '''GearFlankRating: 'ConvexFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_161.GearFlankRating)(self.wrapped.ConvexFlankRating) if self.wrapped.ConvexFlankRating else None

    @property
    def gear_ratings(self) -> 'List[_326.ConicalGearRating]':
        '''List[ConicalGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_326.ConicalGearRating))
        return value

    @property
    def conical_gear_ratings(self) -> 'List[_326.ConicalGearRating]':
        '''List[ConicalGearRating]: 'ConicalGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConicalGearRatings, constructor.new(_326.ConicalGearRating))
        return value
