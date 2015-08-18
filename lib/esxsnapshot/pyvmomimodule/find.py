import esxsnapshot.log
import sys
__author__ = 'weldpua2008@gmail.com'


def vm_by_name(name, con):
    """Find vm by name. It's lazy method
    :param name:
    :param con:
    :return:vm
    """

    try:
        content = con.RetrieveContent()
        children = content.rootFolder.childEntity
        for child in children:
            if hasattr(child, 'vmFolder'):
                datacenter = child
            else:
                # some other non-datacenter type object
                continue
            vm_folder = datacenter.vmFolder
            vm_list = vm_folder.childEntity
            for virtual_machine in vm_list:
                if virtual_machine.summary.config.name == name:
                    return virtual_machine
    except Exception as error:
        esxsnapshot.log.debug('Not found VM %s because %s ' % (name, error))
        return None



def vm_by_uuid(uuid, con):
    """Find vm by uuid
    :param uuid:
    :param con:
    :return:vm
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
    :param ip:
    :param con:
    :return:vm
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
