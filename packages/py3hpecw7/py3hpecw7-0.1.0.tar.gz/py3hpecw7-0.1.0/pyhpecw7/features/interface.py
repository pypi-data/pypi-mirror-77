"""Manage interfaces on HPCOM7 devices.
"""

from pyhpecw7.utils.xml.lib import reverse_value_map
from pyhpecw7.features.errors import InterfaceCreateError, InterfaceTypeError,\
    InterfaceAbsentError, InterfaceParamsError, InterfaceVlanMustExist
from pyhpecw7.features.vlan import Vlan

from pyhpecw7.utils.xml.lib import *


class Interface(object):
    """This class is used to get
    and build interface configurations on ``HPCOM7`` devices.

    Args:
        device (HPCOM7): connected instance of a
            ``phyp.comware.HPCOM7`` object.
        interface_name (str): The name of the interface.

    Attributes:
        device (HPCOM7): connected instance of a
            ``phyp.comware.HPCOM7`` object.
        interface_name (str): The name of the interface.
        iface_index (str): The device's internal number representation
            of an interface.
        iface_type (str): The type of interface,
            for example: 'LoopBack', 'FortyGigE'.
        is_ethernet (bool): Whether the interface is ethernet.
        is_routed (bool): Whether the interface is in layer 3 mode.
            If this is ``False``, the interface is either in bridged
            mode or does not exist.
        iface_exists (bool): Whether the interface exists. Physical
            interfaces should always exist. Logical interfaces may
            or may not exist.
    """
    def __init__(self, device, interface_name):
        # used to map key values from our dictionary model
        # to expected XML tags and vice versa
        self._key_map = {
            'admin': 'AdminStatus',
            'speed': 'ConfigSpeed',
            'duplex': 'ConfigDuplex',
            'description': 'Description',
            'type': 'PortLayer'
        }

        # used to map value values from our dictionary model
        # to expected XML tags and vice versa
        self._value_map = {
            'AdminStatus': {'1': 'up',
                            '2': 'down'},
            'ConfigSpeed': {'1': 'auto', '2': '10',
                            '4': '100', '32': '1000',
                            '1024': '10000', '4096': '20000',
                            '8192': '40000', '16384': '100000'},
            'ConfigDuplex': {'1': 'full',
                             '2': 'half',
                             '3': 'auto'},
            'PortLayer': {'1': 'bridged',
                          '2': 'routed'}
        }

        self._iface_types = set(['FortyGigE', 'Tunnel', 'LoopBack',
                                 'Vlan-interface', 'Bridge-Aggregation',
                                 'Route-Aggregation', 'GigabitEthernet',
                                 'TwentyGigE', 'Ten-GigabitEthernet',
                                 'HundredGigE'])

        # xml tags
        self._iface_row_name = 'Interface'
        self._iface_index_name = 'IfIndex'

        # usd in conjunction with key map and value map above
        self._r_key_map = dict(reversed(item) for item in self._key_map.items())
        self._r_value_map = reverse_value_map(self._r_key_map, self._value_map)

        # connect to the device and get more information
        self.interface_name, self.iface_type = self._iface_type(interface_name)
        self.device = device

        # The interface index is needed for most interface NETCONF requests
        self.iface_index = self._get_iface_index()

        self.is_ethernet, self.is_routed = self._is_ethernet_is_routed()
        self.iface_exists = True if self.iface_index else False

    def _iface_type(self, if_name):
        """Return the normalized interface name and type
        from a denormalized interface name.
        """

        if if_name.lower().startswith('gi'):
            if_type = 'GigabitEthernet'
        elif if_name.lower().startswith('ten'):
            if_type = 'Ten-GigabitEthernet'
        elif if_name.lower().startswith('fo'):
            if_type = 'FortyGigE'
        elif if_name.lower().startswith('vl'):
            if_type = 'Vlan-interface'
        elif if_name.lower().startswith('lo'):
            if_type = 'LoopBack'
        elif if_name.lower().startswith('br'):
            if_type = 'Bridge-Aggregation'
        elif if_name.lower().startswith('ro'):
            if_type = 'Route-Aggregation'
        elif if_name.lower().startswith('tu'):
            if_type = 'Tunnel'
        elif if_name.lower().startswith('tw'):
            if_type = 'TwentyGigE'
        elif if_name.lower().startswith('hu'):
            if_type = 'HundredGigE'
        else:
            if_type = None

        number_list = if_name.split(' ')
        if len(number_list) == 2:
            number = number_list[-1].strip()
        else:
            number = self._get_number(if_name)

        if if_type:
            proper_interface = if_type + number
        else:
            proper_interface = if_name

        return proper_interface, if_type

    def _get_number(self, if_name):
        digits = ''
        for char in if_name:
            if char.isdigit() or char == '/' or char == ':':
                digits += char
        return digits

    def _get_iface_index(self):
        """Return the interface index given the self.interface_name
        attribute by asking the device. If the interface doesn't exist,
        return the empty string.
        """
        E = data_element_maker()
        top = E.top(
            E.Ifmgr(
                E.Interfaces(
                    E.Interface(
                        E.Name(self.interface_name)
                    )
                )
            )
        )

        nc_get_reply = self.device.get(('subtree', top))
        reply_data = find_in_data(
            self._iface_index_name, nc_get_reply.data_ele)

        if reply_data is None:
            return ''

        return reply_data.text

    def _is_ethernet_is_routed(self):
        """Return whether the interface is ethernet and whether
        it is routed. If the interface doesn't exist,
        return False.
        """
        E = data_element_maker()
        top = E.top(
            E.Ifmgr(
                E.Interfaces(
                    E.Interface(
                        E.IfIndex(self.iface_index)
                    )
                )
            )
        )

        nc_get_reply = self.device.get(('subtree', top))
        reply_data = find_in_data('ifType', nc_get_reply.data_ele)

        routed_reply_data = find_in_data('PortLayer', nc_get_reply.data_ele)

        is_ethernet = False
        is_routed = False
        try:
            if reply_data.text == '6':
                is_ethernet = True
        except AttributeError:
            pass

        try:
            if routed_reply_data.text == '2':
                is_routed = True
        except AttributeError:
            pass

        return is_ethernet, is_routed

    def update(self):
        """Update ``self.iface_index`` and ``self.iface_exists``.

        Usually called after a logical interface is created.

        Raises:
            InterfaceCreateError: if the interface hasn't yet
                been successfully created.

        Note:
            It is the responsibility of the caller to call ``update()`
            after staging (``create_logical()``) *and* executing
            (``execute()`` on this class's ``device`` object) of
            commands to create an interface.
         """
        if_index = self._get_iface_index()
        if not if_index:
            raise InterfaceCreateError(self.interface_name)
        self.iface_index = if_index
        self.iface_exists = True

    def get_default_config(self):
        """Return the default configuration of an interface.

        Returns:
            A dictionary of default interface configuration parameters,
            depending on the type of interface.

            For example, for ethernet interfaces::

                {
                    'description': 'FortyGigE1/0/1 Interface',
                    'admin': 'up',
                    'speed': 'auto',
                    'duplex': 'auto',
                    'type': 'bridged'
                }
        """
        if not self.iface_type:
            return None

        defaults = {}
        defaults['description'] = self.interface_name + ' Interface'
        defaults['admin'] = 'up'
        if self.is_ethernet:
            defaults['speed'] = 'auto'
            defaults['duplex'] = 'auto'
            defaults['type'] = 'bridged'
        elif self.iface_type == 'Bridge-Aggregation':
            defaults['type'] = 'bridged'
        else:
            defaults['type'] = 'routed'

        return defaults

    def param_check(self, **params):
        """Checks given parameters against the interface for various errors.

        Args:
            **params: see Keyword Args

        Keyword Args:
            admin (str): The up/down state of the interface.
                'up' or 'down'.
            speed (str): The speed of the interface, in Mbps.
            duplex (str): The duplex of the interface.
                'full', 'half', or 'auto'.
            description (str): The textual description of the interface.
            type (str): Whether the interface is in layer 2 or layer 3 mode.
                'bridged' or 'routed'.

        Raises:
            InterfaceTypeError: if the given interface isn't a valid type.
            InterfaceAbsentError: if the given interface is of type is_ethernet
                and doesn't exist.
            InterfaceParamsError: if 'speed' or 'duplex' are supplied for a
                non ethernet interface.
            InterfaceVlanMustExist: if the interface is of type
                'Vlan-interface' and the the associated vlan doesn't exist.
        """
        if not self.iface_type:
            raise InterfaceTypeError(
                self.interface_name, list(self._iface_types))

        if not self.iface_exists:
            if self.iface_type in {'FortyGigE', 'GigabitEthernet',
                                   'TwentyGigE', 'Ten-GigabitEthernet',
                                   'HundredGigE'}:
                raise InterfaceAbsentError(self.interface_name)

        if not self.is_ethernet:
            param_names = []
            if params.get('speed'):
                param_names.append('speed')
            if params.get('duplex'):
                param_names.append('duplex')
            if param_names:
                raise InterfaceParamsError(self.interface_name, param_names)

        if self.iface_type == 'Vlan-interface':
            number = self.interface_name.split('Vlan-interface')[1]
            vlan = Vlan(self.device, number)
            if not vlan.get_config():
                raise InterfaceVlanMustExist(self.interface_name, number)

    def get_config(self):
        """Return the currently configured
        parameters for the interface.

        Returns:
            A dictionary of currently configured
            parameters for the interface, including:
                :admin (str): The up/down state of the interface.
                    'up' or 'down'.
                :speed (str): The speed of the interface, in Mbps.
                :duplex (str): The duplex of the interface.
                    'full', 'half', or 'auto'.
                :description (str): The textual description of the interface.
                :type (str): Whether the interface is in layer 2 or
                    layer 3 mode. 'bridged' or 'routed'.
        """
        E = data_element_maker()
        top = E.top(
            E.Ifmgr(
                E.Interfaces(
                    E.Interface(
                        E.IfIndex(self.iface_index)
                    )
                )
            )
        )

        nc_get_reply = self.device.get(('subtree', top))
        reply_data = find_in_data(self._iface_row_name, nc_get_reply.data_ele)

        if reply_data is None:
            return {}

        return data_elem_to_dict(reply_data, self._key_map, value_map=self._value_map)

    def create_logical(self, stage=False):
        """Stage or execute the configuration to create
        a logical interface.

        Supported types include 'LoopBack',
        'Vlan-interface', 'Bridge-Aggregation',
        and 'Route-Aggregation'

        Note:
            When stage=True, it's the caller's responsibility to call
            ``execute()`` on this class's ``device``
            object after this method is called.

        Note:
            After execution, the caller must call ``update()`` on this class.

        Returns:
            True if successful.

        Raises:
            InterfaceCreateError: if the logical interface
                cannot be created.
        """
        return self._logical_iface(stage=stage)

    def remove_logical(self, stage=False):
        """Stage or execute the configuration to remove
        a logical interface.

        Supported types include 'LoopBack',
        'Vlan-interface', 'Bridge-Aggregation',
        and 'Route-Aggregation'

        Args:
            stage (bool): whether to stage the commands or execute
                immediately

        Note:
            It's the caller's responsibility to call
            ``execute()`` on this class's ``device``
            object after this method is called.

        Returns:
            True if stage=True and staging is successful
            etree.Element XML response if immediate execution

        Raises:
            InterfaceCreateError: if the logical interface
                cannot be removed.
        """
        return self._logical_iface(remove=True, stage=stage)

    def _logical_iface(self, remove=False, stage=False):
        """Stage or execute the configuration to create
        or remove a logical interface.

        Args:
            remove (bool): If ``True``, the logical
                interface is removed. If ``False``,
                the logical interface is created.

            stage (bool): whether to stage the commands or execute
                immediately

        Returns:
            True if stage=True and staging is successful
            etree.Element XML response if immediate execution
        """
        logic_type_map = {'LoopBack': '16',
                          'Vlan-interface': '41',
                          'Bridge-Aggregation': '56',
                          'Route-Aggregation': '67'}

        if self.iface_type not in logic_type_map:
            raise InterfaceCreateError(self.interface_name)

        iface_number = self.interface_name.split(self.iface_type)[1]

        E = action_element_maker()
        top = E.top(
            E.Ifmgr(
                E.LogicInterfaces(
                    E.Interface(
                        E.IfTypeExt(logic_type_map[self.iface_type]),
                        E.Number(iface_number)
                    )
                )
            )
        )

        if remove:
            find_in_action('Interface', top).append(E.Remove())

        if stage:
            return self.device.stage_config(top, 'action')
        else:
            return self.device.action(top)

    def build(self, stage=False, **params):
        """Stage or execute the configuration to
        modify an interface.

        Args:
            stage (bool): whether to stage the commands or execute
                immediately
            **params: see Keyword Args.

        Keyword Args:
            admin (str): The up/down state of the interface.
                'up' or 'down'.
            speed (str): The speed of the interface, in Mbps.
            duplex (str): The duplex of the interface.
                'full', 'half', or 'auto'.
            description (str): The textual description of the interface.
            type (str): Whether the interface is in layer 2 or layer 3 mode.
                'bridged' or 'routed'.

        Raises:
            InterfaceCreateError: if a logical interface cannot be created.

        Returns:
            True if stage=True and staging is successful
            etree.Element XML response if immediate execution
        """
        return self._build_config(state='present', stage=stage, **params)

    def default(self, stage=False):
        """Stage or execute the configuration to default an interface.

        stage (bool): whether to stage the commands or execute
            immediately

        Returns:
            True if stage=True and staging is successful
            etree.Element XML response if immediate execution
        """
        return self._build_config(state='default', stage=stage)

    def _build_config(self, state, stage=False, **params):
        """Stage or execute the configuration to
        configure, default, or remove an interface.

        Args:
            state (str): 'present' configures,
                'absent' defaults,
                'default' defaults.
            stage (bool): whether to stage the commands or execute
                immediately
            **params: Used when state=present, see Keyword Args.

        Keyword Args:
            admin (str): The up/down state of the interface.
                'up' or 'down'.
            speed (str): The speed of the interface, in Mbps.
            duplex (str): The duplex of the interface.
                'full', 'half', or 'auto'.
            description (str): The textual description of the interface.
            type (str): Whether the interface is in layer 2 or layer 3 mode.
                'bridged' or 'routed'.

        Returns:
            True if stage=True and staging is successful
            etree.Element XML response if immediate execution
            False if illegal operation, e.g. removing a physical interface
        """
        if state == 'default':
            if self.iface_exists:
                E = action_element_maker()
                top = E.top(
                    E.Ifmgr(
                        E.Interfaces(
                            E.Interface(
                                E.IfIndex(self.iface_index),
                                E.Default()
                            )
                        )
                    )
                )

                if stage:
                    return self.device.stage_config(top, 'action')
                else:
                    return self.device.action(top)

        if state == 'present':
            params[self._iface_index_name] = self.iface_index

            EN = nc_element_maker()
            EC = config_element_maker()

            config = EN.config(
                EC.top(
                    EC.Ifmgr(
                        EC.Interfaces(
                            EC.Interface(
                                *config_params(params, self._key_map, value_map=self._r_value_map)
                            )
                        )
                    )
                )
            )

            if stage:
                return self.device.stage_config(config, 'edit_config')
            else:
                return self.device.edit_config(config)

        if state == 'absent':
            if self.is_ethernet:
                return self._build_config('default', stage=stage)

        return False
