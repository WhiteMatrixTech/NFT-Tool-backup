FROM nytimes/blender:2.92-gpu-ubuntu18.04

COPY ./blender/2.93/scripts/addons/better_fbx /bin/2.92/scripts/addons/better_fbx

COPY . .

RUN rm -rf /blender

RUN chmod +x test_run_pawn.sh

CMD ["/bin/sh", "-c", "echo 'sleep infinity' | bash"]
