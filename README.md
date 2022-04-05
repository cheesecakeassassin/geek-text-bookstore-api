# group18-bookstore-api

Flask API with python

1. install flask

2. in terminal enter the following commands to create the database

   python
     >>> from app import db, Book
     >>> db.create_all()
     >>> exit()

3. to use postman on the web you first need to Download Postman Desktop Agent and create an account

4. Run your flask application. In terminal enter flask run

5. Go to PostMan and create a new HTTP request

6. in the Header part of the request select (key = Content type, value = aplication-json)

7. copy the URL of your flask application and paste it in the request URL in POSTMAN

8. add the routes form our app that you want to call to the end of the URL

9. for POST requests add a json to the Body section and select raw

10. For now we can ONLY ADD ONE BOOK AT THE TIME into the database

11. remember to run flask every time you change your code
