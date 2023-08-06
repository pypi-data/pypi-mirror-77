"""Manage switchports on HPCOM7 devices.
"""
from pyhpecw7.features.interface import Interface

from pyhpecw7.utils.xml.lib import *


class Switchport(object):
    """This class is used to get and build layer 2 interface
    configurations on ``HPCOM7`` devices.

    Args:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.
        interface_name (str): The name of the interface.

    Attributes:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.
        interface_name (str): The name of the interface.
        interface (pyhpecw7.features.Interface): The associated
            ``Interface`` configuration object.
    """
    def __init__(self, device, interface_name):
        self.device = device
        self.interface = Interface(device, interface_name)
        self.interface_name = self.interface.interface_name
        self.link_type = 'unknown'

    def get_default(self):
        """Return the default layer 2 settings for a switchport.

        Returns:
            A dictionary of default configuration parameters.

            For example::

                {
                    'pvid': '1',
                    'link_type': 'access'
                }
        """
        return {'pvid': '1', 'link_type': 'access'}

    def get_config(self):
        """Return the current layer 2 settings on the switchport.

        Returns:
            A dictionary of current configuration parameters.

            For example::

                {
                    'pvid': '2',
                    'link_type': 'trunk',
                    'permitted_vlans': '1-5'
                }
        """
        key_map = {'link_type': 'LinkType',
                   'permitted_vlans': 'PermitVlanList',
                   'pvid': 'PVID'}
        value_map = {'LinkType': {'1': 'access',
                                  '2': 'trunk'}}

        E = data_element_maker()
        top = E.top(
            E.VLAN(
                E.Interfaces(
                    E.Interface(
                        E.IfIndex(self.interface.iface_index)
                    )
                )
            )
        )

        nc_get_reply = self.device.get(('subtree', top))
        reply_data = find_in_data('Interface', nc_get_reply.data_ele)

        if reply_data is None:
            return {}

        link_type_value = find_in_data('LinkType', nc_get_reply.data_ele).text

        if link_type_value == '1':
            self.link_type = 'access'
        elif link_type_value == '2':
            self.link_type = 'trunk'

        return data_elem_to_dict(reply_data, key_map, value_map=value_map)

    def convert_interface(self, link_type, stage=False):
        """Stage or execute the commands to toggle an interface between trunk/access.

        Args:
            link_type (str): 'access' or 'trunk'.
            stage (bool): whether to stage the command or execute immediately

        Note:
            If `link_type` does not equal 'access' or 'trunk',
            no commands are staged.

        Returns:
            True if stage=True and successfully staged
            etree.Element XML responses if immediate execution
        """
        if link_type == 'access':
            type_value = '1'
        elif link_type == 'trunk':
            type_value = '2'
        else:
            return

        EN = nc_element_maker()
        EC = config_element_maker()
        config = EN.config(
            EC.top(
                EC.Ifmgr(
                    EC.Interfaces(
                        EC.Interface(
                            EC.IfIndex(self.interface.iface_index),
                            EC.LinkType(type_value),
                        )
                    )
                )
            )
        )

        if stage:
            self.device.stage_config(config, 'edit_config')
        else:
            self.device.edit_config(config)

    def default(self, stage=False):
        """Stage or execute a layer 2 default configuration.

        Args:
            stage (bool): whether to stage the command or execute immediately

        Returns:
            True if stage=True and successfully staged
            etree.Element XML response if immediate execution
        """
        defaults = self.get_default()
        return self.build(stage=stage, **defaults)

    def build(self, stage=False, **params):
        """Stage a layer 2 configuration with given parameters on switchport.

        Args:
            stage (bool): whether to stage the command or execute immediately

        Keyword Args:
            link_type (str): 'access' or 'trunk'.
            pvid (str): The access VLAN if link_type is 'access',
                the native VLAN if link_type is 'trunk'.
            permitted_vlans (str): A comma and/or hyphen delimited list
                of VLAN numbers. Used when link_type is 'trunk'.
                For example: `1,3-5,7`

        Returns:
            True if stage=True and successfully staged
            etree.Element XML response if immediate execution
        """
        EN = nc_element_maker()
        EC = config_element_maker()

        link_type = params.pop('link_type', None)
        if link_type == 'trunk':
            if self.link_type != 'trunk':
                self.convert_interface(link_type, stage=stage)

            key_map = {'permitted_vlans': 'PermitVlanList',
                       'pvid': 'PVID'}

            config = EN.config(
                EC.top(
                    EC.VLAN(
                        EC.TrunkInterfaces(
                            EC.Interface(
                                EC.IfIndex(self.interface.iface_index),
                                *config_params(params, key_map)
                            )
                        )
                    )
                )
            )

        elif link_type == 'access':
            if self.link_type != 'access':
                self.convert_interface(link_type, stage=stage)

            key_map = {'pvid': 'PVID'}
            config = EN.config(
                EC.top(
                    EC.VLAN(
                        EC.AccessInterfaces(
                            EC.Interface(
                                EC.IfIndex(self.interface.iface_index),
                                *config_params(params, key_map)
                            )
                        )
                    )
                )
            )

        else:
            return

        if params:
            if stage:
                return self.device.stage_config(config, 'edit_config')
            else:
                return self.device.edit_config(config)

        return False
