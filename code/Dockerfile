# Use the official Jupyter Notebook Python 3.x image as the base image
FROM jupyter/base-notebook:python-3.10

# Set working directory
WORKDIR /code

# Add a requirements.txt file for your dependencies
COPY requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# Expose the Jupyter Notebook port
EXPOSE 8888

# Start Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
