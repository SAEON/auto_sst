FROM condaforge/mambaforge

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /auto_sst
WORKDIR /auto_sst

# Install environment into base conda environment
COPY environment.yml .
RUN mamba env update -n base -f environment.yml

# Install the code
ADD . /auto_sst

ENTRYPOINT ["python", "run.py"]
