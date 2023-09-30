# smart-teachr-test


## Description

This is an e-learning platform that allows course creators to upload video or blog content, and enables consumers to view a feed of these courses and search them by name. All activity is meticulously tracked in the Postgres database.

## Technologies

This application is built with the Python language and uses NiceGUI for its graphical user interface. It utilizes Docker for build the environment, Postgres for database tracking, and Oracle storage for data preservation.

## Check it out

You can check out the application [here](https://smart-teachr.onrender.com).


## Setting up for Development

These instructions will get you a copy of the project up and running on your local machine for development purposes.
As the environment I deployed to is free (render), slowdowns can occur.

### Prerequisites

What things you need to install the software and how to install them:

1. Docker: [Download](https://www.docker.com/products/docker-desktop)
2. Python 3.9: [Download](https://www.python.org/downloads/)
3. Postgres: [Download](https://www.postgresql.org/download/)

### Running the App

1. Clone the repository on your local machine using `git clone`

   ```
   git clone <Repository link>
   ```

2. Navigate into the cloned repository

3. Run Docker compose to start up the application services

   ```
   docker-compose up
   ```

4. Visit `http://localhost:8080` in your browser to access the application

That's it, you are now up and running!


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Contact

If you have any questions about this repository, or need some help, you can reach out to me at `melotarcisio@hotmail.com`. Catch ya!
