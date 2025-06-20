# Camply Web Interface

A modern web interface for [camply](https://github.com/juftin/camply) - the campsite finder. This application allows users to create campsite availability alerts through a user-friendly web interface, leveraging camply's powerful search capabilities across multiple camping providers.

## Features

- **🔍 Smart Search**: Search across multiple camping providers including Recreation.gov, Yellowstone, California State Parks, and more
- **📱 SMS Notifications**: Get instant SMS alerts when campsites become available
- **🎯 Flexible Criteria**: Set specific date ranges, choose recreation areas, campgrounds, or individual campsites
- **⚡ Real-time Monitoring**: Continuous monitoring of availability with instant notifications
- **📊 Alert Management**: View, edit, and manage your campsite alerts
- **🧪 Test Notifications**: Test your alert setup before going live

## Architecture

- **Backend**: FastAPI (Python) with SQLAlchemy for database management
- **Frontend**: React with TypeScript for a modern, responsive UI
- **Database**: SQLite (development) / PostgreSQL (production)
- **Search Engine**: Integrated with camply's search providers
- **Notifications**: Twilio SMS integration

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Redis (for background tasks)
- Twilio account (for SMS notifications)

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd camply-web/backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run the backend server**:
   ```bash
   python run.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd camply-web/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
# Database Configuration
DATABASE_URL=sqlite:///./camply_web.db
# For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/camply_web

# Redis Configuration (for Celery)
REDIS_URL=redis://localhost:6379

# Twilio Configuration (for SMS notifications)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_SOURCE_NUMBER=your_twilio_phone_number

# API Keys
RECREATION_GOV_API_KEY=your_recreation_gov_api_key

# Application Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Twilio Setup

1. Create a [Twilio account](https://www.twilio.com/)
2. Get your Account SID and Auth Token from the Twilio Console
3. Purchase a phone number for sending SMS
4. Add these credentials to your `.env` file

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/notifications/` - Create a new notification preference
- `GET /api/notifications/` - Get all notifications for a user
- `PUT /api/notifications/{id}` - Update a notification preference
- `DELETE /api/notifications/{id}` - Delete a notification preference
- `GET /api/search/recreation-areas` - Search for recreation areas
- `GET /api/search/campgrounds` - Search for campgrounds
- `GET /api/search/campsites` - Search for campsites

## Usage

### Creating an Alert

1. Navigate to the web interface at `http://localhost:3000`
2. Click "Create Alert" or go to `/create-notification`
3. Select your desired date range
4. Search and select a recreation area, campground, or specific campsite
5. Enter your phone number for SMS notifications
6. Click "Create Alert"

### Managing Alerts

1. Go to "My Alerts" to view all your active notifications
2. Test your alerts to ensure notifications are working
3. Edit or delete alerts as needed

## Development

### Project Structure

```
camply-web/
├── backend/
│   ├── app/
│   │   ├── api/           # API routers
│   │   │   ├── models/        # Database models and schemas
│   │   │   ├── services/      # Business logic
│   │   │   └── utils/         # Utility functions
│   │   ├── tests/             # Backend tests
│   │   ├── requirements.txt   # Python dependencies
│   │   └── run.py            # Startup script
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── components/    # React components
│   │   │   ├── pages/         # Page components
│   │   │   ├── api/           # API client functions
│   │   │   └── utils/         # Utility functions
│   │   ├── public/            # Static files
│   │   └── package.json       # Node.js dependencies
│   └── docker/                # Docker configuration
```

### Running Tests

**Backend Tests**:
```bash
cd backend
pytest
```

**Frontend Tests**:
```bash
cd frontend
npm test
```

### Database Migrations

The application uses SQLAlchemy with automatic table creation. For production, consider using Alembic for database migrations:

```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Deployment

### Docker Deployment

1. **Build the images**:
   ```bash
   docker-compose build
   ```

2. **Run the services**:
   ```bash
   docker-compose up -d
   ```

### Production Considerations

- Use PostgreSQL instead of SQLite
- Set up proper authentication (JWT tokens)
- Configure HTTPS
- Set up monitoring and logging
- Use environment-specific configuration
- Implement rate limiting
- Set up backup strategies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built on top of [camply](https://github.com/juftin/camply) by juftin
- Uses [FastAPI](https://fastapi.tiangolo.com/) for the backend
- Uses [React](https://reactjs.org/) for the frontend
- SMS notifications powered by [Twilio](https://www.twilio.com/) 