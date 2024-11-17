# prw-model

This module is designed to be included as a submodule by other projects. It includes all of the SQLModel ORM files for tables in the PRH analytics warehouse.

## Usage

To include this submodule in your project, use the following command:

```sh
# Add the submodule to the appropriate path under the main project, eg under src/ 
cd src/
git submodule add https://github.com/pullmanregional/prw-model.git prw-model

# Commit and push changes to this submodule from the main project
cd prw-model
git add .
git commit -m "Your commit message"
cd ..
git add prw-model
git commit -m "Updated submodule"
git push --recurse-submodules
```

Note, this submodule does not include a `package.json`. Parent projects must include required dependencies, including [SQLModel](https://sqlmodel.tiangolo.com/).