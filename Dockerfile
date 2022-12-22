FROM python:3.10
WORKDIR /cfhqd
COPY cfhqd cfhqd
COPY Makefile Makefile
RUN pip install --upgrade -r cfhqd/requirements.txt
#RUN make db
CMD ["make", "run"]
