# 📖 Geek Text - Bookstore API! 📖
  [![License: IPL 1.0](https://img.shields.io/badge/License-IPL_1.0-blue.svg)](https://opensource.org/licenses/IPL-1.0)
  ## Description
  
This bookstore API is powered by Python's Flask framework. You have the ability to browse and sort books, manage a profile and its credit cards, add to a shopping cart, check book details and add books as an admin, rate books and comment on them, and add books to a wishlist.

Created by the fellas over at Group 18. Enjoy!


## Technologies Used

* Python (programming language)
* Flask (Python API framework)
* SQLAlchemy/MySQL (database)
* HTML (rendering admin pages)
* Bootstrap (CSS framework for styling html)


  ## Table of Contents

  * [Installation](#installation)
  * [Usage](#usage)
  * [Contributing](#contributing)
  * [License Info](#license-info)


  ### Installation
  
  * Open a terminal, head to the desired destination folder and type ```git clone git@github.com:cheesecakeassassin/group18-bookstore-api.git```
  * Run ```cd group18-bookstore-api``` to enter the repository.
  * Run ```python -m venv venv``` to initiate a virtual environment.
  * Run ```venv/Scripts/activate``` for Windows and ```source venv/bin/activate``` for MacOS to enter the virtual environment to then install the dependencies.
  * Run ```pip install flask flask_admin flask_login bcrypt sqlalchemy pymysql python-dotenv dotenv``` to install all the needed dependencies.
  * Create a ```.env``` file in the root directory with the following text: ```DB_URL=mysql+pymysql://root:<password>@localhost/bookstore_api_db``` replacing ```<password>``` with your MySQL password (MySQL must be downloaded on your machine).
  * Run ```mysql -u root -p``` to enter the MySQL shell, then enter your MySQL password.
  * Run ```source app/db/schema.sql``` to create the database followed by ```exit``` to exit the MySQL shell.
  * Run ```python seeds.py``` to seed the database.
  * Finally, run ```python -m flask run``` to open the development sever and get to work!


  ### Usage

  * Just dive in on ```Postman``` or ```Insomnia``` to test the routes using the ```/api/``` endpoint! For admin actions use the ```/admins/``` endpoint to register/login!


  ### License Info
  * [IBM License](https://opensource.org/licenses/IPL-1.0)
  * The IPL is the open-source license IBM uses for some of its software. Supposed to facilitate commercial use of said software; is very clear on the specifics of liability. Also grants explicit patent rights.
  
  
  ### Contributing - Group 18

  * [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)
  * Sasha Scannell - **Book Details** - GitHub: https://github.com/thedinoinstitute
  * Thamare Saint Louis - **Shopping Cart** - GitHub: https://github.com/thamare1
  * Camilo Sanchez - **Wishlist** - GitHub: https://github.com/puesyo
  * Karim Salazar - **Book Browsing and Sorting** - GitHub: https://github.com/ksala046
  * Fernando Santamarta - **Book Rating and Commenting** - GitHub: https://github.com/fernandosantamarta
  * Sebastian Santa - **Profile Management** - GitHub: https://github.com/cheesecakeassassin  


  ### Further Questions?

  * If you have further questions, feel free to email one of us at one of the following addresss & we will get back to you as soon as we can: santasebastian@yahoo.com, tsain024@fiu.edu, sasha3295@yahoo.com, ksala046@fiu.edu, fsanta076@fiu.edu, csanc236@fiu.edu

