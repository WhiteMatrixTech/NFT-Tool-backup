FROM nytimes/blender:2.93-gpu-ubuntu18.04

RUN apt-get update
RUN apt-get install -y curl unzip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

COPY . .

ENV PATH="/root/.local/bin:/scripts:${PATH}"

RUN pip3.9 install --upgrade pip
RUN pip3.9 install --user pipenv
RUN pipenv install

RUN rm -rf /blender

RUN chmod -R 755 scripts

CMD ["start-runner.sh"]
