import asyncio
import inspect
import logging
import traceback
import sys
from typing import Any, Dict

from opentrons.drivers.smoothie_drivers.driver_3_0 import SmoothieAlarm

from .contexts import ProtocolContext
from .json_dispatchers import pipette_command_map, \
    temperature_module_command_map, magnetic_module_command_map, \
    thermocycler_module_command_map
from . import execute_v3, execute_v4

from opentrons.protocols.types import (PythonProtocol, Protocol,
                                       APIVersion, MalformedProtocolError)
from opentrons.hardware_control import ExecutionCancelledError

MODULE_LOG = logging.getLogger(__name__)


class ExceptionInProtocolError(Exception):
    """ This exception wraps an exception that was raised from a protocol
    for proper error message formatting by the rpc, since it's only here that
    we can properly figure out formatting
    """

    def __init__(self, original_exc, original_tb, message, line):
        self.original_exc = original_exc
        self.original_tb = original_tb
        self.message = message
        self.line = line
        super().__init__(original_exc, original_tb, message, line)

    def __str__(self):
        return '{}{}: {}'.format(
            self.original_exc.__class__.__name__,
            ' [line {}]'.format(self.line) if self.line else '',
            self.message)


def _runfunc_ok(run_func: Any):
    if not callable(run_func):
        raise SyntaxError("No function 'run(ctx)' defined")
    sig = inspect.Signature.from_callable(run_func)
    if not sig.parameters:
        raise SyntaxError("Function 'run()' does not take any parameters")
    if len(sig.parameters) > 1:
        for name, param in list(sig.parameters.items())[1:]:
            if param.default == inspect.Parameter.empty:
                raise SyntaxError(
                    "Function 'run{}' must be called with more than one "
                    "argument but would be called as 'run(ctx)'"
                    .format(str(sig)))


def _find_protocol_error(tb, proto_name):
    """Return the FrameInfo for the lowest frame in the traceback from the
    protocol.
    """
    tb_info = traceback.extract_tb(tb)
    for frame in reversed(tb_info):
        if frame.filename == proto_name:
            return frame
    else:
        raise KeyError


def _run_python(
        proto: PythonProtocol, context: ProtocolContext):
    new_globs: Dict[Any, Any] = {}
    exec(proto.contents, new_globs)
    # If the protocol is written correctly, it will have defined a function
    # like run(context: ProtocolContext). If so, that function is now in the
    # current scope.
    if proto.filename and proto.filename.endswith('zip'):
        filename = 'protocol.ot2.py'
    else:
        filename = proto.filename or '<protocol>'
    try:
        _runfunc_ok(new_globs.get('run'))
    except SyntaxError as se:
        raise MalformedProtocolError(str(se))

    new_globs['__context'] = context
    try:
        exec('run(__context)', new_globs)
    except (SmoothieAlarm, asyncio.CancelledError, ExecutionCancelledError):
        # this is a protocol cancel and shouldn't have special logging
        raise
    except Exception as e:
        exc_type, exc_value, tb = sys.exc_info()
        try:
            frame = _find_protocol_error(tb, filename)
        except KeyError:
            # No pretty names, just raise it
            raise e
        raise ExceptionInProtocolError(e, tb, str(e), frame.lineno)


def run_protocol(protocol: Protocol,
                 context: ProtocolContext):
    """ Run a protocol.

    :param protocol: The :py:class:`.protocols.types.Protocol` to execute
    :param context: The context to use.
    """
    if isinstance(protocol, PythonProtocol):
        if protocol.api_level >= APIVersion(2, 0):
            _run_python(protocol, context)
        else:
            raise RuntimeError(
                f'Unsupported python API version: {protocol.api_level}'
            )
    else:
        if protocol.contents['schemaVersion'] == 3:
            ins = execute_v3.load_pipettes_from_json(
                context, protocol.contents)
            lw = execute_v3.load_labware_from_json_defs(
                context, protocol.contents)
            execute_v3.dispatch_json(context, protocol.contents, ins, lw)
        elif protocol.contents['schemaVersion'] in [4, 5]:
            # reuse the v3 fns for loading labware and pipettes
            # b/c the v4 protocol has no changes for these keys
            ins = execute_v3.load_pipettes_from_json(
                context, protocol.contents)

            modules = execute_v4.load_modules_from_json(
                context, protocol.contents)

            lw = execute_v4.load_labware_from_json_defs(
                context, protocol.contents, modules)
            execute_v4.dispatch_json(
                context, protocol.contents, ins, lw, modules,
                pipette_command_map, magnetic_module_command_map,
                temperature_module_command_map,
                thermocycler_module_command_map)
        else:
            raise RuntimeError(
                f'Unsupported JSON protocol schema: {protocol.schema_version}')
