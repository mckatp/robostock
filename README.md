<p align="center">
  <img src="inventory/static/inventory/images/logo.svg" alt="RoboStock Logo" width="200">
</p>

<h1 align="center">RoboStock</h1>

<p align="center">
  <strong>Inventory Management System for Robotics Labs</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django 5.2">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Gunicorn-WSGI-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn">
  <img src="https://img.shields.io/badge/status-production%20deployed-brightgreen?style=for-the-badge">
</p>

---

RoboStock is a full-featured inventory management system designed for robotics and electronics labs. It tracks components, manages checkouts and returns, records sales, and keeps your team informed with low-stock alerts and email notifications.

## 🧑‍💻 Development

This project was collaboratively initiated with [@mckatp](https://github.com/mckatp).
The system architecture, all core features, database design, deployment
infrastructure, and ongoing development were built by
[@muhasin-code](https://github.com/muhasin-code).

The system is actively deployed within Bloomberg Research Institute of Digital
Communications Pvt Ltd, accessible across the organization's LAN.

## ✨ Features

| Feature                       | Description                                                                                                          |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **📦 Component Management**   | Add, edit, and delete components with serial numbers, categories, images, datasheet links, and box/location tracking |
| **🔄 Checkout & Return**      | Check out components to beneficiaries with quantity tracking; return them when done — with full transaction history  |
| **💰 Sales Tracking**         | Record component sales with pricing, payment status, and buyer information                                           |
| **👥 Beneficiary Management** | Manage employees, students, and interns with profiles, photos, and detailed contact information                      |
| **🚨 Low-Stock Alerts**       | Dashboard highlights components running low (≤ 5 units), color-coded by severity — red for 0, orange for 1–2         |
| **📧 Email Notifications**    | Automatic email alerts on checkout and return events via Gmail SMTP                                                  |
| **🖼️ Image Uploads**          | Upload and display component photos and beneficiary profile pictures                                                 |
| **👮 Role-Based Access**      | Admin and staff roles control who can manage inventory, users, and categories                                        |
| **🔐 User Management**        | Create and manage user accounts with password change support                                                         |
| **💾 Database Backups**       | Automated PostgreSQL backup and restore scripts with configurable retention                                          |

## 🛠️ Tech Stack

- **Backend:** Django 5.2, Python 3.10+
- **Database:** PostgreSQL with `psycopg2`
- **WSGI Server:** Gunicorn
- **Static Files:** WhiteNoise (compressed + cached)
- **Image Processing:** Pillow
- **Configuration:** `python-decouple` (`.env`-based)

## 📁 Project Structure

```
robostock/
├── inventory/                  # Main application
│   ├── management/commands/    # Custom management commands
│   ├── migrations/             # Database migrations
│   ├── static/inventory/       # Static assets (logo, favicon)
│   ├── templates/inventory/    # Django HTML templates
│   │   ├── base.html           # Base layout template
│   │   ├── dashboard.html      # Main dashboard
│   │   ├── component_*.html    # Component CRUD templates
│   │   ├── checkout_form.html  # Component checkout
│   │   ├── sell_form.html      # Component sales
│   │   ├── beneficiary_*.html  # Beneficiary templates
│   │   ├── user_*.html         # User management templates
│   │   └── ...
│   ├── templatetags/           # Custom template tags
│   ├── admin.py                # Django admin configuration
│   ├── forms.py                # Form definitions
│   ├── models.py               # Data models (Component, Category, Beneficiary, Transaction, Sale)
│   ├── urls.py                 # URL routing
│   └── views.py                # View logic
├── robostock/                  # Project configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py                 # WSGI entry point
├── backups/                    # Database backup/restore scripts
│   ├── backup_db.sh            # Automated backup with retention
│   └── restore_db.sh           # Backup restore utility
├── media/                      # User-uploaded files (git-ignored)
├── .env                        # Environment variables (git-ignored)
├── manage.py                   # Django management CLI
├── requirements.txt            # Python dependencies
└── Procfile                    # Process manager configuration
```

## 🚀 Getting Started

### Prerequisites

- **Python** 3.10 or higher
- **PostgreSQL** 14 or higher
- **pip** (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/robostock.git
   cd robostock
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**

   Create a PostgreSQL database and user:

   ```sql
   CREATE DATABASE robostock_db;
   CREATE USER your_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE robostock_db TO your_user;
   ```

5. **Configure environment variables**

   Create a `.env` file in the project root (see [Environment Variables](#-environment-variables) below).

6. **Run migrations**

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**

   ```bash
   python manage.py collectstatic --noinput
   ```

9. **Start the development server**

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000` to access RoboStock.

## ⚙️ Environment Variables

Create a `.env` file in the project root with the following variables:

| Variable               | Description                     | Example                                   |
| ---------------------- | ------------------------------- | ----------------------------------------- |
| `SECRET_KEY`           | Django secret key               | `django-insecure-change-me-in-production` |
| `DEBUG`                | Enable debug mode               | `True` or `False`                         |
| `USE_HTTPS`            | Enable HTTPS-only cookies       | `False` (set `True` only with SSL)        |
| `ALLOWED_HOSTS`        | Comma-separated allowed hosts   | `localhost,127.0.0.1`                     |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins | `https://yourdomain.com`                  |
| `DB_NAME`              | PostgreSQL database name        | `robostock_db`                            |
| `DB_USER`              | PostgreSQL username             | `your_user`                               |
| `DB_PASSWORD`          | PostgreSQL password             | `your_password`                           |
| `DB_HOST`              | Database host                   | `127.0.0.1`                               |
| `DB_PORT`              | Database port                   | `5432`                                    |
| `EMAIL_HOST_USER`      | Gmail address for notifications | `your-email@gmail.com`                    |
| `EMAIL_HOST_PASSWORD`  | Gmail App Password              | `xxxx xxxx xxxx xxxx`                     |

> **Note:** For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) — not your regular password.

## 🌐 Deployment

RoboStock runs in production with **Gunicorn** behind **Nginx**:

```bash
# Start with Gunicorn
gunicorn robostock.wsgi --bind 0.0.0.0:8000
```

A `Procfile` is included for process managers. Make sure to:

- Set `DEBUG=False` in `.env`
- Set `ALLOWED_HOSTS` to your server IP/domain
- Configure Nginx to proxy to Gunicorn and serve `/media/` files
- Set `USE_HTTPS=True` if you have an SSL certificate

### Running as a systemd service (production)

The application runs as a persistent background service on Ubuntu Server:

```ini
# /etc/systemd/system/robostock.service
[Unit]
Description=RoboStock Gunicorn Service
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/robostock
ExecStart=/path/to/venv/bin/gunicorn robostock.wsgi --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable robostock
sudo systemctl start robostock
sudo systemctl status robostock
```

## 💾 Backup & Restore

Database backup scripts are located in the `backups/` directory:

```bash
# Create a backup
bash backups/backup_db.sh

# Restore from a backup
bash backups/restore_db.sh
```

Backups are compressed (`.sql.gz`) with automatic retention — old backups are pruned after 7 days. Set up a cron job for automated daily backups:

```bash
# Run daily at 2:00 AM
0 2 * * * /home/user/robostock/backups/backup_db.sh >> /var/log/robostock-backup.log 2>&1
```

## 🧪 Running Tests

```bash
python manage.py test inventory
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).
