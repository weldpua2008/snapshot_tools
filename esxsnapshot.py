#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import sys
import getpass
import argparse
import base64
from pysphere import VIException
import lib.log
import lib.logs.send
import lib.pysphere.connect
import lib.pysphere.list
import lib.pysphere.find
import lib.pysphere.create
import lib.pysphere.delete
import lib.pysphere.revert


def get_args(): # pragma: no cover
    # Creating the argument parser
    parser = argparse.ArgumentParser(
        description="Manage VM snapshots. Create, Delete, List and Revert to Snapshot.")
    parser.add_argument(
        '-s',
        '--server',
        nargs=1,
        required=True,
        help='The vCenter or ESXi server to connect to',
        dest='server',
        type=str)
    parser.add_argument(
        '-u',
        '--user',
        nargs=1,
        required=True,
        help='The username with which to connect to the server',
        dest='username',
        type=str)
    parser.add_argument(
        '-p',
        '--password',
        nargs=1,
        required=False,
        help='The password in plain text with which to connect to the host. If not specified, the user is prompted at runtime for a password.',
        dest='password',
        type=str)
    parser.add_argument(
        '-pe',
        '--password-encrypted',
        nargs=1,
        required=False,
        help='The password encrypted using Base64 with which to connect to the host. ',
        dest='passwordEncrypted',
        type=str)
    parser.add_argument(
        '-m',
        '--vm',
        nargs=1,
        required=True,
        help='The virtual machine (VM) to manage snapshots',
        dest='vmname',
        type=str)
    parser.add_argument(
        '-v',
        '--verbose',
        required=False,
        help='Enable verbose output',
        dest='verbose',
        action='store_true')
    parser.add_argument(
        '-d',
        '--debug',
        required=False,
        help='Enable debug output',
        dest='debug',
        action='store_true')
    parser.add_argument(
        '-l',
        '--log-file',
        nargs=1,
        required=False,
        help='File to log to (default = stdout)',
        dest='logfile',
        type=str)
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version="%(prog)s (version 0.4)")

    subparsers = parser.add_subparsers(help='commands')

    # A list command
    list_parser = subparsers.add_parser(
        'list',
        help='List Snapshot(s) of a given VM')
    list_parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        help='List all snapshots',
        default=False,
        dest='lall')

    # A create command
    create_parser = subparsers.add_parser(
        'create',
        help='Create a Snapshot of a given VM')
    create_parser.add_argument(
        '-sn',
        '--sname',
        required=True,
        action='store',
        help='New snapshot name',
        dest='sname',
        type=str)
    create_parser.add_argument(
        '-sd',
        '--sdescription',
        required=True,
        help='New snapshot description.',
        action='store',
        dest='sdesc',
        type=str)
    create_parser.add_argument(
        '-sr',
        '--syncrun',
        default=False,
        help='Take snapshot synchronously, default is False',
        dest='ssync',
        action='store_true')
    create_parser.add_argument(
        '-no',
        '--notification',
        required=False,
        help='Send email notification to included email address(es).',
        action='store',
        dest='notif',
        type=str)

    # A delete command
    delete_parser = subparsers.add_parser(
        'delete',
        help='Delete a Snapshot of a given VM')
    delete_parser.add_argument(
        '-sn',
        '--sname',
        action='store',
        required=True,
        help='Name of the snapshot to delete',
        dest='snamed',
        type=str)
    delete_parser.add_argument(
        '-sr',
        '--syncrun',
        default=False,
        help='Delete snapshot synchronously, default is False',
        dest='ssync',
        action='store_true')
    delete_parser.add_argument(
        '-ch',
        '--children',
        default=False,
        help='Will delete not only the specified snapshot but also all of its descendants, default is False',
        dest='children',
        action='store_true')
    delete_parser.add_argument(
        '-no',
        '--notification',
        required=False,
        help='Send email notification to included email address(es).',
        action='store',
        dest='notif',
        type=str)

    # A revert command
    revert_parser = subparsers.add_parser(
        'revert',
        help='Revert to a Snapshot of a given VM')
    revert_parser.add_argument(
        '-sn',
        '--sname',
        action='store',
        required=True,
        help='Name of the snapshot to revert',
        dest='snamer',
        type=str)
    revert_parser.add_argument(
        '-sr',
        '--syncrun',
        default=False,
        help='Revert to snapshot synchronously, default is False',
        dest='ssync',
        action='store_true')
    revert_parser.add_argument(
        '-no',
        '--notification',
        required=False,
        help='Send email notification to included email address(es).',
        action='store',
        dest='notif',
        type=str)

    args = parser.parse_args()
    return args


def run(): # pragma: no cover
    # Notification settings
    from_snap = "vi-admin@vma5"
    status = {1: 'SUCCESSFUL', 0: 'FAILED', 2: 'IN PROGRESS'}
    action = {1: 'CREATE', 2: 'DELETE', 3: 'LIST', 4: 'REVERT'}

    args = get_args()
    argsdict = vars(args)
    server = args.server[0]
    username = args.username[0]
    vmname = args.vmname[0]
    verbose = args.verbose
    debug = args.debug
    log_file = None
    password = None
    emailto = None

    if args.password:
        password = args.password[0]

    if args.logfile:
        log_file = args.logfile[0]

    # Logging settings
    if debug:
        log_level = logging.DEBUG
    elif verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    # Initializing logger
    if log_file:
        logging.basicConfig(
            filename=log_file,
            format='%(asctime)s %(levelname)s %(message)s',
            level=log_level)
    else:
        logging.basicConfig(
            filename=log_file,
            format='%(asctime)s %(levelname)s %(message)s',
            level=log_level)

    logger = logging.getLogger(__name__)
    logger.debug('logger initialized')

    try:
        logger.debug('Using encrypted password. Decrypting now.')
        if args.passwordEncrypted:
            password = base64.b64decode(args.passwordEncrypted[0])
    except Exception as error:
        logger.error(error)
        logger.debug(
            'Password error. Either this is not an encrypted passowrd or is not well formated.')
        sys.exit()

    # Asking Users password for server
    if password is None:
        logger.debug(
            'No command line password received, requesting plain text password from user.')
        password = getpass.getpass(
            prompt='Enter password for vCenter %s for user %s: ' %
            (server, username))

    logger.debug(password)

    # Connecting to server
    logger.info('Connecting to server %s with username %s' % (server, username))
    con = lib.pysphere.connect.to_esx(
        server=server,
        username=username,
        password=password)


    try:
            # Getting VM object
        vm = lib.pysphere.find.vm_by_name(vmname, con)

        if vm:
            logger.info(
                'Successfully found %s in %s' %
                (vm.get_property('name'), vm.get_property('path')))
        else:
            logger.error(
                "Could not find %s, please verify VM's name and try again." %
                vm)
            con.disconnect()
            sys.exit()

        # Parse List opt
        if hasattr(args, 'lall'):
            logger.debug('Listing all snapshots as requested by user.')
            list = args.lall
            i = lib.pysphere.list.snapshot(vm)
            # Notification
            if hasattr(args, 'notif'):
                logger.debug(
                    'Sending notification to %s from %s' %
                    (args.notif, from_snap))
                if i == 0:
                    message = '[%s] Snapshot(s) [%s] was [%s]' % (
                        action[3], vm.properties.name, status[0])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[3],
                        status[0],
                        message)
                elif i == 1:
                    message = '[%s] Snapshot(s) [%s] was [%s]' % (
                        action[3], vm.properties.name, status[1])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[3],
                        status[1],
                        message)
                elif i:
                    message = ""
                    for s in i:
                        message += s + '\n'
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[3],
                        status[1],
                        message)
            pass
        elif hasattr(args, 'sname'):
            logger.debug('Creating snapshot as requested by user.')
            # Parse create opt
            snapname = args.sname
            snapdesc = args.sdesc
            snaprun = args.ssync
            i = lib.pysphere.create.snapshot(vm, snapname, snapdesc, snaprun)

            # Notification
            if hasattr(args, 'notif'):
                logger.debug(
                    'Sending notification to %s from %s' %
                    (args.notif, from_snap))
                if i == 0:
                    message = '[%s] Snapshot [Name: %s; Desc: %s] was [%s]' % (
                        action[1], snapname, snapdesc, status[0])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[1],
                        status[0],
                        message,
                        vm.properties.name)
                elif i == 1:
                    message = '[%s] Snapshot [Name: %s; Desc: %s] was [%s]' % (
                        action[1], snapname, snapdesc, status[1])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[1],
                        status[1],
                        message,
                        vm.properties.name)
                elif i == 2:
                    message = '[%s] Snapshot [Name: %s; Desc: %s] was [%s]' % (
                        action[1], snapname, snapdesc, status[2])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[1],
                        status[2],
                        message,
                        vm.properties.name)
            pass
        elif hasattr(args, 'snamed'):
            logger.debug('Deleting snapshot as requested by user.')
            snapnamed = args.snamed
            snaprun = args.ssync
            children = args.children
            i = lib.pysphere.delete.snapshot(vm, snapnamed, snaprun, children)

            # Notification
            if hasattr(args, 'notif'):
                logger.debug(
                    'Sending notification to %s from %s' %
                    (args.notif, from_snap))
                if i == 0:
                    message = '[%s] Snapshot [Name: %s; Children: %s] was [%s]' % (
                        action[2], snapnamed, children, status[0])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[2],
                        status[0],
                        message,
                        vm.properties.name)
                elif i == 1:
                    message = '[%s] Snapshot [Name: %s; Children: %s] was [%s]' % (
                        action[2], snapnamed, children, status[1])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[2],
                        status[1],
                        message,
                        vm.properties.name)
                elif i == 2:
                    message = '[%s] Snapshot [Name: %s; Children: %s] was [%s]' % (
                        action[2], snapnamed, children, status[2])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[2],
                        status[2],
                        message,
                        vm.properties.name)
            pass
        elif hasattr(args, 'snamer'):
            logger.debug('Reverting snapshot as requested by user.')
            snapnamer = args.snamer
            snaprun = args.ssync
            i = lib.pysphere.revert.snapshot(vm, snapnamer, snaprun)
            # Notification
            if hasattr(args, 'notif'):
                logger.debug(
                    'Sending notification to %s from %s' %
                    (args.notif, from_snap))
                if i == 0:
                    message = '[%s] Snapshot [Name: %s] was [%s]' % (
                        action[4], snapnamer, status[0])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[4],
                        status[0],
                        message,
                        vm.properties.name)
                elif i == 1:
                    message = '[%s] Snapshot [Name: %s] was [%s]' % (
                        action[4], snapnamer, status[1])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[4],
                        status[1],
                        message,
                        vm.properties.name)
                elif i == 2:
                    message = '[%s] Snapshot [Name: %s] was [%s]' % (
                        action[4], snapnamer, status[2])
                    lib.logs.send.send_notification(
                        from_snap,
                        args.notif,
                        action[4],
                        status[2],
                        message,
                        vm.properties.name)
            pass
        logger.debug('Terminating vCenter session.')
        con.disconnect()
    except VIException as inst:
        logger.error(inst)
        logger.error('An unexpceted error ocurred. Program will be terminated.')
        sys.exit()

if __name__ == '__main__':  # pragma: no cover
    run()
