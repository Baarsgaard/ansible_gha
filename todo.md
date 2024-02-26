# TODO
- Automatic detection of CI
- Configuration variables
    - `env_var_enabling_plugin: CI`
    - Allow override formatting. Role format, Play format, End format
- Common presets for popular CICD tools


# Defaults

## Github:

```
ENV: CI/GITHUB_ACTION

::group::Parsing Parameters
message inside Parsing Parameters
::endgroup::
``` 

## TeamCity:

```
ENV: TEAMCITY_VERSION

##teamcity[blockOpened name='Parsing Parameters']
message inside Parsing Parameters
##teamcity[blockClosed name='Parsing Parameters']
```

## Azure Devops
https://github.com/MicrosoftDocs/azure-devops-docs/issues/4051
```
ENV: BUILD_BUILDID
##[group]Parsing Parameters
message inside Parsing Parameters
##[endgroup]
```