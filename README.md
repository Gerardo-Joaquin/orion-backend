# Create conda environment

Firstly, you need to install conda in your local environment.

Follow the next steps to create a conda environment and try apy locally. 
``` 
conda create --name mariavmasmas python=3.10
``` 

Next, activate conda environment with
``` 
conda activate mariavmasmas
``` 

Once you are in your venv, install packages with 
``` 
pip install -r requirements.txt
``` 

# Build with docker

Execute the following command to build with docker
``` 
docker build . -t orionvmasmas --no-cache
``` 

Run the container with docker run
``` 
docker run orionvmasmas -p 5003:8080
``` 
