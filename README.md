# Property News Website

A modern Django-based news website focused on the real estate industry.

## Features

- News article publishing and management
- User authentication
- Article comments
- Post likes and view counters
- Responsive modern design
- Social media sharing

## Local Development

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the development server: `python manage.py runserver`

## Docker Deployment (Free Options)

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. Copy the environment variables example file:
   ```bash
   cp env.example .env
   ```

2. Edit the `.env` file and update the variables:
   - Generate a secure SECRET_KEY
   - Set ALLOWED_HOSTS to include your deployment domain
   - The DATABASE_URL is already configured in docker-compose.yml

### Local Docker Deployment with PostgreSQL

1. Build and start the Docker containers:
   ```bash
   docker-compose up -d --build
   ```

2. Run migrations for the PostgreSQL database:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. Create a superuser (admin):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. Access the application at http://localhost:8000

### Database Management

The PostgreSQL database is included in your docker-compose setup. Important notes:

- Database data is persisted in a Docker volume called `postgres_data`
- Default credentials are:
  - Username: postgres
  - Password: postgres
  - Database name: news_db
- You can access the database directly on port 5432
- For data backup:
  ```bash
  docker-compose exec db pg_dump -U postgres news_db > backup.sql
  ```
- To restore from backup:
  ```bash
  docker-compose exec -T db psql -U postgres news_db < backup.sql
  ```

### Free Hosting Options

#### Option 1: Railway

1. Create an account on [Railway](https://railway.app/)
2. Install the Railway CLI: `npm i -g @railway/cli`
3. Login to Railway: `railway login`
4. Initialize your project: `railway init`
5. Deploy your project: `railway up`

#### Option 2: Render

1. Create an account on [Render](https://render.com/)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set the environment variables from your `.env` file
5. Deploy the service

#### Option 3: Fly.io

1. Sign up for [Fly.io](https://fly.io/) 
2. Install the Flyctl CLI
3. Login: `flyctl auth login`
4. Launch the app:
   ```bash
   flyctl launch
   ```
5. Deploy the app:
   ```bash
   flyctl deploy
   ```

## Database Options

By default, the application uses SQLite. For production, you can configure PostgreSQL by setting the DATABASE_URL environment variable:

```
DATABASE_URL=postgres://username:password@hostname:port/database_name
```

## Additional Deployment Notes

- The application uses Gunicorn as the WSGI server
- Static files are collected to the `/staticfiles` directory
- Media files are stored in the `/media` directory
- For production, consider using a managed database service
- For improved performance, add a CDN for static files

## License

© {% now "Y" %} Copyright - Майборода Максим Валерійович 