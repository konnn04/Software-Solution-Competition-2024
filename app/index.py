from flask import Flask, request
from app import app
from flask import redirect

if __name__ == '__main__':    
    # context = ('app\certificates\cert.pem', 'app\certificates\key.pem')   
    # app.run(debug=True, ssl_context=context)
    app.run(debug=True)


    