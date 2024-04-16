# FROM condaforge/mambaforge
FROM condaforge/mambaforge:22.9.0-1

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /auto_sst
WORKDIR /auto_sst

# Install somisana-croco environment into base conda environment
COPY environment.yml .
RUN mamba env update -n base -f environment.yml

# Install somisana-croco
ADD . /auto_sst

ENTRYPOINT ["python", "run.py"]
