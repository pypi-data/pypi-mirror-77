This project is a fork of [HPENetworking/pyhpecw7][]. The most notable
change is the compatibility with Python 3. The original project is
unfortunately inactive. As soon as the situation changes, the changes
included in this fork will be proposed upstream and, hopefully, this
fork will be terminated.

![Build status](https://img.shields.io/github/workflow/status/vincentbernat/pyhpecw7/Tests)
[![PyPI](https://img.shields.io/pypi/v/py3hpecw7.svg)](https://pypi.python.org/pypi/py3hpecw7)
![PyPI versions](https://img.shields.io/pypi/pyversions/py3hpecw7.svg)
[![Documentation](https://img.shields.io/readthedocs/py3hpecw7)](http://py3hpecw7.readthedocs.io/)

[HPENetworking/pyhpecw7]: https://github.com/HPENetworking/pyhpecw7

# Introduction

This library was built to simplify working with HP Comware 7 switches
that have a NETCONF API. Rather than to have network developers worry
about the underlying NETCONF API, this library provides a means to
manage HP Com7 switches through pre-built Python objects that make it
extremely easy to get started programming in an HP environment.

Before getting started, it's important to understand the high level
workflow required when using this library, which again, is meant to be
fairly straight forward and simple.

### Step 1 - Create HPCOM7 object for each HP switch being managed

```
>>> from pyhpecw7.comware import HPCOM7
>>> args = dict(host='hp1', username='hp', password='hp123')
>>> device = HPCOM7(**args)
```

### Step 2 - Open a Connection to the Device

```
>>> device.open()
<ncclient.manager.Manager object at 0x7fa5088f98d0>
```

### Step 3a - Get Config Data

Nearly all features supported such as `Vlan`, which is used in an
example below, have a `get_config()` method.

The object is imported, it is instantiated, and the `get_config()` can
be called. This method usually returns a Python dictionary with
several key value pairs if the configuration resource exists and if it
doesn't it's an empty dictionary.

Examples are below.

### Step 3b - Configure the Device

Maybe you don't want to get any data, but rather want to make a
configuration change.

Making a configuration change is a two-step process (for most
configuration features).

Build the configuration, which creates the appropriate configuration
object and places it in a *staging* area, but does not push it.

Most methods of the feature class to *build* the configuration are
called `build` or `remove`.

Execute, or push, the configuration object(s) to the device.

While in most cases, users may just want or need to push a single
object, it is possible to build, or stage, multiple configuration
objects and push them all at once in which case they are executed in
the order as they were built. Each time a `build` or `remove` is
executed, a list is being appended to, which is storing the staged
objects.

The final execution (config push) happens by using the `execute`
method of the `HPCOM7` object.

Examples are below.

# Getting Started

## Initialize and Open Connection to the Device

```
>>> from pyhpecw7.comware import HPCOM7
>>> args = dict(host='hp1', username='hp', password='hp123')
>>> device = HPCOM7(**args)
>>> device.open()
<ncclient.manager.Manager object at 0x7fa5088f98d0>
```

## Examples

### Get VLAN Information

```
>>> from pyhpecw7.features.vlan import Vlan
>>> vlan = Vlan(device, '20')
>>> vlan.get_config()
{}
>>> vlan = Vlan(device, '10')
>>> vlan.get_config()
{'name': 'VLAN10_WEB', 'vlanid': '10', 'descr': 'VLAN 0010'}
```

VLAN 20 did not exist on the switch, but VLAN 10 did.

A VLAN object for any VLAN can also return all VLAN IDs that exist on
the switch.

```
>>> vlan.get_vlan_list()
['1', '10']
```

### Configure a VLAN

Let's create a new VLAN object.

```
>>> vlan = Vlan(device, '20')
```

Now add VLAN 20. To do this we'll use the `build` method.

```
>>> vlan.build(stage=True)
True
```

When `True` is returned, it means that the config object that will be
pushed has successfully been staged.

The next step is to execute the change.

```
>>> response = device.execute_staged()
>>> vlan.get_config()
{'name': 'VLAN 0020', 'vlanid': '20', 'descr': 'VLAN 0020'}
```

Setting the vlan name or description could easily be sent in as
additional key value pairs (or with a dictionary) when using `build`.

```
>>> args = dict(name='NEWV20', descr='DESCR_20')
>>> vlan.build(stage=True, **args)
True
>>> rsp = device.execute_staged()
>>> vlan.get_config()
{'name': 'NEWV20', 'vlanid': '20', 'descr': 'DESCR_20'}
```

To remove the VLAN, the `remove` method is used.

```
>>> vlan.remove(stage=True)
True
>>> rsp = device.execute_staged()
>>> vlan.get_config()
{}
```

### Get Interface Information

```
>>> from pyhpecw7.features.interface import Interface
>>> interface = Interface(device, 'FortyGigE1/0/4')
>>> interface.get_config()
{'admin': 'up', 'duplex': 'auto', 'speed': 'auto', 'description': 'DESCR104', 'type': 'routed'}
```

### Default an Interface

```
>>> interface.default(stage=True)
True
>>> response = device.execute_staged()
>>> interface.get_config()
{'admin': 'up', 'duplex': 'auto', 'speed': 'auto', 'description': 'FortyGigE1/0/4 Interface', 'type': 'switched'}
```

### Configure an Interface

```
>>> interface.build(stage=True, admin='down', description='TEST_DESCR')
True
>>> rsp = device.execute_staged()
>>> interface.get_config()
{'admin': 'down', 'duplex': 'auto', 'speed': 'auto', 'description': 'TEST_DESCR', 'type': 'switched'}
```
