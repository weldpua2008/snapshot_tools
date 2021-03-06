import esxsnapshot.log
from pysphere import VIException


__author__ = 'weldpua2008@gmail.com'


def snapshot(vm, snapname, snapdesc, snaprun):
    try:
        esxsnapshot.log.info(
            'Creating snapshot on %s with the following attributes: Name: %s; Description: %s; Run Sync: %s' %
            (vm.properties.name, snapname, snapdesc, snaprun))
        vm.create_snapshot(snapname, description=snapdesc, sync_run=snaprun)
        if snaprun:
            esxsnapshot.log.info("Snapshot taken successfully.")
            return 1
        else:
            esxsnapshot.log.warning(
                "Task running asynchronously. This might take a few minutes.")
            return 2
    except VIException as inst:
        esxsnapshot.log.error(inst)
        return 0
