FROM public.ecr.aws/lambda/python:3.12

WORKDIR /etl_app

# there is no path for requirements.txt because it is in the same root as the docker file
COPY requirements.txt .

# same as above
RUN pip install --no-cache-dir -r requirements.txt

# copy every python file into the lambda function directory inside the container
COPY ./script/*.py .
# Copy ALL application files to Lambda's default working directory
COPY script/ /var/task/

# Set Python path to include /var/task
ENV PYTHONPATH=/var/task
# the first value before the "." is the filename where the function that is called is located in,
# and the second is the function-name which should be invoked when lambda is executed.
CMD [ "transform_anime_data.lambda_handler" ]


