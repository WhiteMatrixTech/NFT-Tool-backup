FROM nytimes/blender:2.92-gpu-ubuntu18.04

RUN apt-get update
RUN apt-get install -y curl unzip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

COPY ./blender/2.93/scripts/addons/better_fbx /bin/2.92/scripts/addons/better_fbx

COPY . .

RUN rm -rf /blender

RUN chmod -R 755 scripts

ENV PATH="/scripts:${PATH}"

#CMD ["/bin/sh", "-c", "echo 'sleep infinity' | bash"]
CMD ["renderjob.sh"]
