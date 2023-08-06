﻿'''_5412.py

TorqueConverterGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2164
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6227
from mastapy.system_model.analyses_and_results.system_deflections import _2359
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5314
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'TorqueConverterGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterGearWhineAnalysis',)


class TorqueConverterGearWhineAnalysis(_5314.CouplingGearWhineAnalysis):
    '''TorqueConverterGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2164.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2164.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6227.TorqueConverterLoadCase':
        '''TorqueConverterLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6227.TorqueConverterLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2359.TorqueConverterSystemDeflection':
        '''TorqueConverterSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2359.TorqueConverterSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
