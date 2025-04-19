FROM public.ecr.aws/lambda/python:3.11

# WORKDIR /etl_app

# there is no path for requirements.txt because it is in the same root as the docker file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# same as above
RUN pip install -r requirements.txt

# copy every python file into the lambda function directory inside the container
COPY ./script/*.py ${LAMBDA_TASK_ROOT}

# the first value before the "." is the filename where the function that is called is located in,
# and the second is the function-name which should be invoked when lambda is executed.
CMD [ "transform_anime_data.lambda_handler" ]


