# Testing

# Interactions and modeling

## Helm Provider
call() returns HelmResponse
## Helm Client
HelmClient: Builder model (version(),upgrade(),upgrade_install())
command(str,args)
execute(): call to provider - returns HelmResponse
addArg()
defaultArgs()
arguments
provider()
addRepository()
HelmResponse
status()
output() stderr,stdout,full
## Course
Course(yml_file, args)
charts
_helm_global_args
_kubectl_context
_update_kubectl_context()
_checkYaml() schema validate the yaml
_loadYaml()
_loadEnvVars()
_loadCommandArgs()
attr: local_development
attr: charts
attr: 
_update_context
## Chart
Chart
repositories() Repositories() Repsitory()
install()
hooks()
## Repository
Repository()
provider() attr
getChart()
## RepositoryGit
## RepositoryUrl
## RepositoryPath
## CLI Interface
## Kubectl Client
## Kubectl Provider
