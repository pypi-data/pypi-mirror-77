# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
Module that contains Artella Indie API implementation
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os
import re
import sys
import json
import socket
import logging
import threading
import traceback
try:
    from urllib.request import urlopen, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, \
        install_opener
except ImportError:
    from urllib2 import urlopen, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, install_opener

from Qt.QtWidgets import *

import tpDcc as tp
from tpDcc.libs.python import osplatform
from tpDcc.libs.qt.core import qtutils

import artellapipe
from artellapipe.libs import artella as artella_lib
from artellapipe.libs.artella.core import artellaclasses

LOGGER = logging.getLogger('artellapipe-libs-artella')

global artella_client
global spigot_thread

artella_client = None
spigot_thread = None


try:
    import Artella as art
    getCmsUri = art.getCmsUri
    handleMessage = art.handleMessage
    passMsgToMainThread = art.passMsgToMainThread

except ImportError:

    def getCmsUri(broken_path):
        path_parts = re.split(r'[/\\]', broken_path)
        while len(path_parts):
            path_part = path_parts.pop(0)
            if path_part == '_art':
                relative_path = '/'.join(path_parts)
                return relative_path
        return ''

    def handleMessage(json_msg):
        pass

    def passMsgToMainThread(json_msg):
        handleMessage(json_msg)

# =================================================================================================================


def update_local_artella_root():
    """
    Updates the environment variable that stores the Artella Local Path
    NOTE: This is done by Artella plugin when is loaded, so we should not do it manually again
    """

    metadata = get_metadata()
    if metadata:
        metadata.update_local_root()
        return True

    return False


def check_artella_plugin_loaded():
    """
    Returns True if the Artella plugin is loaded in Maya or False otherwise
    :return: bool
    """

    if tp.is_maya():
        return tp.Dcc.is_plugin_loaded('Artella')

    return False


def get_artella_data_folder():
    """
    Returns last version Artella folder installation
    :return: str
    """

    if osplatform.is_mac():
        artella_folder = os.path.join(os.path.expanduser('~/Library/Application Support/'), 'Artella')
    elif osplatform.is_windows():
        artella_folder = os.path.join(os.getenv('PROGRAMDATA'), 'Artella')
    else:
        return None

    next_version = artella_lib.config.get('app', 'indie').get('next_version_filename', '')
    artella_app_version = None
    version_file = os.path.join(artella_folder, next_version)
    if os.path.isfile(version_file):
        with open(version_file) as f:
            artella_app_version = f.readline()

    if artella_app_version is not None:
        artella_folder = os.path.join(artella_folder, artella_app_version)
    else:
        artella_folder = [
            os.path.join(artella_folder, name) for name in os.listdir(artella_folder) if os.path.isdir(
                os.path.join(artella_folder, name)) and name != 'ui']
        if len(artella_folder) == 1:
            artella_folder = artella_folder[0]
        else:
            LOGGER.info('Artella folder not found!')

    LOGGER.debug('ARTELLA FOLDER: {}'.format(artella_folder))
    if not os.path.exists(artella_folder):
        qtutils.show_info(
            None, 'Artella Folder not found!',
            'Artella App Folder {} does not exists! Make sure that Artella is installed in your computer!')

    return artella_folder


def update_artella_paths():
    """
    Updates system path to add artella paths if they are not already added
    :return:
    """

    artella_folder = get_artella_data_folder()

    LOGGER.debug('Updating Artella paths from: {0}'.format(artella_folder))
    if artella_folder is not None and os.path.exists(artella_folder):
        for subdir, dirs, files in os.walk(artella_folder):
            if subdir not in sys.path:
                LOGGER.debug('Adding Artella path: {0}'.format(subdir))
                sys.path.append(subdir)


def get_artella_python_folder():
    """
    Returns folder where Artella stores Python scripts
    :return: str
    """

    return os.path.join(get_artella_data_folder(), 'python')


def get_artella_plugins_folder():
    """
    Returns folder where Artella stores its plugins
    :return: str
    """

    return os.path.join(get_artella_data_folder(), 'plugins')


def get_artella_dcc_plugin(dcc='maya'):
    """
    Gets Artella DCC plugin depending of the given dcc string
    :param dcc: str, "maya" or "nuke"
    :return: str
    """

    return os.path.join(get_artella_plugins_folder(), dcc)


def get_artella_app():
    """
    Returns path where Artella path is installed
    :return: str
    """

    artella_app_name = artella_lib.config.get('app', 'indie').get('name', 'artella')
    if osplatform.is_windows():
        artella_folder = os.path.dirname(get_artella_data_folder())
        return os.path.join(artella_folder, artella_app_name)
    elif osplatform.is_mac():
        artella_folder = os.path.dirname(get_artella_data_folder())
        return os.path.join(artella_folder, artella_app_name)
    else:
        qtutils.show_warning(
            None,
            'Platform not supported',
            'Current platform is not supported by Artella App: {}'.format(osplatform.get_sys_platform())
        )
        return ''


def get_artella_program_folder():
    """
    Returns folder where Artella shortcuts are located
    :return: str
    """

    # TODO: This only works on Windows, find a cross-platform way of doing this

    return os.path.join(os.environ['PROGRAMDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Artella')


def get_artella_launch_shortcut():
    """
    Returns path where Launch Artella shortcut is located
    :return: str
    """

    # TODO: This only works on Windows, find a cross-platform way of doing this

    return os.path.join(get_artella_program_folder(), 'Launch Artella.lnk')


def launch_artella_app():
    """
    Executes Artella App
    """

    if osplatform.is_mac():
        artella_app_file = get_artella_app() + '.bundle'
    elif osplatform.is_windows():
        artella_app_file = get_artella_launch_shortcut()
    else:
        qtutils.show_warning(
            None,
            'Platform not supported',
            'Current platform is not supported by Artella App: {}'.format(osplatform.get_sys_platform())
        )
        return

    artella_app_file = artella_app_file
    LOGGER.info('Artella App File: {0}'.format(artella_app_file))

    if os.path.isfile(artella_app_file):
        LOGGER.info('Launching Artella App ...')
        LOGGER.debug('Artella App File: {0}'.format(artella_app_file))
        os.startfile(artella_app_file.replace('\\', '//'))


def close_all_artella_app_processes():
    """
    Closes all Artella app (lifecycler.exe) processes
    :return:
    """

    artella_app_name = artella_lib.config.get('app', 'indie').get('name', 'artella')
    psutil_available = False
    try:
        import psutil
        psutil_available = True
    except ImportError:
        pass

    if psutil_available:
        try:
            for proc in psutil.process_iter():
                if proc.name() == '{}.exe'.format(artella_app_name):
                    LOGGER.debug('Killing Artella App process: {}'.format(proc.name()))
                    proc.kill()
            return True
        except RuntimeError:
            LOGGER.error('Impossible to close Artella app instances because psutil library is not available!')
            return False

    return False


def connect_artella_app_to_spigot(cli=None, app_identifier=None):
    """
    Creates a new Spigot Client instance and makes it to listen
    to our current installed (and launched) Artella app
    """

    # TODO: Check if Artella App is launched and, is not, launch it

    def get_handle_msg(json_msg):
        if tp.is_houdini():
            try:
                msg = json.loads(json_msg)
            except Exception:
                LOGGER.warning('Unknown command!')
        else:
            return handleMessage(json_msg)

    if cli is None:
        cli = get_artella_client()

    artella_app_identifier = get_artella_app_identifier()
    if not artella_app_identifier and app_identifier:
        artella_app_identifier = app_identifier

    if tp.is_maya():
        pass_msg_fn = passMsgToMainThread
    elif tp.is_houdini():
        def pass_msg_to_main_thread(json_msg):
            from tpDcc.dccs.houdini.core import helpers
            main_thread_fn = helpers.get_houdini_pass_main_thread_function()
            main_thread_fn(get_handle_msg, json_msg)
        pass_msg_fn = pass_msg_to_main_thread
    else:
        def pass_msg(json_msg):
            get_handle_msg(json_msg)
        pass_msg_fn = pass_msg

    if tp.Dccs.Unknown:
        spigot_listen(cli, artella_app_identifier, pass_msg_fn)
    else:
        cli.listen(artella_app_identifier, pass_msg_fn)

    return cli


def spigot_listen(cli, app_id, handler):
    """
    Function that creates Spigot Thread.
    We use it in non DCC Python apps to properly close thread when the app is closed
    :param cli: SpigotClient
    :param appId:str
    :param handler: fn
    """

    global spigot_thread

    spigot_thread = threading.Thread(
        target=cli._pullMessages,
        args=(app_id, handler)
    )

    # Demonize thread to make sure that thread is automatically closed when Python interpreter is closed
    spigot_thread.daemon = True
    spigot_thread.start()


def load_artella_maya_plugin():
    """
    Loads the Artella plugin in the current Maya session
    :return: bool
    """

    if not tp.is_maya():
        return False

    artella_plugin_name = artella_lib.config.get('app', 'indie').get('plugin', '')
    LOGGER.debug('Loading Artella Maya Plugin: {} ...'.format(artella_plugin_name))
    artella_maya_plugin_folder = get_artella_dcc_plugin(dcc='maya')
    artella_maya_plugin_file = os.path.join(artella_maya_plugin_folder, artella_plugin_name)
    if os.path.isfile(artella_maya_plugin_file):
        if not tp.Dcc.is_plugin_loaded(artella_plugin_name):
            tp.Dcc.load_plugin(artella_maya_plugin_file)
            return True

    return False


def get_artella_client(app_identifier=None, force_create=True):
    """
    Creates, connects and returns an instance of the Spigot client
    :return: SpigotClient
    """

    global artella_client

    if artella_client is None and force_create:
        if tp.is_maya():
            from tpDcc.dccs.maya.core import gui
            gui.force_stack_trace_on()
        from am.artella.spigot.spigot import SpigotClient
        artella_client = SpigotClient()
        connect_artella_app_to_spigot(artella_client, app_identifier=app_identifier)

    return artella_client


def get_artella_app_identifier():
    """
    Returns the installed Artella App identifier
    :return: variant, str || None
    """

    app_identifier = os.environ.get('ARTELLA_APP_IDENTIFIER', None)
    if app_identifier is None:
        app_identifier = tp.Dcc.get_version_name()
        if tp.is_maya():
            app_identifier = 'maya.{}'.format(app_identifier.split()[0])

    return app_identifier


def fix_path_by_project(project, path, fullpath=False):
    """
    Fix given path and updates to make it relative to the Artella project
    :param project: ArtellaProject
    :param path: str, path to be fixed
    :return: str
    """

    artella_root_prefix = artella_lib.config.get('app', 'indie').get('root_prefix', 'ART_LOCAL_ROOT')
    project_path = project.get_path()
    new_path = path.replace(project_path, '${}\\'.format(artella_root_prefix))
    if fullpath:
        new_path = path.replace(project_path, '${}'.format(artella_root_prefix) + '/' + project.full_id)
    return new_path


def get_metadata():
    """
    Returns Artella App MetaData
    :return: ArtellaMetaData or None
    """

    client = get_artella_client()

    try:
        rsp = client.execute(command_action='do', command_name='getMetaData', payload='{}')
    except socket.error as exc:
        # LOGGER.debug(exc)
        return None

    rsp = json.loads(rsp)

    metadata = artellaclasses.ArtellaAppMetaData(
        cms_web_root=rsp['cms_web_root'],
        local_root=rsp['local_root'],
        storage_id=rsp['storage_id'],
        token=rsp['token']
    )

    return metadata


def get_cms_uri(path):
    """
    Returns the CMS uri of the given path, if exists
    :param path: str
    :return: dict
    """

    if not path:
        return path

    path = os.path.normpath(path)
    cms_uri = getCmsUri(path)
    if not cms_uri:
        LOGGER.debug('Unable to get CMS uri from path: {0}'.format(path))
        return False

    req = json.dumps({'cms_uri': cms_uri})
    return req


def get_cms_uri_current_file():
    """
    Returns the CMS uri of the current file
    :return: str
    """

    current_file = tp.Dcc.scene_name()
    LOGGER.debug('Getting CMS Uri of file {0}'.format(current_file))

    cms_uri = getCmsUri(current_file)
    if not cms_uri:
        LOGGER.debug('Unable to get CMS uri from path: {0}'.format(current_file))
        return False

    LOGGER.debug('Retrieved CMS uri: {0}'.format(cms_uri))
    req = json.dumps({'cms_uri': cms_uri})

    return req


def get_status(file_path, **kwargs):
    """
    Returns the status of  the given file path
    :param file_path: str
    :return: str
    """

    as_json = kwargs.get('as_json', False)
    max_tries = kwargs.get('max_tries', 3)

    if max_tries > 50:
        max_tries = 50

    uri = get_cms_uri(file_path)
    if not uri:
        LOGGER.debug('Unable to get cmds uri from path: {}'.format(file_path))
        return False

    spigot = get_artella_client()

    current_try = 0
    rsp = None

    while current_try < max_tries:
        try:
            rsp = spigot.execute(command_action='do', command_name='status', payload=uri)
        except Exception as exc:
            LOGGER.debug(exc)
        if rsp and isinstance(rsp, (str, unicode)):
            try:
                rsp = json.loads(rsp)
                break
            except Exception:
                pass
        current_try += 1

    if current_try >= max_tries:
        msg = 'Artella is not available at this moment ... Restart Maya and try again please!'
        LOGGER.debug(msg)
        if artellapipe.project:
            artellapipe.project.message(msg)
        return {}

    if as_json:
        return rsp

    # Artella is down!!!!!
    if not rsp:
        msg = 'Artella is not available at this moment ... Restart Maya and try again please!'
        LOGGER.debug(msg)
        if artellapipe.project:
            artellapipe.project.message(msg)
        return None

    if 'data' in rsp:
        if '_latest' in rsp['data']:
            status_metadata = artellaclasses.ArtellaAssetMetaData(metadata_path=file_path, status_dict=rsp)
            return status_metadata

        status_metadata = artellaclasses.ArtellaDirectoryMetaData(metadata_path=file_path, status_dict=rsp)
    else:
        status_metadata = artellaclasses.ArtellaHeaderMetaData(header_dict=rsp['meta'])

    return status_metadata


def get_status_current_file():
    """
    Returns the status of the current file
    :return:
    """

    current_file = tp.Dcc.scene_name()
    LOGGER.debug('Getting Artella Status of file {0}'.format(current_file))

    status = get_status(current_file)
    LOGGER.debug('{0} STATUS -> {1}'.format(current_file, status))

    return status


def explore_file(path):
    """
    Opens the current file in the file explorer
    :param path: str
    """

    uri = get_cms_uri(path)
    spigot = get_artella_client()
    rsp = spigot.execute(command_action='do', command_name='explore', payload=uri)

    if isinstance(rsp, (unicode, str)):
        rsp = json.loads(rsp)

    return rsp


def pause_synchronization():
    """
    Pauses synchronization of files from Artella server
    """

    pass


def resume_synchronization():
    """
    Resumes synchronization of files from Artella server
    """

    pass


def get_synchronization_progress():
    """
    Returns the progress of the current Artella server synchronization operation
    Returns a tuple containing the following info:
        - amount of done download operations
        - amount of total download operations in progress
        - amount of total download operations that are going to be done
        - amount of total bytes downloaded
        - amount of total bytes to download
    :return: int, int, int, int, int
    """

    return 0, 0, 0, 0, 0


def synchronize_path(path):
    """
    Synchronize all the content of the given path, if exists
    :param path: str
    """

    uri = get_cms_uri(path)
    spigot = get_artella_client()
    rsp = spigot.execute(command_action='do', command_name='updateCollection', payload=uri)

    if isinstance(rsp, (unicode, str)):
        rsp = json.loads(rsp)

    return rsp


def synchronize_file(file_path):
    """
    Synchronize the specific given file, if exists
    :param file_path: str
    :return:
    """

    try:
        uri = get_cms_uri(file_path)
        spigot = get_artella_client()
        rsp = spigot.execute(command_action='do', command_name='update', payload=uri)

        if isinstance(rsp, (unicode, str)):
            rsp = json.loads(rsp)

        return rsp
    except Exception:
        LOGGER.error(traceback.format_exc())
        return None


def synchronize_path_with_folders(file_path, recursive=False, only_latest_published_versions=True):
    """
    Synchronizes given path and all its folders
    :param file_path: str
    :param recursive: bool
    :param only_latest_published_versions: bool
    :return:
    """

    try:
        status = get_status(file_path)
        if isinstance(status, artellaclasses.ArtellaDirectoryMetaData):
            references = status.references
            for ref_name, ref_data in references.items():
                ref_path = ref_data.path
                if ref_data.is_directory:
                    synchronize_path(ref_path)
                    if recursive:
                        synchronize_path_with_folders(ref_path, recursive=True)
                else:
                    synchronize_file(ref_path)
            return True
        else:
            if os.path.isdir(file_path):
                child_dirs = list()
                # status = get_status(file_path)
                if isinstance(status, artellaclasses.ArtellaDirectoryMetaData):
                    for ref_name, ref_data in status.references.items():
                        dir_path = ref_data.path
                        if os.path.isdir(dir_path) or os.path.splitext(dir_path)[-1]:
                            continue
                        child_dirs.append(dir_path)
                elif isinstance(status, artellaclasses.ArtellaAssetMetaData):
                    working_folder = artellapipe.project.get_working_folder()
                    working_path = os.path.join(status.path, working_folder)
                    artella_data = get_status(working_path)
                    if isinstance(artella_data, artellaclasses.ArtellaDirectoryMetaData):
                        child_dirs.append(working_path)

                    if only_latest_published_versions:
                        published_versions = status.get_latest_published_versions(force_update=True)
                    else:
                        published_versions = status.get_published_versions(force_update=True)
                    if published_versions:
                        for version_name, version_data_list in published_versions.items():
                            for version_data in version_data_list:
                                version_path = version_data[2]
                                # No need to check path status because published versions function already does that
                                child_dirs.append(version_path)

                if child_dirs:
                    for child_dir in child_dirs:
                        synchronize_path_with_folders(child_dir, recursive=recursive)
                return True
    except Exception:
        LOGGER.error(traceback.format_exc())
        return None

    return False


def get_artella_project_url(project_id, files_url=True):
    """
    Returns Artella project URL
    :param project_id: str, Unique ID for the Artella project
    :param files_url: bool, Whether to return root project URL of project files URL
    :return: str
    """

    artella_web = artellapipe.libs.artella.config.get('server', dict()).get('url', 'https://indie.artella.com')
    artella_url = '{}/project/{}'.format(artella_web, project_id)

    return artella_url if not files_url else '{}/files'.format(artella_url)


def split_version(name, next_version=False):
    """
    Returns the version of a specific given asset (model_v001, return [v001, 001, 1])
    :param name: str
    :param next_version: bool
    :return: list(str, int, int)
    """

    string_version = name[-7:]
    int_version = map(int, re.findall(r'\d+', string_version))[0]
    int_version_formatted = '{0:03}'.format(int_version)
    if next_version:
        new_int_version = int_version + 1
        new_int_version_formatted = '{0:03}'.format(new_int_version)
        new_string_version = string_version.replace(int_version_formatted, new_int_version_formatted)
        return new_string_version, new_int_version, new_int_version_formatted

    return string_version, int_version, int_version_formatted


def get_file_history(file_path, as_json=False):
    """
    Returns the history info of the given file, if exists
    :param file_path: str
    :param as_json: bool
    """

    uri = get_cms_uri(file_path)
    spigot = get_artella_client()
    rsp = spigot.execute(command_action='do', command_name='history', payload=uri)

    try:
        if isinstance(rsp, (unicode, str)):
            rsp = json.loads(rsp)
    except Exception as e:
        msg = 'Error while getting file history info: {}'.format(rsp)
        LOGGER.error(msg)
        LOGGER.error(str(e))
        return {}

    if as_json:
        return rsp

    if 'data' in rsp:
        file_metadata = artellaclasses.ArtellaFileMetaData(file_dict=rsp)
        return file_metadata

    return rsp


def get_asset_image(asset_path, project_id):
    """
    Returns the asset image from Artella server
    :param asset_path: str, path of the asset relative to the Assets folder
    :param project_id: str, ID of the Artella project you are currently working
    :return:
    """

    # TODO: Authentication problem when doing request: look for workaround
    image_url = os.path.join('https://cms-static.artella.com/cms_browser/thumbcontainerAvatar', project_id, asset_path)
    data = urlopen(image_url).read()

    return data


def launch_maya(file_path, maya_version=None):
    """
    :param file_path: str
    :param maya_version: int
    :return:
    """

    if not tp.is_maya():
        return

    if maya_version is None:
        maya_version = tp.Dcc.get_version()

    spigot = get_artella_client()

    payload = dict()
    payload['appName'] = "maya.{0}".format(str(maya_version))
    payload['parameter'] = "\"{0}\"".format(file_path)
    payload['wait'] = "60"
    payload = json.dumps(payload)
    rsp = spigot.execute(command_action='do', command_name='launchApp', payload=payload)
    if isinstance(rsp, (unicode, str)):
        rsp = json.loads(rsp)

    return rsp


def open_file_in_maya(file_path, maya_version=None):
    """
    Open the given path in the given Maya version
    :param file_path: str
    :param maya_version: int
    """

    if not tp.is_maya():
        return None

    if maya_version is None:
        maya_version = tp.Dcc.get_version()

    spigot = get_artella_client()

    # Firt we try to open the app if its not launched
    launch_maya(file_path=file_path, maya_version=maya_version)

    # Now we open the file
    payload = dict()
    payload['appId'] = "maya.{0}".format(str(maya_version))
    payload['message'] = "{\"CommandName\":\"open\",\"" \
                         "CommandArgs\":{\"path\":\"" + file_path + "\"}}".replace('\\', '/')
    payload['message'] = payload['message'].replace('\\', '/').replace('//', '/')
    payload = json.dumps(payload)

    rsp = spigot.execute(command_action='do', command_name='passToApp', payload=payload)

    if isinstance(rsp, (unicode, str)):
        rsp = json.loads(rsp)

    return rsp


def import_file_in_maya(file_path, maya_version=None):
    """
    Import the given asset path in the given Maya version current scene
    :param file_path: str
    :param maya_version: int
    """

    if not tp.is_maya():
        return None

    if maya_version is None:
        maya_version = tp.Dcc.get_version()

    spigot = get_artella_client()

    payload = dict()
    payload['appId'] = "maya.{0}".format(str(maya_version))
    payload['message'] = "{\"CommandName\":\"import\"," \
                         "\"CommandArgs\":{\"path\":\"" + file_path + "\"}}".replace('\\', '/')
    payload['message'] = payload['message'].replace('\\', '/').replace('//', '/')
    payload = json.dumps(payload)

    rsp = spigot.execute(command_action='do', command_name='passToApp', payload=payload)

    if isinstance(rsp, (unicode, str)):
        rsp = json.loads(rsp)

    return rsp


def reference_file_in_maya(file_path, maya_version=None):
    """
    Import the given asset path in the given Maya version current scene
    :param file_path: str
    :param maya_version: int
    """

    if not tp.is_maya():
        return None

    if maya_version is None:
        maya_version = tp.Dcc.get_version()

    spigot = get_artella_client()

    payload = dict()
    payload['appId'] = "maya.{0}".format(str(maya_version))
    payload['message'] = "{\"CommandName\":\"reference\"," \
                         "\"CommandArgs\":{\"path\":\"" + file_path + "\"}}".replace('\\', '/')
    payload['message'] = payload['message'].replace('\\', '/').replace('//', '/')
    payload = json.dumps(payload)

    rsp = spigot.execute(command_action='do', command_name='passToApp', payload=payload)

    if isinstance(rsp, (unicode, str)):
        rsp = json.loads(rsp)

    return rsp


def is_published(file_path):
    """
    Returns whether an absolute file path refers to a published asset
    :param file_path: str, absolute path to a file
    :return: bool
    """

    rsp = get_status(file_path=file_path, as_json=True)
    if not rsp:
        return False

    meta = rsp.get('meta', {})
    if meta.get('status') != 'OK':
        LOGGER.info('Status is not OK: {}'.format(meta))
        return False

    return 'release_name' in meta


def is_updated(file_path):
    """
    Returns whether or not given file path is updated to the last version
    :param file_path: str
    :return: bool
    """

    rsp = get_status(file_path=file_path)
    if rsp:
        if isinstance(rsp, artellaclasses.ArtellaDirectoryMetaData):
            is_updated = False
            if rsp.header.status != 'OK':
                LOGGER.info('Status is not OK: {}'.format(rsp))
                return False
            for name, ref in rsp.references.items():
                if ref.view_version < ref.maximum_version:
                    return False
                else:
                    is_updated = True
            return is_updated
        elif isinstance(rsp, artellaclasses.ArtellaReferencesMetaData):
            return rsp.view_version < rsp.maximum_version
        else:
            # We return None in files that are only in local (not in server)
            return None

    return False


def is_locked(file_path):
    """
    Returns whether an absolute file path refers to a locked asset in edit mode, and if the file is locked
    by the current storage workspace
    :param file_path: str, absolute path to a file
    :return: (bool, bool), Whether file is locked or not, whether the file is locked by another user or not
    """

    rsp = get_status(file_path=file_path)
    if rsp:
        if isinstance(rsp, artellaclasses.ArtellaDirectoryMetaData):
            if rsp.header.status != 'OK':
                LOGGER.info('Status is not OK: {}'.format(rsp))
                return False, False

            file_path = rsp.header.file_path or ''
            if not file_path or file_path == '':
                LOGGER.info('File path not found in response: {}'.format(rsp))
                return False, False

            for ref, ref_data in rsp.references.items():
                file_data = ref_data.path
                if not file_data:
                    LOGGER.info('File data not found in response: {}'.format(rsp.get('data', {}), ))
                    return
                if ref_data.locked:
                    user_id = get_current_user_id()
                    return True, user_id == ref_data.locked_view
        elif isinstance(rsp, artellaclasses.ArtellaHeaderMetaData):
            if rsp.status != 'OK':
                LOGGER.info('Status is not OK: {}'.format(rsp))
                return False, False

            file_path_header = rsp.file_path or ''
            if not file_path_header or file_path_header == '':
                LOGGER.info('File path not found in response: {}'.format(rsp))
                return False, False

            # This happens when we are trying to lock a file that has not been uploaded to Artella yet
            return None, None

    return False, False


def lock_file(file_path=None, force=False):
    """
    Locks given file path
    :param file_path: str
    :param force: bool
    """

    if not file_path:
        file_path = tp.Dcc.scene_name()
    if not file_path:
        LOGGER.error('File {} cannot be locked because it does not exists!'.format(file_path))
        return False

    file_published = is_published(file_path=file_path)
    if file_published:
        msg = 'Current file ({}) is published and cannot be edited'.format(os.path.basename(file_path))
        LOGGER.info(msg)
        if hasattr(artellapipe, 'project') and artellapipe.project:
            artellapipe.project.message(msg)
        return False

    in_edit_mode, is_locked_by_me = is_locked(file_path=file_path)
    can_write = os.access(file_path, os.W_OK)
    if not can_write and is_locked_by_me:
        msg = 'Unable to check local write permissions for file: {}'.format(file_path)
        LOGGER.info(msg)
        if hasattr(artellapipe, 'project') and artellapipe.project:
            artellapipe.project.message(msg)

    if in_edit_mode is None and is_locked_by_me is None:
        msg = 'File is not versioned yet! '
        LOGGER.info(msg)
        return True

    if in_edit_mode and not is_locked_by_me:
        msg = 'Locked by another user or workspace or file is not uploaded to Artella yet: {}'.format(
            os.path.basename(file_path))
        LOGGER.info(msg)
        tp.Dcc.warning(msg)
        return False
    elif force or not in_edit_mode:
        result = 'Yes'
        if not force and not in_edit_mode:
            msg = '{} needs to be in Edit mode to save your file. Would like to turn edit mode on now?'.format(
                os.path.basename(file_path))
            LOGGER.info(msg)
            if artellapipe.project:
                artellapipe.project.message(msg)
            result = tp.Dcc.confirm_dialog(
                title='Artella Pipeline - Lock File',
                message=msg, button=['Yes', 'No'], cancel_button='No', dismiss_string='No')
        if result != 'Yes':
            return False

    spigot = get_artella_client()
    payload = dict()
    payload['cms_uri'] = getCmsUri(file_path)
    payload = json.dumps(payload)

    rsp = spigot.execute(command_action='do', command_name='checkout', payload=payload)

    if isinstance(rsp, (unicode, str)):
        rsp = json.loads(rsp)

    LOGGER.debug('Server checkout response: {}'.format(rsp))

    if rsp.get('meta', {}).get('status') != 'OK':
        msg = 'Failed to lock {}'.format(os.path.basename(file_path))
        LOGGER.info(msg)
        tp.Dcc.warning(msg)
        return False

    return True


def unlock_file(file_path, **kwargs):
    """
    Unlocks a given file path
    :param file_path:
    """

    spigot = get_artella_client()
    payload = dict()
    payload['cms_uri'] = getCmsUri(file_path)
    payload = json.dumps(payload)

    if not can_unlock(file_path=file_path):
        LOGGER.debug('Impossible to unlock file. File is locked by other user!')
        return False

    rsp = spigot.execute(command_action='do', command_name='unlock', payload=payload)

    if isinstance(rsp, (unicode, str)):
        rsp = json.loads(rsp)

    # if rsp.get('status', {}).get('meta', {}).get('status') != 'OK':

    if rsp:
        if rsp.get('meta', {}).get('status') != 'OK':
            msg = 'Failed to unlock {}'.format(os.path.basename(file_path))
            LOGGER.info(msg)
            return False
    else:
        return False

    return True


def upload_file(file_path, comment):
    """
    Uploads a new version of the given file to Artella server
    :param file_path: str
    :param comment: str
    """

    spigot = get_artella_client()
    payload = dict()
    cms_uri = getCmsUri(file_path)
    if not cms_uri.startswith('/'):
        cms_uri = '/' + cms_uri
    payload['cms_uri'] = cms_uri
    payload['comment'] = comment
    payload = json.dumps(payload)

    rsp = spigot.execute(command_action='do', command_name='upload', payload=payload)
    if isinstance(rsp, (str, unicode)):
        rsp = json.loads(rsp)

    if rsp.get('status', {}).get('meta', {}).get('status') != 'OK':
        msg = 'Failed to publish version to Artella {}'.format(os.path.basename(file_path))
        LOGGER.info(msg)
        tp.Dcc.warning(msg)
        tp.Dcc.confirm_dialog(
            title='Artella Pipeline -  Failed to Upload Bug. Restart DCC please!', message=msg, button=['OK'])
        return False

    return True


def get_current_user_id():
    """
    Returns Artella ID of the current user
    :return: str
    """

    metadata = get_metadata()
    if not metadata:
        return None
    return metadata.storage_id


def can_unlock(file_path, **kwargs):
    """
    Returns whether given path can be unlocked or not by current user
    :param file_path: str
    :return: bool
    """

    asset_status = get_status(file_path=file_path)
    if not asset_status:
        return False

    if type(asset_status) == artellaclasses.ArtellaHeaderMetaData:
        LOGGER.debug('File {} is not uploaded on Artella yet, so you cannot unlock it!')
        return False

    asset_info = asset_status.references.values()[0]
    locker_name = asset_info.locked_view
    user_id = get_current_user_id()

    if locker_name is not None and locker_name != user_id:
        return False

    return True


def upload_new_asset_version(file_path=None, comment='Published new version with Artella Pipeline', skip_saving=False):
    """
    Adds a new file to the Artella server
    :param file_path:
    :param comment:
    :param skip_saving: When we publish textures we do not want to save the maya scene
    """

    if not file_path:
        file_path = tp.Dcc.scene_name()
    if not file_path:
        LOGGER.error('File {} cannot be locked because it does not exists!'.format(file_path))
        return False

    msg = 'Making new version for {}'.format(file_path)
    LOGGER.info(msg)
    if artellapipe.project:
        artellapipe.project.message(msg)
    if file_path is not None and file_path != '':
        valid_lock = lock_file(file_path=file_path)
        if not valid_lock:
            return False

        if not skip_saving:
            if tp.Dcc.scene_is_modified():
                tp.Dcc.save_current_scene(force=True)
            if tp.is_maya():
                from tpDcc.dccs.maya.core import helpers
                if helpers.file_has_student_line(filename=file_path):
                    helpers.clean_student_line(filename=file_path)
                    if helpers.file_has_student_line(filename=file_path):
                        LOGGER.error('After updating model path the Student License could not be fixed again!')
                        return False

        msg = 'Saving new file version on Artella Server: {}'.format(file_path)
        LOGGER.info(msg)
        if artellapipe.project:
            artellapipe.project.message(msg)
        if comment is None:
            result = tp.Dcc.confirm_dialog(
                title='Artella Pipeline - Save New Version on Artella Server', message=msg, button=['Save', 'Cancel'],
                cancel_button='Cancel', dismiss_string='Cancel')
            if result == 'Save':
                comment = qtutils.get_comment(title='Comment')
            else:
                return False

        spigot = get_artella_client()
        payload = dict()
        cms_uri = getCmsUri(file_path)
        if not cms_uri.startswith('/'):
            cms_uri = '/' + cms_uri
        payload['cms_uri'] = cms_uri
        payload['comment'] = comment
        payload = json.dumps(payload)

        rsp = spigot.execute(command_action='do', command_name='upload', payload=payload)
        if isinstance(rsp, (unicode, str)):
            rsp = json.loads(rsp)

        if 'status' in rsp and 'meta' in rsp['status'] and rsp['status']['meta']['status'] != 'OK':
            LOGGER.info('Make new version response: {}'.format(rsp))
            msg = 'Failed to make new version of {}'.format(os.path.basename(file_path))

            tp.Dcc.confirm_dialog(title='Artella Pipeline - Failed to Make New Version', message=msg, button=['Ok'])
            return False

        unlock_file(file_path=file_path)

    else:
        msg = 'The file has not been created yet'
        LOGGER.debug(msg)
        tp.Dcc.warning(msg)
        tp.Dcc.confirm_dialog(title='Artella Pipeline - Failed to Make New Version', message=msg, button=['Ok'])

    return True


def publish_asset(asset_path, comment, selected_versions, version_name):
    """
    Publish a new version of the given asset
    :param asset_path:
    :param comment:
    :param selected_versions:
    :param version_name:
    """

    spigot = get_artella_client()
    payload = dict()
    payload['cms_uri'] = '/' + getCmsUri(asset_path) + '/' + version_name
    payload['comment'] = comment
    payload['selectedVersions'] = selected_versions
    payload = json.dumps(payload)

    rsp = spigot.execute(command_action='do', command_name='createRelease', payload=payload)

    if isinstance(rsp, (unicode, str)):
        rsp = json.loads(rsp)

    return rsp


def get_local_working_version(file_path):
    """
    Returns current version of the given file in Artella server
    :param file_path: str
    :return: int
    """

    if not file_path or not os.path.exists(file_path):
        return -1

    history = get_file_history(file_path)
    file_versions = history.versions
    if not file_versions:
        current_version = 0
    else:
        current_version = 0
        for v in file_versions:
            if int(v[0]) > current_version:
                current_version = int(v[0])

    return current_version


def get_current_version(file_path):
    """
    Returns current published version of the given file path in Artella server
    :param file_path: str
    :return: int
    """

    current_versions = dict()

    rsp = get_status(file_path=file_path)
    if rsp:
        if isinstance(rsp, artellaclasses.ArtellaDirectoryMetaData):
            if rsp.header.status != 'OK':
                LOGGER.info('Status is not OK: {}'.format(rsp))
                return False
            for name, ref in rsp.references.items():
                if ref.view_version is not None:
                    current_versions[ref.name] = ref.view_version
                else:
                    current_versions[ref.name] = 0
        elif isinstance(rsp, artellaclasses.ArtellaReferencesMetaData):
            current_versions[rsp.name] = rsp.view_version
        elif isinstance(rsp, artellaclasses.ArtellaAssetMetaData):
            current_versions = rsp.get_published_versions()
        else:
            return current_versions

    return current_versions


def get_latest_version(file_path, check_validity=True):
    """
    Returns last version of the given file path in Artella server
    :param file_path: str
    :param check_validity: bool
    :return: int
    """

    maximum_versions = dict()

    rsp = get_status(file_path=file_path)
    if rsp:
        if isinstance(rsp, artellaclasses.ArtellaDirectoryMetaData):
            if rsp.header.status != 'OK':
                LOGGER.info('Status is not OK: {}'.format(rsp))
                return False
            for name, ref in rsp.references.items():
                maximum_versions[ref.name] = ref.maximum_version
        elif isinstance(rsp, artellaclasses.ArtellaReferencesMetaData):
            maximum_versions[rsp.name] = rsp.maximum_version
        elif isinstance(rsp, artellaclasses.ArtellaAssetMetaData):
            maximum_versions = dict()
            published_versions = rsp.get_published_versions(check_validity=check_validity)
            for file_name_version, info_version in published_versions.items():
                if not file_name_version.startswith('__'):
                    file_name_version = '__{}'.format(file_name_version)
                if not file_name_version.endswith('__'):
                    file_name_version = '{}__'.format(file_name_version)
                file_version = split_version(file_name_version)
                file_name = file_name_version.replace(file_version[0], '').replace('__', '')
                if file_name not in maximum_versions:
                    maximum_versions[file_name] = 0
                if file_version[1] > maximum_versions[file_name]:
                    maximum_versions[file_name] = file_version[1]
        else:
            return maximum_versions

    return maximum_versions


def within_artella_scene():
    """
    Returns True if the current Maya scene corresponds to a Artella Maya scene
    :return: bool
    """

    current_scene = tp.Dcc.scene_name() or 'untitled'
    LOGGER.debug('Current scene name: {}'.format(current_scene))
    if 'artella' not in current_scene.lower():
        return False
    return True


def get_user_avatar(user_id):
    """
    Downloads from Artella the avatar of the given user id
    Only works if the user is loaded before to Artella
    :param user_id: str
    :return:
    """

    project_type = artellapipe.project.get_project_type()
    artella_cms_url = artella_lib.config.get('server', project_type).get('cms_url')
    manager = HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, artella_cms_url, 'default', 'default')
    auth = HTTPBasicAuthHandler(manager)
    opener = build_opener(auth)
    install_opener(opener)
    response = urlopen('{0}/profile/{1}/avatarfull.img'.format(artella_cms_url, user_id))

    return response


def get_dependencies(file_path):
    """
    Returns a list with all the dependencies
    :param file_path: str
    :return: dict
    """

    if not file_path:
        file_path = tp.Dcc.scene_name()
    if not file_path:
        LOGGER.error('File {} cannot be locked because it does not exists!'.format(file_path))
        return False

    if file_path is not None and file_path != '':
        spigot = get_artella_client()
        payload = dict()
        payload['cms_uri'] = getCmsUri(file_path)
        payload = json.dumps(payload)

        rsp = spigot.execute(command_action='do', command_name='getDependencies', payload=payload)

        if isinstance(rsp, (unicode, str)):
            rsp = json.loads(rsp)

        return rsp

    return None


def create_asset(asset_name, asset_path):
    """
    Creates an asset with given name and in given path
    :param asset_name: str
    :param asset_path: str
    :return: dict
    """

    full_path = os.path.join(asset_path, asset_name)
    if os.path.exists(full_path):
        LOGGER.warning('Impossible to create already existing asset!')
        return False

    spigot = get_artella_client()
    payload = dict()
    payload['cms_uri'] = getCmsUri(full_path)
    payload = json.dumps(payload)

    rsp = spigot.execute(command_action='do', command_name='createContainer', payload=payload)

    if isinstance(rsp, (unicode, str)):
        rsp = json.dumps(rsp)

    return rsp


def delete_file(file_path):
    """
    Removes given file from Artella server
    :param file_path: str
    :return: dict
    """

    spigot = get_artella_client()
    payload = dict()
    payload['cms_uri'] = getCmsUri(file_path)
    payload = json.dumps(payload)

    rsp = spigot.execute(command_action='do', command_name='delete', payload=payload)

    if isinstance(rsp, (unicode, str)):
        rsp = json.dumps(rsp)

    return rsp


def rename_file(file_path, new_name):
    """
    Renames given file with new given name
    :param file_path: str
    :param new_name: str
    """

    res = qtutils.show_question(
        None, 'Confirm Rename',
        'Are you you would like to rename "{}" to "{}"?Any references to this file will need to be updated.'.format(
            os.path.basename(file_path), new_name))
    if res != QMessageBox.Yes:
        return

    dir_name = os.path.dirname(file_path)
    file_ext = os.path.splitext(file_path)[-1]
    if file_ext:
        if not new_name.endswith(file_ext):
            new_name += file_ext
    else:
        file_ext = os.path.splitext(file_path)[-1]
        if file_ext:
            new_name = file_ext[0]
    new_path = os.path.join(dir_name, new_name)

    spigot = get_artella_client()
    payload = dict()
    payload['cms_uri'] = getCmsUri(file_path)
    payload['dst_uri'] = getCmsUri(new_path)
    payload = json.dumps(payload)

    rsp = spigot.execute(command_action='do', command_name='rename', payload=payload)

    if isinstance(rsp, (unicode, str)):
        rsp = json.dumps(rsp)

    return rsp


def new_folder(root_path, folder_name):
    """
    Creates a new folder in the given path
    :param root_path: str
    :param folder_name: str
    """

    if not folder_name:
        folder_name = qtutils.get_string_input('Folder Name', 'Create Folder')
        if not folder_name:
            return

    file_path = os.path.join(root_path, folder_name)

    spigot = get_artella_client()
    payload = dict()
    payload['cms_uri'] = getCmsUri(file_path)
    payload['new_folder'] = True
    payload = json.dumps(payload)

    rsp = spigot.execute(command_action='do', command_name='upload', payload=payload)

    if isinstance(rsp, (unicode, str)):
        rsp = json.dumps(rsp)

    return rsp
