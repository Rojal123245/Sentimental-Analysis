"""
Authors: Amita Verma, Marcus Fernandes, Ajit Gurung.
Flask application code for backend - support the website with the dashboard
References:
    https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim
    https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
    https://www.youtube.com/watch?v=RPU11g-0ByE&ab_channel=CoderPros
    https://www.youtube.com/watch?v=g5BfdCgrc8k
    https://medium.com/aws-pocket/aws-rds-with-mysql-using-flask-f1c6d8cc7eff
    https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html
"""

from website import create_app

# Calling the function create_app() from __init__.py
app = create_app()

# Initialization
if __name__ == '__main__':
    app.run(debug=True)
