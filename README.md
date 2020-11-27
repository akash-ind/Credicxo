# Project API

API created for internship project at Credicxo

## Getting Started

To get started on your PC. Clone the repository. And then in virtual environment install
the dependencies by
```
pip install -r requirement.txt
```
### Notations
    ${variable} is used to describe value of variable
    <value1>, <value2> means value1 or value2.
### API Documentation

${domain}/api/token: takes in Form with POST request
    username: ${username}
    password: ${password}
It returns two JWT token access and refresh, access must be specified in authorization header of type
Bearer token
```
username: akash
password: akash
```
${domain}/api/refresh: takes in Form with POST request
    refresh: ${refresh_token}
It returns the JWT access token. It is necessary because refresh token are long lived.And access are short lived
```
refresh: ${refresh_token}
```
${domain}/list/users: A get request. It returns a list of users. 
1. All users in case Admin sends the request.
2. Only Students in case Teacher sends the request.
3. Only self in case if Student sends the request. 

${domain}/create/user: takes in Form with POST request.It takes values 
```
first_name: ${first_name}
last_name: ${last_name}
password: ${password}
username: ${username}
type: oneof{<student>, <teacher>, <admin>}
```
Only admin can create user of type admin, teacher, student.
teacher only create type student.
student can't create any user

${domain}/forgot-password: takes in Form POST request
    It takes in username and returns the temp token
```
    username: ${username}
```
token must be send in other request to change password.
${domain}/change-password: takes in Form POST reques
    It takes in token returned in previous step. 
    And new_password
```
    token: ${token}
    new_password: ${new_password}
```
We can extend it easily to emails. 