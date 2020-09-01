## uhmalguhm
 uh *mal* guhm

 The purpose of this project is to provide a easy to use interface to spin up virtual machines that use docker images as an overlay to the root filesystem.

 Essentially uhmalguhm will build an image that is very fast to boot up that is capable of consuming a Dockerfile.

### How to setup a development environment
Currently this application is being developed on OpenSuse tumbleweed and has not been tested on any other distro.

```
sudo zypper -y install git python3-pip docker libguestfs-devel python3-devel libguestfs gcc
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
pip install pipenv
echo 'PATH=$PATH:~/.local/bin' >> ~/.bashrc
sudo reboot
```

### How to use this software
```
git clone https://github.com/fortnebula/uhmalguhm.git
cd uhmalguhm
pipenv shell
pip install -r requirements.txt
docker run -d -p 6379:6379 redis:latest
celery worker -A worker.celery --loglevel=info &
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
```

You can also use supervisor with the included config file to start flask, redis, and celery, however it won't auto-reload
```
supervisord
```
### Where to find the documentation

This README serves as the documentation for usage of uhmalguhm for now. Additionally the application includes some rudimentary docs at the root url.

### What does this thing do?

Currently this application at the POC stage. The only things you can do are create users, issue tokens, and refresh tokens.
This README will be updated until a better doc system is put into place. It is expected that each function should have an example on interactions with this software.

### Register a user
To use the api, first a user needs to be created

```
curl -H "Content-Type: application/json" -X POST   -d '{"username":"test","password":"test"}' http://localhost:5000/api/v1/user/create
```

A successful registration should return

```
{
    "status": "registered",
    "username": "test"
}
```

### Obtain an access and refresh token

Now that you have a user, you can request an access token using the token endpoint

```
curl -H "Content-Type: application/json" -X POST   -d '{"username":"test","password":"test"}' http://localhost:5000/api/v1/token/issue
```

This will return an access token and a refresh token

```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTgzNTU5MDIsIm5iZiI6MTU5ODM1NTkwMiwianRpIjoiZjNjODVkOTUtMzQ1Mi00MDM4LThhMmYtNDQzMjdmMDZkYjAzIiwiZXhwIjoxNTk4MzU2ODAyLCJpZGVudGl0eSI6InRlc3QxIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.J2if1aJ5qWzLZHs389IpyA04qBZXlDGLF7W9G98wVt8",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTgzNTU5MDIsIm5iZiI6MTU5ODM1NTkwMiwianRpIjoiOWExYzBiMDMtZGZmZi00N2NlLWJhZmUtODE1M2U2NWM0NWMxIiwiZXhwIjoxNjAwOTQ3OTAyLCJpZGVudGl0eSI6InRlc3QxIiwidHlwZSI6InJlZnJlc2gifQ.LcfWa0xheY6r1T9x6z66Ho7wk2qSm2LdDXMTFGyJZKs"

```

### Refresh a token

If the access token expires, the refresh token method will issue a new access token

First export the refresh token to a variable so it's easier to work with

```
export REFRESH="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTgzNTU5MDIsIm5iZiI6MTU5ODM1NTkwMiwianRpIjoiOWExYzBiMDMtZGZmZi00N2NlLWJhZmUtODE1M2U2NWM0NWMxIiwiZXhwIjoxNjAwOTQ3OTAyLCJpZGVudGl0eSI6InRlc3QxIiwidHlwZSI6InJlZnJlc2gifQ.LcfWa0xheY6r1T9x6z66Ho7wk2qSm2LdDXMTFGyJZKs"
```

You can now use this refresh token to obtain a new access token by posting to the refresh endpoint

```
curl -H "Authorization: Bearer $REFRESH" -X POST http://localhost:5000/api/v1/token/refresh
```

The API should return a new access token to extend the lifetime of your current session

```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTgzNTU5MjEsIm5iZiI6MTU5ODM1NTkyMSwianRpIjoiYmNhYWM2MjktNzBlNS00NDVlLWI3OTctODc1Mzc4OTE5MDNhIiwiZXhwIjoxNTk4MzU2ODIxLCJpZGVudGl0eSI6InRlc3QxIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.TexDr4flGEkS_ZQmXPEvWBqGH5Wxya_xDALDOX9KKJ0"
}

```

### Create an virtual machine image

*** Warning
This code is still very much a work in progress and moving very fast, so don't
count on anything to be consistent until this method is stablized and you do
not see this warning anymore

First you need an access token, so hit the api to issue a token

```
curl -H "Content-Type: application/json" -X POST   -d '{"username":"test1","password":"test1"}' http://localhost:5000/api/v1/token/issue
{
 "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTg3MjM3NzYsIm5iZiI6MTU5ODcyMzc3NiwianRpIjoiY2Q5Njg2YmQtZDk3Ny00OWI1LWI1NTktMTJkYjEyYTlmOTNiIiwiZXhwIjoxNTk4NzI0Njc2LCJpZGVudGl0eSI6InRlc3QxIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.hcbnv7aZoVqPjoHkKOlLlueb9iuLR8AZRnkJr72ZMVY",
 "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTg3MjM3NzYsIm5iZiI6MTU5ODcyMzc3NiwianRpIjoiZTk3NWE3ZTMtMjE5My00ZDRiLThlODAtM2E3NTdmMzdkYWRiIiwiZXhwIjoxNjAxMzE1Nzc2LCJpZGVudGl0eSI6InRlc3QxIiwidHlwZSI6InJlZnJlc2gifQ.me1X1z24D4IACWZbF59vBCYq5aCYDbIpiPSt79-HytA"
}
```

Next export the access token to make your life less hateful

```
export ACS="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTg3MjM3NzYsIm5iZiI6MTU5ODcyMzc3NiwianRpIjoiY2Q5Njg2YmQtZDk3Ny00OWI1LWI1NTktMTJkYjEyYTlmOTNiIiwiZXhwIjoxNTk4NzI0Njc2LCJpZGVudGl0eSI6InRlc3QxIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.hcbnv7aZoVqPjoHkKOlLlueb9iuLR8AZRnkJr72ZMVY"
```

Now you can tell uhmalguhm to create a virtual machine image

```
curl -H "Authorization: Bearer $ACS"  -H "Content-Type: application/json" -X POST -d '{"image":"nginx", "tag":"latest"}' http://localhost:5000/api/v1/container/create
{
 "id": "b3b47b6d-b208-47a7-af2e-e7df92524678",
 "status": "building"
}
```

That's all for now, it just builds and deletes the image. However in the near
term this function will copy the image to the storage locations you have setup
in the API. (this doesn't exsist yet)

