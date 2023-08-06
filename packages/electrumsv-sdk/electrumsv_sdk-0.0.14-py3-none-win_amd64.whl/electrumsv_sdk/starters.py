import asyncio
import json
import logging
import subprocess
import sys
import time
import aiorpcx
import requests
from electrumsv_node import electrumsv_node
from electrumsv_sdk.utils import trace_pid

from .constants import STATUS_MONITOR_API
from .status_monitor_client import StatusMonitorClient

from .components import Component, ComponentName, ComponentType, ComponentState, ComponentStore

logger = logging.getLogger("starters")


class Starters:
    def __init__(self, app_state):
        self.app_state = app_state
        self.component_store = ComponentStore(self.app_state)
        self.status_monitor_client = StatusMonitorClient(self.app_state)

    def spawn_in_new_console(self, command):
        if sys.platform in ('linux', 'darwin'):
            process = subprocess.Popen(f"gnome-terminal -- {command}", shell=True,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            process.wait()
            process_handle = trace_pid(command)
        else:
            process_handle = subprocess.Popen(
                f"{command}", creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        return process_handle

    async def is_electrumx_running(self):
        for sleep_time in (1, 2, 3):
            try:
                logger.debug("polling electrumx...")
                async with aiorpcx.connect_rs(host="127.0.0.1", port=51001) as session:
                    result = await session.send_request("server.version")
                    if result[1] == "1.4":
                        return True
            except Exception as e:
                pass

            await asyncio.sleep(sleep_time)
        return False

    def is_electrumsv_running(self):
        for sleep_time in (3, 3, 3):
            try:
                logger.debug("polling electrumsv...")
                result = requests.get("http://127.0.0.1:9999/")
                result.raise_for_status()
                assert result.json()["status"] == "success"
                return True
            except Exception as e:
                pass

            time.sleep(sleep_time)
        return False

    def is_status_monitor_running(self) -> bool:
        try:
            result = requests.get(STATUS_MONITOR_API + "/get_status")
            result.raise_for_status()
            return True
        except Exception as e:
            logger.error("problem fetching status: reason: " + str(e))
            return False

    def start_node(self):
        process_pid = electrumsv_node.start()

        component = Component(
            pid=process_pid,
            process_name=ComponentName.NODE,
            process_type=ComponentType.NODE,
            endpoint="http://127.0.0.1:18332",
            component_state=ComponentState.NONE,
            location=None,
            metadata={},
            logging_path=None,
        )
        while not electrumsv_node.is_running():
            logger.debug("polling bitcoin daemon...")
            time.sleep(5)
        if not electrumsv_node.is_running():
            component.component_state = ComponentState.Failed
            logger.error("bitcoin daemon failed to start")
        else:
            component.component_state = ComponentState.Running
            logger.debug("bitcoin daemon online")
        self.component_store.update_status_file(component)
        self.status_monitor_client.update_status(component)

        # process handle not returned because node is stopped via rpc

    def run_electrumx_server(self):
        logger.debug(f"starting RegTest electrumx server...")
        if sys.platform == "win32":
            electrumx_server_script = self.app_state.run_scripts_dir.joinpath("electrumx.bat")
        else:
            electrumx_server_script = self.app_state.run_scripts_dir.joinpath("electrumx.sh")

        process = self.spawn_in_new_console(electrumx_server_script)

        component = Component(
            pid=process.pid,
            process_name=ComponentName.ELECTRUMX,
            process_type=ComponentType.ELECTRUMX,
            endpoint="http://127.0.0.1:51001",
            component_state=ComponentState.NONE,
            location=str(self.app_state.electrumx_dir),
            metadata={"data_dir": str(self.app_state.electrumx_data_dir)},
            logging_path=None,
        )

        is_running = asyncio.run(self.is_electrumx_running())
        if not is_running:
            component.component_state = ComponentState.Failed
            logger.error("electrumx server failed to start")
        else:
            component.component_state = ComponentState.Running
            logger.debug("electrumx online")
        self.component_store.update_status_file(component)
        self.status_monitor_client.update_status(component)
        return process

    def disable_rest_api_authentication(self):
        path_to_config = self.app_state.electrumsv_regtest_config_path

        config = {}
        if path_to_config.exists():
            with open(path_to_config, "r") as f:
                config = json.load(f)
        config["rpcpassword"] = ""
        config["rpcuser"] = "user"

        with open(path_to_config, "w") as f:
            f.write(json.dumps(config, indent=4))

    def start_and_stop_ESV(self, electrumsv_server_script):
        # Ugly hack (first time run through need to start then stop ESV wallet to make config files)
        logger.debug(
            "starting RegTest electrumsv daemon for the first time - initializing wallet - "
            "standby..."
        )
        process = subprocess.Popen(
            f"{electrumsv_server_script}", creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        time.sleep(7)
        if sys.platform in ("linux", "darwin"):
            subprocess.run(f"pkill -P {process.pid}", shell=True)
        else:
            subprocess.run(f"taskkill.exe /PID {process.pid} /T /F")

    def run_electrumsv_daemon(self, is_first_run=False):
        """Todo - this currently uses ugly hacks with starting and stopping the ESV wallet
         in order to:
        1) generate the config files (so that it can be directly edited) - would be obviated by
        fixing this: https://github.com/electrumsv/electrumsv/issues/111
        2) newly created wallet doesn't seem to be fully useable until after stopping the daemon."""
        if sys.platform == "win32":
            electrumsv_server_script = self.app_state.run_scripts_dir.joinpath("electrumsv.bat")
        else:
            electrumsv_server_script = self.app_state.run_scripts_dir.joinpath("electrumsv.sh")
        try:
            self.disable_rest_api_authentication()
        except FileNotFoundError:  # is_first_run = True
            self.start_and_stop_ESV(electrumsv_server_script)  # generates config json file
            self.disable_rest_api_authentication()  # now this will work
            return self.run_electrumsv_daemon(is_first_run=True)

        logger.debug(f"starting RegTest electrumsv daemon...")
        process = self.spawn_in_new_console(electrumsv_server_script)
        if is_first_run:
            time.sleep(7)
            self.app_state.resetters.reset_electrumsv_wallet()  # create first-time wallet
            time.sleep(1)

            if sys.platform in ("linux", "darwin"):
                subprocess.run(f"pkill -P {process.pid}", shell=True)
            else:
                subprocess.run(f"taskkill.exe /PID {process.pid} /T /F", check=True)
            return self.run_electrumsv_daemon(is_first_run=False)

        component = Component(
            pid=process.pid,
            process_name=ComponentName.ELECTRUMSV,
            process_type=ComponentType.ELECTRUMSV,
            endpoint="http://127.0.0.1:9999",
            component_state=ComponentState.NONE,
            location=str(self.app_state.electrumsv_regtest_dir),
            metadata={"config": str(self.app_state.electrumsv_regtest_config_path)},
            logging_path=str(self.app_state.electrumsv_data_dir.joinpath("logs")),
        )

        is_running = self.is_electrumsv_running()
        if not is_running:
            component.component_state = ComponentState.Failed
            logger.error("electrumsv failed to start")
        else:
            component.component_state = ComponentState.Running
            logger.debug("electrumsv online")

        self.component_store.update_status_file(component)
        self.status_monitor_client.update_status(component)
        return process

    def start_status_monitor(self):
        if sys.platform == "win32":
            status_monitor_script = self.app_state.run_scripts_dir.joinpath("status_monitor.bat")
        else:
            status_monitor_script = self.app_state.run_scripts_dir.joinpath("status_monitor.sh")

        logger.debug(f"starting status monitor daemon...")
        process = self.spawn_in_new_console(status_monitor_script)

        component = Component(
            pid=process.pid,
            process_name=ComponentName.STATUS_MONITOR,
            process_type=ComponentType.STATUS_MONITOR,
            endpoint="http://127.0.0.1:api/status",
            component_state=ComponentState.Running,
            location=str(self.app_state.status_monitor_dir),
            metadata={},
            logging_path=None,
        )

        is_running = self.is_status_monitor_running()
        if not is_running:
            component.component_state = ComponentState.Failed
            logger.error("status_monitor failed to start")
        else:
            component.component_state = ComponentState.Running
            logger.debug("status_monitor online")
        self.component_store.update_status_file(component)
        return process

    def start(self):
        print()
        print()
        print("running stack...")

        open(self.app_state.electrumsv_sdk_data_dir / "spawned_pids", 'w').close()

        procs = []
        status_monitor_process = self.start_status_monitor()
        procs.append(status_monitor_process.pid)
        time.sleep(1)

        if ComponentName.NODE in self.app_state.start_set:
            self.start_node()
            time.sleep(2)

        if ComponentName.ELECTRUMX in self.app_state.start_set:
            electrumx_process = self.run_electrumx_server()
            procs.append(electrumx_process.pid)

        if ComponentName.ELECTRUMSV in self.app_state.start_set:
            esv_process = self.run_electrumsv_daemon()
            procs.append(esv_process.pid)

        self.app_state.save_repo_paths()
