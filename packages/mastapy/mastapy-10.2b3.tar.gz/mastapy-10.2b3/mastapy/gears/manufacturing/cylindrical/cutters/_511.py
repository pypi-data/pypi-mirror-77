﻿'''_511.py

CylindricalGearGrindingWorm
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _531, _533, _528
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters import _515
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_GRINDING_WORM = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearGrindingWorm')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearGrindingWorm',)


class CylindricalGearGrindingWorm(_515.CylindricalGearRackDesign):
    '''CylindricalGearGrindingWorm

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_GRINDING_WORM

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearGrindingWorm.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def clearance_coefficient(self) -> 'float':
        '''float: 'ClearanceCoefficient' is the original name of this property.'''

        return self.wrapped.ClearanceCoefficient

    @clearance_coefficient.setter
    def clearance_coefficient(self, value: 'float'):
        self.wrapped.ClearanceCoefficient = float(value) if value else 0.0

    @property
    def flat_tip_width(self) -> 'float':
        '''float: 'FlatTipWidth' is the original name of this property.'''

        return self.wrapped.FlatTipWidth

    @flat_tip_width.setter
    def flat_tip_width(self, value: 'float'):
        self.wrapped.FlatTipWidth = float(value) if value else 0.0

    @property
    def edge_height(self) -> 'float':
        '''float: 'EdgeHeight' is the original name of this property.'''

        return self.wrapped.EdgeHeight

    @edge_height.setter
    def edge_height(self, value: 'float'):
        self.wrapped.EdgeHeight = float(value) if value else 0.0

    @property
    def has_tolerances(self) -> 'bool':
        '''bool: 'HasTolerances' is the original name of this property.'''

        return self.wrapped.HasTolerances

    @has_tolerances.setter
    def has_tolerances(self, value: 'bool'):
        self.wrapped.HasTolerances = bool(value) if value else False

    @property
    def nominal_worm_grinder_shape(self) -> '_531.CylindricalGearWormGrinderShape':
        '''CylindricalGearWormGrinderShape: 'NominalWormGrinderShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_531.CylindricalGearWormGrinderShape)(self.wrapped.NominalWormGrinderShape) if self.wrapped.NominalWormGrinderShape else None

    @property
    def nominal_rack_shape(self) -> '_533.RackShape':
        '''RackShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_533.RackShape)(self.wrapped.NominalRackShape) if self.wrapped.NominalRackShape else None

    @property
    def nominal_rack_shape_of_type_cylindrical_gear_hob_shape(self) -> '_528.CylindricalGearHobShape':
        '''CylindricalGearHobShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _528.CylindricalGearHobShape.TYPE not in self.wrapped.NominalRackShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_rack_shape to CylindricalGearHobShape. Expected: {}.'.format(self.wrapped.NominalRackShape.__class__.__qualname__))

        return constructor.new(_528.CylindricalGearHobShape)(self.wrapped.NominalRackShape) if self.wrapped.NominalRackShape else None

    @property
    def nominal_rack_shape_of_type_cylindrical_gear_worm_grinder_shape(self) -> '_531.CylindricalGearWormGrinderShape':
        '''CylindricalGearWormGrinderShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _531.CylindricalGearWormGrinderShape.TYPE not in self.wrapped.NominalRackShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_rack_shape to CylindricalGearWormGrinderShape. Expected: {}.'.format(self.wrapped.NominalRackShape.__class__.__qualname__))

        return constructor.new(_531.CylindricalGearWormGrinderShape)(self.wrapped.NominalRackShape) if self.wrapped.NominalRackShape else None
