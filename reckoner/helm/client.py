from provider import HelmProvider
from command import HelmCommand
from reckoner.command_line_caller import Response
import re


class HelmClient(object):
    version_regex = re.compile(r'[a-zA-Z]+: v([0-9\.]+)(\+g[0-9a-f]+)?')
    repo_header_regex = re.compile(r'^NAME\s+URL$')

    def __init__(self, default_helm_arguments=[], provider=HelmProvider):
        self._default_helm_arguments = default_helm_arguments
        self._provider = provider

    @property
    def default_helm_arguments(self):
        """The default helm arguments for all commands run through the client."""
        return self._default_helm_arguments

    @default_helm_arguments.setter
    def default_helm_arguments(self, value):
        """Setter of the default helm arguments to override"""
        self._default_helm_arguments = value

    def execute(self, command, arguments=[]):
        """
        Run the command with the help of the provider.

        return HelmCmdResponse
        """

        arguments = self.default_helm_arguments + arguments
        command = HelmCommand(
            command=command,
            arguments=arguments,
        )
        response = self._provider.execute(command)
        if response.succeeded:
            return response
        else:
            raise HelmClientException('Command Failed with output below:\nSTDOUT: {}\nSTDERR: {}\nCOMMAND: {}'.format(
                response.stdout, response.stderr, response.command))

    @property
    def client_version(self):
        return self._get_version('--client')

    @property
    def server_version(self):
        return self._get_version('--server')

    @property
    def repositories(self):
        repo_names = []
        raw_repositories = self.execute('repo', ['list']).stdout
        for line in raw_repositories.splitlines():
            # Try to filter out the header line as a viable repo name
            if HelmClient.repo_header_regex.match(line):
                continue
            # If the line is blank
            if not line:
                continue

            repo_names.append(line.split()[0])

        return repo_names

    def check_helm_command(self):
        return self.execute("help").succeeded

    def upgrade(self, args, install=True):
        if install:
            arguments = ['--install'] + args
        else:
            arguments = args
        return self.execute("upgrade", arguments)

    def rollback(self, release):
        raise NotImplementedError('TODO SHIT DO NOT SHIP IT')

    def dependency_update(self, chart_path):
        raise NotImplementedError('Sorry this feature has not yet been implemented.')

    def repo_update(self):
        """Function to update all the repositories"""
        return self.execute('repo', ['update'])

    def repo_add(self, name, url):
        """Function add repositories to helm via command line"""
        return self.execute('repo', ['add', name, url])

    def _get_version(self, kind='--server'):
        get_ver = self.execute("version", arguments=['--short', kind])
        ver = self._find_version(get_ver.stdout)

        if ver == None:
            raise HelmClientException(
                """Could not find version!! Could the helm response format have changed?
                STDOUT: {}
                STDERR: {}
                COMMAND: {}""".format(get_ver.stdout, get_ver.stderr, get_ver.command)
            )

        return ver

    @staticmethod
    def _find_version(raw_version):
        ver = HelmClient.version_regex.search(raw_version)
        if ver:
            return ver.group(1)
        else:
            return None


class HelmClientException(Exception):
    pass
