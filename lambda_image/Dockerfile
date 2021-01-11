FROM public.ecr.aws/lambda/provided

ENV R_VERSION=4.0.3
ENV PATH="${PATH}:/opt/R/${R_VERSION}/bin/"

# install R
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
    && yum -y install https://cdn.rstudio.com/r/centos-7/pkgs/R-${R_VERSION}-1-1.x86_64.rpm \
    openssl-devel \
    libxml2-devel \
    unzip \
    && yum clean all \
    && rm -rf /var/cache/yum/*

# install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -f awscliv2.zip

# install R packages
RUN Rscript -e "install.packages(c('httr', 'logger', 'glue', 'jsonslite', 'randomForest'), repos = 'https://cloud.r-project.org/')"

COPY runtime.R predict.R ${LAMBDA_TASK_ROOT}/
RUN chmod 755 -R ${LAMBDA_TASK_ROOT}/

COPY bootstrap ${LAMBDA_RUNTIME_DIR}/
RUN chmod 755 ${LAMBDA_RUNTIME_DIR}/bootstrap
RUN rm -rf /tmp/*

CMD [ "predict.handler" ]