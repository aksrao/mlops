# Project - 1 (Hotel Reservation Prediction)

- Platform and resources :- AWS's S3 bucket
- Create a virtual env through conda.
- Tools:- python, pandas, jypter Notebook, Flask, numpy
- Package Manager - anaconda (conda)

## Terraform 
- through terraform create private bucket and role called mlops.
- this mlops role has to permission to do operation on this data.
- attache a bucket policy so that this role only can access to this bucket.
- this is done so that the unauthorized person cannot acces the data in s3.

## Conda Commands
- conda create --name "name" python=3.12
- conda activate "env name"
- conda env update -f environment.yml --prune
- conda install -c <channel_name> <dependencies_name>

## Env setup and insatll modules
![create virtual env](images/create_virtual_env_with_conda.png)
![activate and insatll](images/venv_activate_and_module_install.png)

## Data Ingestion output
![Result](images/data-ingestiion.png)

### Split the data
![split](images/split.png)


