import unittest
import main as app
from flask import session
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup


class TestAssignment(unittest.TestCase):

    def client(self):
        app.app.config["TESTING"] = True
        with app.app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "admin"
            yield client

    def test_signup(self):
        url = "http://127.0.0.1:5000/sign-up" 
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        heading_element = soup.find("h3")
        heading_text = heading_element.text.strip()
        expected_text = "Sign Up"
        self.assertEqual(heading_text, expected_text)

    def test_successful_signup(self):
        client = next(self.client())
        d={"email": "seedawy2002@gmail.com", "firstName": "Mariam", "password1": "pass12345678", "password2": "pass12345678"}
        response = client.post("/sign-up", data=d)   
        # Check if the login was successful and redirected to the expected page
        self.assertEqual(response.status_code, 200)

    def test_signup_fail(self):
        client = next(self.client())
        d={"email": "seedawy2002@gmail.com", "firstName": "Mariam", "password1": "pass", "password2": "pass"}

        response = client.post("/sign-up", data=d, follow_redirects=True)

        # Check if the signup was successful and redirected to the expected page
        self.assertEqual(response.request.path, "/sign-up")  # Check if the client is redirected to "/sign up" URL
    
    def test_loginpage(self):
        url = "http://127.0.0.1:5000/login"  
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        heading_element = soup.find("h3")
        heading_text = heading_element.text.strip()
        expected_text = "Login"
        self.assertEqual(heading_text, expected_text)

    def test_login_success(self):
        client = next(self.client())
        d={"email": "seedawy2002@gmail.com", "firstName": "Mariam", "password1": "pass12345678", "password2": "pass12345678"}
        response = client.post("/sign-up", data=d)   
        # Check if the login was successful and redirected to the expected page
        self.assertEqual(response.status_code, 200)

        d={"email": "seedawy2002@gmail.com", "password": "pass12345678"}
        response = client.post("/login", data=d)

        # Check if the login was successful and redirected to the expected page
        self.assertEqual(response.status_code, 200)  # Expect a 200 status code for the redirected page

    def test_login_fail(self):
        client = next(self.client())
        d={"email": "seedawy2002@gmail.com", "firstName": "Mariam", "password1": "pass12345678", "password2": "pass12345678"}
        response = client.post("/sign-up", data=d)   
        # Check if the login was successful and redirected to the expected page
        self.assertEqual(response.status_code, 200)

        d={"email": "seedawy2002@gmail.com", "password": "pass1234567"}
        response = client.post("/login", data=d)

        # Check if the login was successful and redirected to the expected page
        self.assertEqual(response.request.path, "/login")  # Check if the client is redirected to "/login" URL


    def test_logout(self):
        client = next(self.client())
        d={"email": "seedawy2002@gmail.com", "firstName": "Mariam", "password1": "pass12345678", "password2": "pass12345678"}
        response = client.post("/sign-up", data=d)   
        # Check if the login was successful and redirected to the expected page
        self.assertEqual(response.status_code, 200)

        d={"email": "seedawy2002@gmail.com", "password": "pass12345678"}
        response = client.post("/login", data=d)

        # Check if the login was successful and redirected to the expected page
        self.assertEqual(response.status_code, 200)  # Expect a 200 status code for the redirected page

        url = "http://127.0.0.1:5000/login"  
        response = client.post("/login", data=d)

        self.assertEqual(response.request.path, "/login")  # Check if the client is redirected to "/login" URL


    def test_support(self):
        client = next(self.client())
        d={"email": "seedawy2002@gmail.com", "firstName": "Mariam", "password1": "pass12345678", "password2": "pass12345678"}
        response = client.post("/sign-up", data=d)   
        # Check if the login was successful and redirected to the expected page
        self.assertEqual(response.status_code, 200)

        d={"email": "seedawy2002@gmail.com", "password": "pass12345678"}
        response = client.post("/login", data=d)

        # Check if the login was successful and redirected to the expected page
        self.assertEqual(response.status_code, 200)  # Expect a 200 status code for the redirected page
        response = client.post("/support")
        self.assertEqual(response.request.path, "/support")  # Check if the client is redirected to "/support" URL

if __name__ == '__main__':
    unittest.main()