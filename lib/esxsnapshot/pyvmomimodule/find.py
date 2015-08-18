import esxsnapshot.log
import sys
__author__ = 'weldpua2008@gmail.com'


def vm_by_uuid(uuid, con):
    """Find vm by uuid
    :param uuid:
    :param con:
    :return:
    """

    try:
        search_index = con.content.searchIndex
        vm = search_index.FindByUuid(None, uuid, True, True)
        # if vm is None:
        #     print("Could not find virtual machine '{0}'".format(uuid))
        #     sys.exit(1)
        if vm is not None:
            esxsnapshot.log.debug('Found VM %s' % vm.name)
        return vm
    except Exception:
        return None

def vm_by_ip(ip, con):
    """Find vm by uuid
    :param uuid:
    :param con:
    :return:
    """

    try:
        search_index = con.content.searchIndex
        vm = search_index.FindByIp(None, ip, True)
        # if vm is None:
        #     print("Could not find virtual machine '{0}'".format(uuid))
        #     sys.exit(1)
        if vm is not None:
            esxsnapshot.log.debug('Found VM %s' % vm.name)
        return vm
    except Exception:
        return None
