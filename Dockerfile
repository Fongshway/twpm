################################################################################
# https://github.com/Fongshway/docker-python/blob/master/Dockerfile
FROM fongshway/python:production
################################################################################
ENV PROJECT_DIR="/opt/twpm" \
    PYTHONPATH="${PYTHONPATH}:${PROJECT_DIR}" \
    USER=twpm \
    TASKWARRIOR_VERSION=2.5.1+dfsg-7

# -- Create non-root user:
RUN useradd -ms /bin/bash ${USER} && \
    mkdir -p "${PROJECT_DIR}" && \
    chown -R ${USER}: "${PROJECT_DIR}" /usr/local /home/${USER} && \
    usermod -aG sudo ${USER} && \
    sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers

# -- Create application directory:
RUN set -ex && mkdir -p ${PROJECT_DIR}

WORKDIR "${PROJECT_DIR}"

USER ${USER}

# -- Install taskwarrior:
RUN sudo apt-get update && \
    sudo apt-get install -y taskwarrior=${TASKWARRIOR_VERSION} && \
    sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/* && \
    touch /home/twpm/.taskrc

COPY . "${PROJECT_DIR}"

RUN sudo chown -R ${USER}: "${PROJECT_DIR}"
