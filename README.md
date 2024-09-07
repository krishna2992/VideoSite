# VideoSite

Welcome to the Video Streaming Website project! This web application allows users to stream videos with support for HLS (HTTP Live Streaming). The project is built using Django (Python) for the backend and HTML, CSS, JavaScript for the frontend. AWS S3 is utilized for storage, and the application generates video thumbnails and previews dynamically.

# Features

HLS Streaming: Support for HTTP Live Streaming to ensure smooth and adaptive video playback.
AWS S3 Storage: Secure and scalable storage for video files.
Dynamic Thumbnails: Automatic generation of video thumbnails on-the-fly.

# Technologies Used
Backend: Django (Python)
Frontend: HTML, CSS, JavaScript
Storage: AWS S3
Thumbnail and Preview Generation: moviepy


# Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.x installed
Django installed (pip install django)
AWS account and S3 bucket configured
moviepy installed (for thumbnail and preview generation)

# Installation


1. Clone the repository:

```
git clone https://github.com/krishna2992/VideoSite.git
```
2. Create a virtual environment and activate it:
```
python -m venv env
source env/bin/activate
```
3. Install the required Python packages:
```
pip install -r requirements.txt
```

4. Configure Django settings:
Update settings.py with your AWS S3 credentials and bucket details.
Configure your DATABASES setting according to your database setup.
Set up any other environment-specific settings as required.
```
AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'your-region-name'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```
5. Apply migrations:

```
python manage.py makemigrations
python manage.py migrate
```

6.Create a superuser (for admin access):
```
python manage.py createsuperuser
```

7. Run the development server:
```
python manage.py runserver

```
Note: For Production , Use NGINX + GUNICORN For deployment.
