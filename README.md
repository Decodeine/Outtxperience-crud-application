# Outtxperience-crud-application
a simple crud application using fastapi and SQLAlchemy for ORM

To run the application
* Clone the repository:
git clone https://github.com/Decodeine/Outtxperience-crud-application.git

*Navigate to the directory you clone into

    example cd outtxperience
    
* Install the required Python packages:

pip install -r requirements.txt

* Set the `FLASK_APP` environment variable
    $env:FLASK_APP = "main"

* Run the application:
   python -m flask run

  The application will be accessible at `http://127.0.0.1:5000`.

## Docker Setup
navigate to your project directory
Build the Docker image using

    docker build -t my-flask-app .

 Run the Docker container:

    docker run -p 5000:5000 my-flask-app
    
 The application will be accessible at `http://localhost:5000`.


