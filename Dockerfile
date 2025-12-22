#Old
#FROM condaforge/mambaforge

#ENV DEBIAN_FRONTEND noninteractive

#RUN mkdir /auto_sst
#WORKDIR /auto_sst

# Install environment into base conda environment
#COPY environment.yml .
#RUN mamba env update -n base -f environment.yml

# Install the code
#ADD . /auto_sst

#ENTRYPOINT ["python", "run.py"]

## New
FROM condaforge/mambaforge:23.11.0-0

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /auto_sst

# Copy environment definition
COPY environment.yml .

# Create a clean conda environment (more reliable than updating base)
RUN mamba env create -n auto_sst -f environment.yml \
 && conda clean -afy

# Activate the environment
ENV PATH=/opt/conda/envs/auto_sst/bin:$PATH

# Copy the code
COPY . /auto_sst

ENTRYPOINT ["python", "run.py"]
