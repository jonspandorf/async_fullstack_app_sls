FROM public.ecr.aws/lambda/python:3.12


RUN dnf update && dnf install mesa-libGLU  -y 

RUN pip install opencv-python

COPY haarcascade_frontalface_default.xml .

COPY main.py ${LAMBDA_TASK_ROOT}

CMD ["main.lambda_handler"]