#!/usr/bin/env python3
# The {} placeholders in the docstring are to be replaced with URL_HELP
# and URL_GITLAB_ISSUES whenever the docstring is used.
"""Secure Encryption and Transfer Tool
For detailed documentation see: {}
To report an issue, please use: {}
"""

import os
import json
import logging
from functools import wraps
from getpass import getpass
from pathlib import Path
from typing import List, Dict, Any, Optional

from .progress import CliProgress
from .. import VERSION_WITH_DEPS
from ..utils.config import Config, load_config, config_to_dict
from .cli_builder import rename, return_to_stdout, partial, lazy_partial, \
    Subcommands, Subcommand, SubcommandGroup, decorate, block, set_default
from ..utils.log import exception_to_message, add_stream_handler_to_logger, \
    add_rotating_file_handler_to_logger, create_logger
from ..workflows.config import create as create_config
from ..workflows.transfer import transfer as workflows_transfer
from ..workflows.decrypt import decrypt as workflows_decrypt
from ..workflows.encrypt import encrypt as workflows_encrypt
from ..workflows.request_sigs import request_sigs
from ..workflows.upload_keys import upload_keys
from ..protocols import parse_protocol, __all__ as available_protocols
from ..core.versioncheck import check_version
from ..core.error import UserError
from .. import URL_READTHEDOCS, URL_GITLAB_ISSUES

logger = create_logger(__name__)


def parse_dict(s):
    return json.loads(s)

def parse_protocol_args(s):
    args = parse_dict(s)
    not_provided = object()
    pw = args.get("pkey_password", not_provided)
    if pw is None: # pw is provided and is None
        args["pkey_password"] = getpass(
            "Please enter your ssh private key password:")
    return args

def two_factor_cli_prompt():
    return input("Verification code: ")


@exception_to_message(FileNotFoundError, logger)
def get_passphrase_from_file_or_prompt(passphrase_file: Optional[str]) -> str:
    if passphrase_file:
        return Path(passphrase_file).read_text().strip()
    return getpass("Please enter your gpg private key password:")


@wraps(workflows_encrypt)
def encrypt(*args, config: Config, dry_run: bool, passphrase_file: Optional[str],
            **kwargs):
    if dry_run:
        kwargs["passphrase"] = None
    elif config.sign_encrypted_data:
        kwargs["passphrase"] = get_passphrase_from_file_or_prompt(passphrase_file)
    else:
        kwargs["passphrase"] = None
    return workflows_encrypt(*args, config=config, dry_run=dry_run, **kwargs)


@wraps(workflows_decrypt)
def decrypt(*args, dry_run: bool, passphrase_file: Optional[str], **kwargs):
    if dry_run:
        kwargs["passphrase"] = None
    else:
        kwargs["passphrase"] = get_passphrase_from_file_or_prompt(passphrase_file)
    return workflows_decrypt(*args, dry_run=dry_run, **kwargs)


@exception_to_message((UserError, FileNotFoundError), logger)
def transfer(files: List[str],
             *,
             connection: str = None,
             two_factor_callback,
             config: Config,
             protocol=None,
             protocol_args: Dict[str, Any] = None,
             dry_run: bool = False,
             progress=None):
    if connection is not None:
        if protocol is not None:
            raise UserError("Arguments 'protocol' and 'connection' "
                            "cannot be given together")
        connection = config.connections[connection]
        protocol = parse_protocol(connection.protocol)
        if protocol_args is None:
            protocol_args = {}
        protocol_args = {**connection.parameters, **protocol_args}
    if protocol is None or protocol_args is None:
        raise UserError("Either 'protocol' together with 'protocol_args' "
                        "or 'connection' "
                        "has to be given as an argument")
    return workflows_transfer(files, protocol=protocol,
                              protocol_args=protocol_args,
                              config=config,
                              two_factor_callback=two_factor_callback,
                              dry_run=dry_run,
                              progress=progress)


def load_config_check():
    cfg = load_config()
    if not cfg.offline and cfg.check_version:
        exception_to_message(logger=logger)(check_version)(cfg.repo_url)
    return cfg


class Cli(Subcommands):
    description = __doc__.format(URL_READTHEDOCS, URL_GITLAB_ISSUES)
    version = VERSION_WITH_DEPS
    config = load_config_check()
    passphrase_override = dict(help="Instead of asking for passphrase, "
                                    "read it from a file",
                               name="passphrase-file",
                               dest="passphrase_file")
    logger = logging.getLogger()
    add_rotating_file_handler_to_logger(logger,
                                        log_dir=config.log_dir,
                                        file_max_number=config.log_max_file_number)
    add_stream_handler_to_logger(logger)
    subcommands = (
        Subcommand(
            decorate(encrypt,
                     set_default(offline=config.offline),
                     partial(config=config),
                     lazy_partial(progress=CliProgress)
                     ),
            overrides={
                "files": dict(help="Input file(s) or directories"),
                "sender": dict(help="fingerprint, key ID or email associated "
                                    "with GPG key of data sender.",
                               alias='-s'),
                "recipient": dict(help="fingerprint, key ID or email associated "
                                  "with GPG key of data recipient(s).",
                                  alias='-r'),
                "transfer_id": dict(help="Transfer id (optional)", alias='-t'),
                "offline": dict(
                    help="Offline mode: skip transfer_id validation and key "
                         "refreshing."),
                "purpose": dict(
                    help="Purpose of the transfer (PRODUCTION, TEST), "
                         "default: PRODUCTION"),
                "output_name": dict(
                    help="output encrypted file name. If no path is specified, "
                         "the output tarball is saved in the current working "
                         "directory. If this argument is "
                         "missing the output name is set to a string based on "
                         "the current date and time the function.",
                    default=None,
                    alias='-o'),
                "dry_run": dict(
                    help="Use this flag to perform checks on the data only."),
                "compress": dict(
                    help="Compress the inner tarball"),
                "passphrase": passphrase_override
            }),
        Subcommand(
            decorate(transfer,
                     partial(config=config,
                             two_factor_callback=two_factor_cli_prompt),
                     lazy_partial(progress=CliProgress)
                     ),
            overrides={
                "files": dict(help="Input file(s) or directories"),
                "protocol": dict(help="The protocol for the file transfer."
                                 "Currently available: {}".format(
                                     ", ".join(available_protocols)),
                                 type=parse_protocol,
                                 alias="-p"),
                "protocol_args": dict(help="Protocol specific arguments. "
                                      "Must be passed as a json string",
                                      type=parse_protocol_args),
                "connection": dict(help="Instead of the option 'protocol', load a "
                                   "connection named by the argument of this option "
                                   "to use the protocol and protocol args from the "
                                   "config. The protocol args can be overwritten by "
                                   "the protocol_args option"),
                "dry_run": dict(help="Use this flag to perform checks on the data only")
            }),
        Subcommand(
            decorate(
                decrypt,
                partial(config=config),
                lazy_partial(progress=CliProgress)
            ),
            overrides={
                "output_dir": dict(help="Output directory", default=os.getcwd(), alias="-o"),
                "decrypt_only": dict(help="Skip extraction"),
                "dry_run": dict(help="Use this flag to perform checks on the data only"),
                "passphrase": passphrase_override
            }
        ),
        SubcommandGroup("config",
                        decorate(config_to_dict,
                                 rename("show"),
                                 return_to_stdout,
                                 partial(config=config)),
                        create_config,
                        help="Commands related to config file"
                        ),
        Subcommand(
            decorate(
                request_sigs,
                partial(
                    portal_pgpkey_endpoint_url=config.dcc_portal_pgpkey_endpoint_url,
                    gpg_store=config.gpg_store)
            ),
            overrides={
                "key_ids": dict(help="Key ids to request signatures for")
            }
        ),
        Subcommand(
            decorate(
                upload_keys,
                partial(
                    keyserver=config.keyserver_url,
                    gpg_store=config.gpg_store)
            ),
            overrides={
                "key_ids": dict(help="Key ids to upload")
            }
        )
    )


def run():
    if Cli():
        return 0
    return 1


if __name__ == '__main__':
    run()
