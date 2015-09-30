FROM python:2.7.9
RUN apt-get update \
	&& apt-get install -y \
	python-imaging 	       \
	python-lxml            \ 
	libjpeg-dev            \
        libpng-dev             \
        libpq-dev              \
        libproj-dev            \
        libxml2-dev            \
        libxslt-dev            \
	python-imaging         \
        python-psycopg2        \
        python-support         \
	unzip                  \
	zip
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code


