﻿'''_1624.py

LoadedAxialThrustCylindricalRollerBearingRow
'''


from mastapy.bearings.bearing_results.rolling import _1623, _1654
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_AXIAL_THRUST_CYLINDRICAL_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedAxialThrustCylindricalRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedAxialThrustCylindricalRollerBearingRow',)


class LoadedAxialThrustCylindricalRollerBearingRow(_1654.LoadedNonBarrelRollerBearingRow):
    '''LoadedAxialThrustCylindricalRollerBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_AXIAL_THRUST_CYLINDRICAL_ROLLER_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedAxialThrustCylindricalRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_1623.LoadedAxialThrustCylindricalRollerBearingResults':
        '''LoadedAxialThrustCylindricalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1623.LoadedAxialThrustCylindricalRollerBearingResults)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None
