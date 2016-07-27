import esxsnapshot
import esxsnapshot.log
from pysphere import VIException


__author__ = 'weldpua2008@gmail.com'


def snapshot(vm, snapname, snaprun, children):
    try:
        esxsnapshot.log.info(
            'Deleting snapshot of %s with the following attributes: Name: %s. Delete options: Run Sync: %s; Children: %s' %
            (vm.properties.name, snapname, snaprun, children))
        vm.delete_named_snapshot(
            snapname,
            remove_children=children,
            sync_run=snaprun)
        if snaprun:
            esxsnapshot.log.info("Snapshot successfully deleted")
            return 1
        else:
            esxsnapshot.log.warning(
                "Task running asynchronously. This might take a few minutes.")
            return 2
    except VIException as inst:
        esxsnapshot.log.error(inst)
        return 0
