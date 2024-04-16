# auto_sst
operational sst plots

To run this locally, first create the conda environment:
```sh
mamba env create -f environment.yml
```
or use `conda` instead of `mamba` if you haven't moved to mamba yet

Then activate the environment
```sh
conda activate auto_sst
```

And run the script
```sh
python run.py <your-copernicus-username> <your-copernicus-password> <sender-email-address> <sender-email-password>
```

You can also run the script as a docker image, generated using the `Dockerfile` in this repo:
```sh
docker run --rm -v <your-local-dir>:/tmp ghcr.io/saeon/auto_sst_main:latest <your-copernicus-username> <your-copernicus-password> <sender-email-address> <sender-email-password>
``` 

This docker image is updated operationally once a day, and run on a 'github-hosted runner' following the workflow in `.github/workflows/run_ops.yml`

