# Grocery Shop Demo Web Application

This repository contains a demo web application for a grocery shop developed using Django. You can deploy this application by forking the repo and deploying it on your preferred cloud service, such as Heroku or Render.com.

## Deployment Instructions

### Deploying on Render.com

1. **Create a PostgreSQL Database on Render**
   - Set up a PostgreSQL database on Render for your application.

2. **Building and Starting the Application**
   - Setup you Environment Variables:
        ```
        ALLOWED_HOSTS = "* localhost"
        DATABASE = <database_url>
        DEBUG = FALSE
        SECRET_KEY = <generate_secret_key>
        ```
   - Run the following commands:
     ```
     pip install -r requirements.txt
     ```
   - Note: For the initial deployment, uncomment line 9 in `build.sh` to create a superuser for the Django admin page and populate the database with data from `products.csv`.
   - For more details view scripts/data.py

3. **Deployment**
    ```
    ./build.sh
    ```
   - Once the initial setup is completed, you can deploy your application on Render.com.


## Usage

Upon successful deployment, visit the application URL to access the grocery shop demo. Use the features to browse products, make purchases, and experience the functionality of the web application.

## Important Notes

- **First Deployment:**
  - Uncomment line 9 in `build.sh` during the initial deploy to create a superuser for the Django admin page and populate the database with data from `products.csv`.

- **Subsequent Deployments:**
  - No need to recreate the superuser or reinsert the product data into the database for future deployments.

## Contributing

Feel free to contribute to the project by opening issues or pull requests.

## Acknowledgements

Special thanks to my teammates:

    - Peter Fayez

    - Mohamed Ayman