FROM jupyter/base-notebook:python-3.9.7
ENV HOME /home/jovyan
USER root
COPY mace4-examples ${HOME}
RUN rm -rf ${HOME}/solutions
RUN chown -R jovyan ${HOME}
USER jovyan
WORKDIR ${HOME}
