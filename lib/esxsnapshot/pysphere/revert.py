import esxsnapshot.log
from pysphere import VIException


__author__ = 'weldpua2008@gmail.com'


def snapshot(vm, snapname, snaprun):
    try:
        esxsnapshot.log.info(
            'Reverting snapshot on %s with the following attributes: Name: %s. Revert options: Run Sync: %s.' %
            (vm.properties.name, snapname, snaprun))
        vm.revert_to_named_snapshot(snapname, sync_run=snaprun)
        if snaprun:
            esxsnapshot.log.info("Snapshot was successfully reverted")
            return 1
        else:
            esxsnapshot.log.warning(
                "Task running asynchronously. This might take a few minutes.")
            return 2
    except VIException as inst:
        esxsnapshot.log.error(inst)
        return 0
