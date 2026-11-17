# \# CampusFest â€“ College Event Management System

#

# CampusFest is a full-stack college event management platform that allows students to explore college events and register for individual and team competitions.

#

# The platform is designed for students of our college, providing a centralized way to discover events and manage registrations.

#

# \## Technology Stack

#

# | Component | Technology |

# |---|---|

# | Frontend | React.js |

# | Backend | Python, Django |

# | API | Django REST Framework |

# | Database | MySQL |

# | Authentication | JWT |

# | Version Control | Git and GitHub |

# | API Testing | Postman |

#

# \## Features

#

# \### Student Authentication

# \- Student registration using an authorized student ID.

# \- Student login using email and password.

# \- JWT-based authentication.

# \- Protected student profile.

#

# \### Event Management

# \- Browse available college events.

# \- View individual event details.

# \- Search events by name.

# \- Filter events by category.

# \- Support for individual and team events.

#

# \### Event Registration

# \- Register for individual events.

# \- Register teams for team-based events.

# \- Configure minimum and maximum team sizes for each event.

# \- Select a team captain.

# \- Validate student IDs and prevent duplicate registrations.

#

# \### Student Dashboard

# \- View student profile information.

# \- View individual event registrations.

# \- View team event registrations.

#

# \## Project Structure

#

# ```text

# CampusFest/

# â”‚

# â”œâ”€â”€ backend/

# â”‚   â”œâ”€â”€ accounts/

# â”‚   â”œâ”€â”€ events/

# â”‚   â”œâ”€â”€ config/

# â”‚   â”œâ”€â”€ manage.py

# â”‚   â”œâ”€â”€ requirements.txt

# â”‚   â””â”€â”€ .env.example

# â”‚

# â”œâ”€â”€ frontend/

# â”‚

# â”œâ”€â”€ .gitignore

# â””â”€â”€ README.md

# ```

#

# \## Backend Setup

#

# \### 1. Clone the repository

#

# ```bash

# git clone https://github.com/Madesh-ux/CampusFest.git

# cd CampusFest

# ```

#

# \### 2. Navigate to the backend

#

# ```bash

# cd backend

# ```

#

# \### 3. Create a virtual environment

#

# ```bash

# python -m venv .venv

# ```

#

# Activate it on Windows:

#

# ```bash

# .venv\\Scripts\\activate

# ```

#

# \### 4. Install dependencies

#

# ```bash

# pip install -r requirements.txt

# ```

#

# \### 5. Configure environment variables

#

# Copy `.env.example` and create a `.env` file.

#

# On Windows CMD:

#

# ```cmd

# copy .env.example .env

# ```

#

# Update `.env` with your own Django secret key and MySQL credentials.

#

# \*\*Never commit your actual `.env` file to GitHub.\*\*

#

# \### 6. Create the MySQL database

#

# Open MySQL and execute:

#

# ```sql

# CREATE DATABASE campusfest\_db;

# ```

#

# \### 7. Apply migrations

#

# ```bash

# python manage.py migrate

# ```

#

# \### 8. Create an admin account

#

# ```bash

# python manage.py createsuperuser

# ```

#

# \### 9. Start the development server

#

# ```bash

# python manage.py runserver

# ```

#

# Backend server:

#

# ```text

# http://127.0.0.1:8000/

# ```

#

# Django Admin:

#

# ```text

# http://127.0.0.1:8000/admin/

# ```

#

# \## API Endpoints

#

# \### Accounts

#

# | Method | Endpoint | Description |

# |---|---|---|

# | POST | `/api/accounts/register/` | Student registration |

# | POST | `/api/accounts/login/` | Student login |

# | GET | `/api/accounts/profile/` | View student profile |

# | POST | `/api/accounts/token/refresh/` | Refresh JWT token |

# | GET | `/api/accounts/my-registrations/` | View personal registrations |

#

# \### Events

#

# | Method | Endpoint | Description |

# |---|---|---|

# | GET | `/api/events/` | List active events |

# | GET | `/api/events/<id>/` | View event details |

# | POST | `/api/events/register/individual/` | Individual registration |

# | POST | `/api/events/register/team/` | Team registration |

#

# Protected endpoints require JWT authentication.

#

# \## Project Status

#

# Backend development is in progress. Authentication, event listing, individual registration, team registration and student registration history have been implemented and tested.

#

# Frontend integration and further testing are part of the ongoing development.

#

# \## Author

#

# \*\*Madesh S.\*\*

#

# GitHub: https://github.com/Madesh-ux
