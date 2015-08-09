import esxsnapshot.log
from pysphere import VIException

__author__ = 'weldpua2008@gmail.com'


def vm_by_name(name, con):
    """Find vm by name
    :param name:
    :param con:
    :return:
    """

    try:
        vm = con.get_vm_by_name(name)
        esxsnapshot.log.debug('Found VM %s' % vm.properties.name)
        return vm
    except VIException:
        return None
