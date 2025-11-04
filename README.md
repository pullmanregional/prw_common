# prw_common

This module is designed to be included as a submodule by other projects. It includes all of the SQLModel ORM files for tables in the PRW data warehouse and common utilities modules.

## Usage

To include this submodule in your project, use the following command:

```sh
# Add the submodule to the appropriate path under the main project, eg under src/
cd src/
git submodule add https://github.com/pullmanregional/prw_common.git prw_common

# Commit and push changes to this submodule from the main project
cd prw_common
git add .
git commit -m "Your commit message"
cd ..
git add prw_common
git commit -m "Updated submodule"
git push --recurse-submodules
```

Note, this submodule does not include a `pyproject.toml`. Parent projects must include required dependencies, including [SQLModel](https://sqlmodel.tiangolo.com/).
