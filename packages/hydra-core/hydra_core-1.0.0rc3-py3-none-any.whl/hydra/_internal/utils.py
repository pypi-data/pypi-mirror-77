# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import copy
import inspect
import logging.config
import os
import sys
import warnings
from dataclasses import dataclass
from os.path import dirname, join, normpath, realpath
from traceback import print_exc, print_exception
from types import FrameType
from typing import (
    Any,
    Callable,
    List,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from omegaconf import DictConfig, OmegaConf, read_write
from omegaconf.errors import OmegaConfBaseException

from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra.core.config_search_path import ConfigSearchPath, SearchPathQuery
from hydra.core.utils import get_valid_filename, split_config_path
from hydra.errors import (
    CompactHydraException,
    InstantiationException,
    SearchPathException,
)
from hydra.types import ObjectConf, TaskFunction

log = logging.getLogger(__name__)


def _get_module_name_override() -> Optional[str]:
    module_envs = ["HYDRA_MAIN_MODULE", "FB_PAR_MAIN_MODULE", "FB_XAR_MAIN_MODULE"]
    for module_env in module_envs:
        if module_env in os.environ:
            return os.environ[module_env]
    return None


def detect_calling_file_or_module_from_task_function(
    task_function: Any,
) -> Tuple[Optional[str], Optional[str], str]:

    mdl = task_function.__module__
    override = _get_module_name_override()
    if override is not None:
        mdl = override

    calling_file: Optional[str]
    calling_module: Optional[str]
    if mdl not in (None, "__main__"):
        calling_file = None
        calling_module = mdl
    else:
        calling_file = task_function.__code__.co_filename
        calling_module = None

    task_name = detect_task_name(calling_file, mdl)

    return calling_file, calling_module, task_name


def detect_calling_file_or_module_from_stack_frame(
    stack_depth: int,
) -> Tuple[Optional[str], Optional[str]]:

    stack = inspect.stack()
    frame = stack[stack_depth]
    if is_notebook() and "_dh" in frame[0].f_globals:
        pynb_dir = frame[0].f_globals["_dh"][0]
        calling_file = join(pynb_dir, "notebook.ipynb")
        return calling_file, None

    calling_file = frame.filename
    calling_module = None
    try:
        calling_module = _get_module_name_override()
        if calling_module is None:
            calling_module = frame[0].f_globals[frame[3]].__module__
    except KeyError:
        try:
            calling_module = frame[0].f_locals["self"].__module__
        except KeyError:
            pass

    return calling_file, calling_module


def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__  # type: ignore
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False


def detect_task_name(calling_file: Optional[str], calling_module: Optional[str]) -> str:

    if calling_file is not None:
        target_file = os.path.basename(calling_file)
        task_name = get_valid_filename(os.path.splitext(target_file)[0])
    elif calling_module is not None:
        last_dot = calling_module.rfind(".")
        if last_dot != -1:
            task_name = calling_module[last_dot + 1 :]
        else:
            task_name = calling_module
    else:
        raise ValueError()

    return task_name


def compute_search_path_dir(
    calling_file: Optional[str],
    calling_module: Optional[str],
    config_path: Optional[str],
) -> str:
    if calling_file is not None:
        abs_base_dir = realpath(dirname(calling_file))

        if config_path is not None:
            search_path_dir = join(abs_base_dir, config_path)
        else:
            search_path_dir = abs_base_dir
        search_path_dir = normpath(search_path_dir)
    elif calling_module is not None:
        last_dot = calling_module.rfind(".")
        if last_dot != -1:
            calling_module = calling_module[0:last_dot]
        else:
            calling_module = ""

        if config_path is not None:
            config_path = config_path.replace(os.path.sep, "/")
            while str.startswith(config_path, "../"):
                config_path = config_path[len("../") :]
                last_dot = calling_module.rfind(".")
                if last_dot != -1:
                    calling_module = calling_module[0:last_dot]
                else:
                    calling_module = ""

        search_path_dir = "pkg://" + calling_module

        if config_path is not None:
            if calling_module != "":
                search_path_dir = search_path_dir + "/" + config_path
            else:
                search_path_dir = search_path_dir + config_path
    else:
        raise ValueError()

    return search_path_dir


def create_automatic_config_search_path(
    calling_file: Optional[str],
    calling_module: Optional[str],
    config_path: Optional[str],
) -> ConfigSearchPath:
    search_path_dir = compute_search_path_dir(calling_file, calling_module, config_path)
    return create_config_search_path(search_path_dir)


def create_config_search_path(search_path_dir: Optional[str]) -> ConfigSearchPath:
    from hydra.core.plugins import Plugins
    from hydra.plugins.search_path_plugin import SearchPathPlugin

    search_path = ConfigSearchPathImpl()
    search_path.append("hydra", "pkg://hydra.conf")

    if search_path_dir is not None:
        search_path.append("main", search_path_dir)

    search_path_plugins = Plugins.instance().discover(SearchPathPlugin)
    for spp in search_path_plugins:
        plugin = spp()
        assert isinstance(plugin, SearchPathPlugin)
        plugin.manipulate_search_path(search_path)

    search_path.append("schema", "structured://")

    return search_path


def run_and_report(func: Any) -> Any:
    try:
        return func()
    except Exception as ex:
        if "HYDRA_FULL_ERROR" in os.environ and os.environ["HYDRA_FULL_ERROR"] == "1":
            print_exc()
        else:
            if isinstance(ex, CompactHydraException):
                sys.stderr.write(str(ex) + os.linesep)
                if isinstance(ex.__cause__, OmegaConfBaseException):
                    sys.stderr.write(str(ex.__cause__) + os.linesep)
            else:
                # Custom printing that strips the Hydra related stack frames from the top
                # And any omegaconf frames from the bottom.
                # It is possible to add additional libraries to sanitize from the bottom later,
                # maybe even make it configurable.
                tb: Any = ex.__traceback__
                search_max = 10
                # strip Hydra frames from start of stack
                # will strip until it hits run_job()
                while search_max > 0:
                    if tb is None:
                        break
                    frame = tb.tb_frame
                    tb = tb.tb_next
                    search_max = search_max - 1
                    if inspect.getframeinfo(frame).function == "run_job":
                        break

                if search_max == 0 or tb is None:
                    # could not detect run_job, probably a runtime exception before we got there.
                    # do not sanitize the stack trace.
                    print_exc()
                    sys.exit(1)

                # strip OmegaConf frames from bottom of stack
                end = tb
                num_frames = 0
                while end is not None:
                    frame = end.tb_frame
                    mdl = inspect.getmodule(frame)
                    assert mdl is not None
                    name = mdl.__name__
                    if name.startswith("omegaconf."):
                        break
                    end = end.tb_next
                    num_frames = num_frames + 1

                @dataclass
                class FakeTracebackType:
                    tb_next: Any = None  # Optional[FakeTracebackType]
                    tb_frame: Optional[FrameType] = None
                    tb_lasti: Optional[int] = None
                    tb_lineno: Optional[int] = None

                iter_tb = tb
                final_tb = FakeTracebackType()
                cur = final_tb
                added = 0
                while True:
                    cur.tb_lasti = iter_tb.tb_lasti
                    cur.tb_lineno = iter_tb.tb_lineno
                    cur.tb_frame = iter_tb.tb_frame

                    if added == num_frames - 1:
                        break
                    added = added + 1
                    cur.tb_next = FakeTracebackType()
                    cur = cur.tb_next
                    iter_tb = iter_tb.tb_next

                print_exception(etype=None, value=ex, tb=final_tb)  # type: ignore
            sys.stderr.write(
                "\nSet the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.\n"
            )
        sys.exit(1)


def _run_hydra(
    args_parser: argparse.ArgumentParser,
    task_function: TaskFunction,
    config_path: Optional[str],
    config_name: Optional[str],
    strict: Optional[bool],
) -> None:

    from hydra.core.global_hydra import GlobalHydra

    from .hydra import Hydra

    args = args_parser.parse_args()
    if args.config_name is not None:
        config_name = args.config_name

    if args.config_path is not None:
        config_path = args.config_path

    (
        calling_file,
        calling_module,
        task_name,
    ) = detect_calling_file_or_module_from_task_function(task_function)

    config_dir, config_name = split_config_path(config_path, config_name)

    search_path = create_automatic_config_search_path(
        calling_file, calling_module, config_dir
    )

    def add_conf_dir() -> None:
        if args.config_dir is not None:
            abs_config_dir = os.path.abspath(args.config_dir)
            if not os.path.isdir(abs_config_dir):
                raise SearchPathException(
                    f"Additional config directory '{abs_config_dir}' not found"
                )
            search_path.prepend(
                provider="command-line",
                path=f"file://{abs_config_dir}",
                anchor=SearchPathQuery(provider="schema"),
            )

    run_and_report(add_conf_dir)
    hydra = run_and_report(
        lambda: Hydra.create_main_hydra2(
            task_name=task_name, config_search_path=search_path, strict=strict
        )
    )

    try:
        if args.help:
            hydra.app_help(config_name=config_name, args_parser=args_parser, args=args)
            sys.exit(0)
        if args.hydra_help:
            hydra.hydra_help(
                config_name=config_name, args_parser=args_parser, args=args
            )
            sys.exit(0)

        has_show_cfg = args.cfg is not None
        num_commands = (
            args.run + has_show_cfg + args.multirun + args.shell_completion + args.info
        )
        if num_commands > 1:
            raise ValueError(
                "Only one of --run, --multirun,  -cfg, --info and --shell_completion can be specified"
            )
        if num_commands == 0:
            args.run = True
        if args.run:
            run_and_report(
                lambda: hydra.run(
                    config_name=config_name,
                    task_function=task_function,
                    overrides=args.overrides,
                )
            )
        elif args.multirun:
            run_and_report(
                lambda: hydra.multirun(
                    config_name=config_name,
                    task_function=task_function,
                    overrides=args.overrides,
                )
            )
        elif args.cfg:
            run_and_report(
                lambda: hydra.show_cfg(
                    config_name=config_name,
                    overrides=args.overrides,
                    cfg_type=args.cfg,
                    package=args.package,
                )
            )
        elif args.shell_completion:
            run_and_report(
                lambda: hydra.shell_completion(
                    config_name=config_name, overrides=args.overrides
                )
            )
        elif args.info:
            hydra.show_info(config_name=config_name, overrides=args.overrides)
        else:
            sys.stderr.write("Command not specified\n")
            sys.exit(1)
    finally:
        GlobalHydra.instance().clear()


def _get_exec_command() -> str:
    if sys.argv[0].endswith(".py"):
        return f"python {sys.argv[0]}"
    else:
        # Running as an installed app (setuptools entry point)
        executable = os.path.basename(sys.argv[0])
        return executable


def _get_completion_help() -> str:
    from hydra.core.plugins import Plugins
    from hydra.plugins.completion_plugin import CompletionPlugin

    completion_plugins = Plugins.instance().discover(CompletionPlugin)
    completion_info: List[str] = []
    for plugin_cls in completion_plugins:
        assert issubclass(plugin_cls, CompletionPlugin)
        for cmd in ["install", "uninstall"]:
            head = f"{plugin_cls.provides().capitalize()} - {cmd.capitalize()}:"
            completion_info.append(head)
            completion_info.append(plugin_cls.help(cmd).format(_get_exec_command()))
        completion_info.append("")
    completion_help = "\n".join([f"    {x}" if x else x for x in completion_info])
    return completion_help


def get_args_parser() -> argparse.ArgumentParser:
    from .. import __version__

    parser = argparse.ArgumentParser(add_help=False, description="Hydra")
    parser.add_argument("--help", "-h", action="store_true", help="Application's help")
    parser.add_argument("--hydra-help", action="store_true", help="Hydra's help")
    parser.add_argument(
        "--version",
        action="version",
        help="Show Hydra's version and exit",
        version=f"Hydra {__version__}",
    )
    parser.add_argument(
        "overrides",
        nargs="*",
        help="Any key=value arguments to override config values (use dots for.nested=overrides)",
    )

    parser.add_argument(
        "--cfg",
        "-c",
        choices=["job", "hydra", "all"],
        help="Show config instead of running [job|hydra|all]",
    )

    parser.add_argument(
        "--package", "-p", help="Config package to show",
    )

    parser.add_argument("--run", "-r", action="store_true", help="Run a job")

    parser.add_argument(
        "--multirun",
        "-m",
        action="store_true",
        help="Run multiple jobs with the configured launcher and sweeper",
    )

    parser.add_argument(
        "--shell-completion",
        "-sc",
        action="store_true",
        help=f"Install or Uninstall shell completion:\n{_get_completion_help()}",
    )

    parser.add_argument(
        "--config-path",
        "-cp",
        help="""Overrides the config_path specified in hydra.main().
                    The config_path is relative to the Python file declaring @hydra.main()""",
    )

    parser.add_argument(
        "--config-name",
        "-cn",
        help="Overrides the config_name specified in hydra.main()",
    )

    parser.add_argument(
        "--config-dir",
        "-cd",
        help="Adds an additional config dir to the config search path",
    )

    parser.add_argument(
        "--info", "-i", action="store_true", help="Print Hydra information",
    )
    return parser


def get_args(args: Optional[Sequence[str]] = None) -> Any:
    return get_args_parser().parse_args(args=args)


def get_column_widths(matrix: List[List[str]]) -> List[int]:
    num_cols = 0
    for row in matrix:
        num_cols = max(num_cols, len(row))
    widths: List[int] = [0] * num_cols
    for row in matrix:
        for idx, col in enumerate(row):
            widths[idx] = max(widths[idx], len(col))

    return widths


def _instantiate_class(
    clazz: Type[Any], config: Union[ObjectConf, DictConfig], *args: Any, **kwargs: Any
) -> Any:
    # TODO: pull out to caller?
    final_kwargs = _get_kwargs(config, **kwargs)
    return clazz(*args, **final_kwargs)


def _call_callable(
    fn: Callable[..., Any],
    config: Union[ObjectConf, DictConfig],
    *args: Any,
    **kwargs: Any,
) -> Any:
    final_kwargs = _get_kwargs(config, **kwargs)
    return fn(*args, **final_kwargs)


def _locate(path: str) -> Union[type, Callable[..., Any]]:
    """
    Locate an object by name or dotted path, importing as necessary.
    This is similar to the pydoc function `locate`, except that it checks for
    the module from the given path from back to front.
    """
    if path == "":
        raise ImportError("Empty path")
    import builtins
    from importlib import import_module

    parts = [part for part in path.split(".") if part]
    module = None
    for n in reversed(range(len(parts))):
        try:
            mod = ".".join(parts[:n])
            module = import_module(mod)
        except Exception as e:
            if n == 0:
                raise ImportError(f"Error loading module '{path}'") from e
            continue
        if module:
            break
    if module:
        obj = module
    else:
        obj = builtins
    for part in parts[n:]:
        mod = mod + "." + part
        if not hasattr(obj, part):
            try:
                import_module(mod)
            except Exception as e:
                raise ImportError(
                    f"Encountered error: `{e}` when loading module '{path}'"
                ) from e
        obj = getattr(obj, part)
    if isinstance(obj, type):
        obj_type: type = obj
        return obj_type
    elif callable(obj):
        obj_callable: Callable[..., Any] = obj
        return obj_callable
    else:
        # dummy case
        raise ValueError(f"Invalid type ({type(obj)}) found for {path}")


def _get_kwargs(config: Union[ObjectConf, DictConfig], **kwargs: Any) -> Any:

    if isinstance(config, ObjectConf):
        config = OmegaConf.structured(config)
        if config.params is not None:
            params = config.params
        else:
            params = OmegaConf.create()
    else:
        config = copy.deepcopy(config)
        if "params" in config:
            msg = (
                "\nField 'params' is deprecated since Hydra 1.0 and will be removed in Hydra 1.1."
                "\nInline the content of params directly at the containing node."
                "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/object_instantiation_changes"
            )
            warnings.warn(category=UserWarning, message=msg)
            params = config.params
        else:
            params = OmegaConf.create()
            for k, v in config.items():
                if k != "_target_":
                    params[k] = v

    assert isinstance(
        params, MutableMapping
    ), f"Input config params are expected to be a mapping, found {type(config.params).__name__}"

    if isinstance(config, DictConfig):
        assert isinstance(params, DictConfig)
        params._set_parent(config)

    config_overrides = {}
    passthrough = {}
    for k, v in kwargs.items():
        if k in params:
            config_overrides[k] = v
        else:
            passthrough[k] = v
    final_kwargs = {}

    with read_write(params):
        params.merge_with(config_overrides)

    for k, v in params.items():
        final_kwargs[k] = v

    for k, v in passthrough.items():
        final_kwargs[k] = v
    return final_kwargs


def _get_cls_name(config: DictConfig, pop: bool = True) -> str:
    def _getcls(field: str) -> str:
        if pop:
            classname = config.pop(field)
        else:
            classname = config[field]
        if not isinstance(classname, str):
            raise InstantiationException(f"_target_ field '{field}' must be a string")
        return classname

    for field in ["target", "cls", "class"]:
        if field in config:
            key = config._get_full_key(field)
            msg = (
                f"\nConfig key '{key}' is deprecated since Hydra 1.0 and will be removed in Hydra 1.1."
                f"\nUse '_target_' instead of '{field}'."
                f"\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/object_instantiation_changes"
            )
            warnings.warn(message=msg, category=UserWarning)

    if "_target_" in config:
        return _getcls("_target_")

    for field in ["target", "cls", "class"]:
        if field in config:
            return _getcls(field)

    raise InstantiationException("Input config does not have a `_target_` field")
