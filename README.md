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

Lots of scope for generalising this, but it's a start
