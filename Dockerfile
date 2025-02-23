FROM public.ecr.aws/lambda/python:3.13

COPY app/app.py ${LAMBDA_TASK_ROOT}
COPY app/requirements.txt  .

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD [ "app.lambda_handler" ] 
