FROM ubuntu:22.04

RUN apt update
RUN apt install -y python3.10
RUN apt install -y python3-pip
# RUN apt install -y python3.10-venv
RUN apt install -y git
RUN apt install wget

SHELL ["/bin/bash", "--login", "-c"]

RUN mkdir -p /home/root/project
WORKDIR /home/root/project
COPY ./__init__.py /home/root/project
COPY ./__main__.py /home/root/project
COPY ./setup.py /home/root/project
RUN mkdir /home/root/project/func
COPY ./func/__init__.py /home/root/project/func
COPY ./func/func.py /home/root/project/func
COPY ./configDocker.json /home/root/project/config.json
COPY ./requirements.txt /home/root/project
COPY ya2ro/properties.yaml /home/root/ya2ro/src/ya2ro/resources/properties.yaml
COPY ya2ro/Research_Object.yaml /home/root
COPY installWordNet.py /home/root/project/

ENV CONDA_DIR=/home/root/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
RUN chmod 0700 ~/miniconda.sh
RUN bash ~/miniconda.sh -b -p ${CONDA_DIR}
RUN rm ~/miniconda.sh
ENV PATH=$CONDA_DIR/bin:$PATH

RUN echo ". ${CONDA_DIR}/etc/profile.d/conda.sh" >> ~/.profile
RUN conda init bash

ENV ENV_PREFIX=groupProject
RUN conda update --name base --channel defaults conda 
RUN conda create -n $ENV_PREFIX
RUN conda clean --all --yes

RUN conda activate ${ENV_PREFIX} && \
    python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    git clone https://github.com/kermitt2/grobid_client_python && \
    cd grobid_client_python && \
    python3 setup.py install && \
    cd .. && \
    pip install -e . && \
    python3 /home/root/project/installWordNet.py

COPY entrypoint.sh /home/root/
RUN chmod 0700 /home/root/entrypoint.sh
ENTRYPOINT ["/home/root/entrypoint.sh"]
