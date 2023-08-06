﻿'''_3263.py

CoaxialConnectionPowerFlow
'''


from mastapy.system_model.connections_and_sockets import _1854
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6097
from mastapy.system_model.analyses_and_results.power_flows import _3333
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CoaxialConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionPowerFlow',)


class CoaxialConnectionPowerFlow(_3333.ShaftToMountableComponentConnectionPowerFlow):
    '''CoaxialConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1854.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1854.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6097.CoaxialConnectionLoadCase':
        '''CoaxialConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6097.CoaxialConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
