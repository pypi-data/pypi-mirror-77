﻿'''_4728.py

AssemblyModalAnalysis
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2002
from mastapy.system_model.analyses_and_results.static_loads import _6080
from mastapy.system_model.analyses_and_results.system_deflections import _2237
from mastapy.system_model.analyses_and_results.modal_analyses import (
    _4783, _4729, _4731, _4734,
    _4741, _4740, _4744, _4749,
    _4752, _4763, _4767, _4773,
    _4774, _4782, _4790, _4793,
    _4794, _4795, _4801, _4806,
    _4809, _4810, _4811, _4817,
    _4813, _4818, _4824, _4827,
    _4830, _4833, _4837, _4841,
    _4844, _4853, _4856, _4723
)
from mastapy.system_model.analyses_and_results.modal_analyses.reporting import _4857
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'AssemblyModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyModalAnalysis',)


class AssemblyModalAnalysis(_4723.AbstractAssemblyModalAnalysis):
    '''AssemblyModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def calculate_all_selected_strain_and_kinetic_energies(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateAllSelectedStrainAndKineticEnergies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateAllSelectedStrainAndKineticEnergies

    @property
    def calculate_all_strain_and_kinetic_energies(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateAllStrainAndKineticEnergies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateAllStrainAndKineticEnergies

    @property
    def assembly_design(self) -> '_2002.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2002.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6080.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6080.AssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2237.AssemblySystemDeflection':
        '''AssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2237.AssemblySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def full_fe_meshes_for_calculating_modes(self) -> 'List[_4783.ImportedFEComponentModalAnalysis]':
        '''List[ImportedFEComponentModalAnalysis]: 'FullFEMeshesForCalculatingModes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FullFEMeshesForCalculatingModes, constructor.new(_4783.ImportedFEComponentModalAnalysis))
        return value

    @property
    def calculate_full_fe_results_by_mode(self) -> 'List[_4857.CalculateFullFEResultsForMode]':
        '''List[CalculateFullFEResultsForMode]: 'CalculateFullFEResultsByMode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CalculateFullFEResultsByMode, constructor.new(_4857.CalculateFullFEResultsForMode))
        return value

    @property
    def bearings(self) -> 'List[_4729.BearingModalAnalysis]':
        '''List[BearingModalAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4729.BearingModalAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_4731.BeltDriveModalAnalysis]':
        '''List[BeltDriveModalAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4731.BeltDriveModalAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4734.BevelDifferentialGearSetModalAnalysis]':
        '''List[BevelDifferentialGearSetModalAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4734.BevelDifferentialGearSetModalAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_4741.BoltModalAnalysis]':
        '''List[BoltModalAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4741.BoltModalAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_4740.BoltedJointModalAnalysis]':
        '''List[BoltedJointModalAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4740.BoltedJointModalAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_4744.ClutchModalAnalysis]':
        '''List[ClutchModalAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4744.ClutchModalAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_4749.ConceptCouplingModalAnalysis]':
        '''List[ConceptCouplingModalAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4749.ConceptCouplingModalAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4752.ConceptGearSetModalAnalysis]':
        '''List[ConceptGearSetModalAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4752.ConceptGearSetModalAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_4763.CVTModalAnalysis]':
        '''List[CVTModalAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4763.CVTModalAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4767.CylindricalGearSetModalAnalysis]':
        '''List[CylindricalGearSetModalAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4767.CylindricalGearSetModalAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4773.FaceGearSetModalAnalysis]':
        '''List[FaceGearSetModalAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4773.FaceGearSetModalAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4774.FlexiblePinAssemblyModalAnalysis]':
        '''List[FlexiblePinAssemblyModalAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4774.FlexiblePinAssemblyModalAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4782.HypoidGearSetModalAnalysis]':
        '''List[HypoidGearSetModalAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4782.HypoidGearSetModalAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4783.ImportedFEComponentModalAnalysis]':
        '''List[ImportedFEComponentModalAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4783.ImportedFEComponentModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4790.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4790.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4793.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4793.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_4794.MassDiscModalAnalysis]':
        '''List[MassDiscModalAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4794.MassDiscModalAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_4795.MeasurementComponentModalAnalysis]':
        '''List[MeasurementComponentModalAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4795.MeasurementComponentModalAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_4801.OilSealModalAnalysis]':
        '''List[OilSealModalAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4801.OilSealModalAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4806.PartToPartShearCouplingModalAnalysis]':
        '''List[PartToPartShearCouplingModalAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4806.PartToPartShearCouplingModalAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_4809.PlanetCarrierModalAnalysis]':
        '''List[PlanetCarrierModalAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4809.PlanetCarrierModalAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_4810.PointLoadModalAnalysis]':
        '''List[PointLoadModalAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4810.PointLoadModalAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_4811.PowerLoadModalAnalysis]':
        '''List[PowerLoadModalAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4811.PowerLoadModalAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4817.ShaftHubConnectionModalAnalysis]':
        '''List[ShaftHubConnectionModalAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4817.ShaftHubConnectionModalAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4813.RollingRingAssemblyModalAnalysis]':
        '''List[RollingRingAssemblyModalAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4813.RollingRingAssemblyModalAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_4818.ShaftModalAnalysis]':
        '''List[ShaftModalAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4818.ShaftModalAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4824.SpiralBevelGearSetModalAnalysis]':
        '''List[SpiralBevelGearSetModalAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4824.SpiralBevelGearSetModalAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_4827.SpringDamperModalAnalysis]':
        '''List[SpringDamperModalAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4827.SpringDamperModalAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4830.StraightBevelDiffGearSetModalAnalysis]':
        '''List[StraightBevelDiffGearSetModalAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4830.StraightBevelDiffGearSetModalAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4833.StraightBevelGearSetModalAnalysis]':
        '''List[StraightBevelGearSetModalAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4833.StraightBevelGearSetModalAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_4837.SynchroniserModalAnalysis]':
        '''List[SynchroniserModalAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4837.SynchroniserModalAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_4841.TorqueConverterModalAnalysis]':
        '''List[TorqueConverterModalAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4841.TorqueConverterModalAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4844.UnbalancedMassModalAnalysis]':
        '''List[UnbalancedMassModalAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4844.UnbalancedMassModalAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4853.WormGearSetModalAnalysis]':
        '''List[WormGearSetModalAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4853.WormGearSetModalAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4856.ZerolBevelGearSetModalAnalysis]':
        '''List[ZerolBevelGearSetModalAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4856.ZerolBevelGearSetModalAnalysis))
        return value
