import os

import click
import requirements

from spell.api.models import RunRequest
from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
    SPELL_INVALID_CONFIG,
)
from spell.cli.commands.logs import logs
from spell.cli.log import logger
from spell.cli.utils import (
    git_utils,
    parse_utils,
    with_emoji,
    ellipses,
    command,
)
from spell.cli.utils.parse_utils import parse_conditions, validate_attached_resources
from spell.cli.utils.command_options import (
    dependency_params,
    workspace_spec_params,
    machine_config_params,
    cli_params,
    description_param,
    label_param,
    background_option,
    idempotent_option,
    tensorboard_params,
    stop_condition_option,
)
from spell.cli.utils.exceptions import ParseException


@command(name="run", short_help="Execute a new run")
@click.argument("command")
@click.argument("args", nargs=-1)
@idempotent_option
@machine_config_params
@dependency_params()
@workspace_spec_params
@tensorboard_params
@description_param
@label_param
@cli_params
@background_option
@click.option(
    "--distributed",
    type=int,
    metavar="N",
    help="Execute a distributed run using N machines of the specified machine type.",
)
@click.option(
    "--auto-resume/--disable-auto-resume",
    default=None,
    help="Enable or disable auto-resume. NOTE: This is only supported for spot instance machine types",
)
@stop_condition_option
@click.pass_context
def run(
    ctx,
    command,
    args,
    machine_type,
    pip_packages,
    requirements_file,
    apt_packages,
    stop_condition,
    docker_image,
    framework,
    commit_ref,
    description,
    labels,
    envvars,
    raw_resources,
    background,
    conda_file,
    force,
    verbose,
    idempotent,
    provider,
    tensorboard_dir,
    distributed,
    auto_resume,
    run_type="user",
    **kwargs
):
    """
    Execute COMMAND remotely on Spell's infrastructure

    The run command is used to create runs and is likely the command you'll use most
    while using Spell. It is intended to be emulate local development. Any code,
    software, binaries, etc., that you can run locally on your computer can be run
    on Spell - you simply put `spell run` in front of the same commands you would use
    locally and they will run remotely. The various options can be used to customize
    the environment in which COMMAND will run.
    """
    logger.info("starting run command")
    try:
        stop_conditions = parse_conditions(stop_condition)
    except ParseException as e:
        raise ExitException(e.message)

    run_req = create_run_request(
        ctx,
        command,
        args,
        machine_type,
        pip_packages,
        requirements_file,
        apt_packages,
        docker_image,
        framework,
        commit_ref,
        description,
        envvars,
        raw_resources,
        conda_file,
        force,
        verbose,
        idempotent,
        provider,
        run_type,
        labels=labels,
        tensorboard_dir=tensorboard_dir,
        distributed=distributed,
        stop_conditions=stop_conditions,
        auto_resume=auto_resume,
        **kwargs
    )

    # execute the run
    client = ctx.obj["client"]
    logger.info("sending run request to api")
    with api_client_exception_handler():
        run = client.run(run_req)

    utf8 = ctx.obj["utf8"]
    if run.already_existed:
        click.echo(
            with_emoji(u"♻️", "Idempotent: Found existing run {}".format(run.id), utf8)
            + ellipses(utf8)
        )
    else:
        click.echo(with_emoji(u"💫", "Casting spell #{}".format(run.id), utf8) + ellipses(utf8))
    if background:
        click.echo("View logs with `spell logs {}`".format(run.id))
    else:
        click.echo(with_emoji(u"✨", "Stop viewing logs with ^C", utf8))
        ctx.invoke(logs, run_id=str(run.id), follow=True, verbose=verbose, run_warning=True)


def create_run_request(
    ctx,
    command,
    args,
    machine_type,
    pip_packages,
    requirements_file,
    apt_packages,
    docker_image,
    framework,
    commit_ref,
    description,
    envvars,
    raw_resources,
    conda_file,
    force,
    verbose,
    idempotent,
    provider,
    run_type,
    github_url,
    github_ref,
    labels=None,
    distributed=None,
    tensorboard_dir=None,
    stop_conditions=None,
    auto_resume=None,
    **kwargs
):

    if command is None:
        cmd_with_args = None
    else:
        cmd_with_args = " ".join((command,) + args)

    repo = git_utils.detect_repo(
        ctx,
        github_url=github_url,
        github_ref=github_ref,
        force=force,
        description=description,
        commit_ref=commit_ref,
    )

    source_spec = sum(1 for x in (framework, docker_image, conda_file) if x is not None)
    if source_spec > 1:
        raise ExitException(
            "Only one of the following options can be specified: --framework, --from, --conda-file",
            SPELL_INVALID_CONFIG,
        )

    if docker_image is not None and (pip_packages or apt_packages or requirements_file):
        raise ExitException(
            "--apt, --pip, or --pip-req cannot be specified when --from is provided."
            " Please install packages from the specified Dockerfile.",
            SPELL_INVALID_CONFIG,
        )

    if conda_file is not None and (pip_packages or requirements_file):
        raise ExitException(
            "--pip or --pip-req cannot be specified when using a conda environment. "
            "You can include the pip installs in the conda environment file instead."
        )
    # Read the conda file
    conda_file_contents = None
    if conda_file is not None:
        with open(conda_file) as conda_f:
            conda_file_contents = conda_f.read()

    if requirements_file:
        if not os.path.isfile(requirements_file):
            raise ExitException("--pip-req file not found: " + requirements_file)
        pip_packages = list(pip_packages)
        with open(requirements_file, "r") as rf:
            try:
                reqs = list(requirements.parse(rf))
            except Exception:
                raise ExitException(
                    "Pip requirements file could not be parsed", SPELL_INVALID_CONFIG
                )
            for req in reqs:
                pip_packages.append(req.line)

    # extract envvars into a dictionary
    curr_envvars = parse_utils.parse_env_vars(envvars)

    # extract attached resources
    attached_resources = validate_attached_resources(raw_resources)

    # TensorBoard checks
    if tensorboard_dir in attached_resources.values():
        raise ExitException("cannot mount into TensorBoard directory")

    return RunRequest(
        machine_type=machine_type,
        command=cmd_with_args,
        workspace_id=repo.workspace_id,
        workspace_remote_url=repo.workspace_remote_url,
        commit_hash=repo.commit_hash if not repo.has_github() else None,
        uncommitted_hash=repo.uncommitted_hash,
        cwd=repo.relative_path,
        root_directory=repo.root_directory,
        pip_packages=pip_packages,
        apt_packages=apt_packages,
        docker_image=docker_image,
        framework=framework,
        tensorboard_directory=tensorboard_dir,
        description=description,
        labels=labels,
        envvars=curr_envvars,
        attached_resources=attached_resources,
        conda_file=conda_file_contents,
        run_type=run_type,
        idempotent=idempotent,
        provider=provider,
        local_root=repo.local_root,
        github_url=repo.github_url,
        github_ref=repo.commit_hash if repo.has_github() else None,
        distributed=distributed,
        stop_conditions=stop_conditions,
        auto_resume=auto_resume,
    )
