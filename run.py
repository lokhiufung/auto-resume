from dotenv import load_dotenv

load_dotenv()


# from auto_resume.app import create_app
from auto_resume.app_v2 import create_app


app = create_app()
app.run(debug=True)

