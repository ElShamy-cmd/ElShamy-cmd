# Deploying Milk Webapp

This guide provides instructions for deploying the Milk webapp to a web domain.

## Prerequisites

1. A web server with Python 3.8+ installed
2. A domain name and DNS access
3. SSL certificate (recommended)
4. Stable Diffusion models downloaded and placed in the `models` directory

## Installation Steps

1. Clone the repository to your server:
```bash
git clone <repository-url>
cd Milk
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the application:
   - Set up environment variables in `.env` file:
     ```
     FLASK_ENV=production
     FLASK_APP=app.py
     SECRET_KEY=your-secret-key
     ```
   - Adjust `config.py` settings if needed

## Web Server Setup

### Using Nginx (Recommended)

1. Install Nginx:
```bash
sudo apt update
sudo apt install nginx
```

2. Create a new Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/milk
```

3. Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/Milk/static;
    }
}
```

4. Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/milk /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Using Apache

1. Install Apache and mod_wsgi:
```bash
sudo apt update
sudo apt install apache2 libapache2-mod-wsgi-py3
```

2. Create a new Apache configuration file:
```bash
sudo nano /etc/apache2/sites-available/milk.conf
```

3. Add the following configuration:
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    ServerAdmin webmaster@your-domain.com
    
    WSGIDaemonProcess milk python-path=/path/to/Milk:/path/to/Milk/venv/lib/python3.8/site-packages
    WSGIProcessGroup milk
    WSGIScriptAlias / /path/to/Milk/wsgi.py
    
    <Directory /path/to/Milk>
        Require all granted
    </Directory>
    
    Alias /static /path/to/Milk/static
    <Directory /path/to/Milk/static>
        Require all granted
    </Directory>
</VirtualHost>
```

4. Enable the site and restart Apache:
```bash
sudo a2ensite milk.conf
sudo systemctl restart apache2
```

## Running the Application

1. Create a systemd service file:
```bash
sudo nano /etc/systemd/system/milk.service
```

2. Add the following configuration:
```ini
[Unit]
Description=Milk Web Application
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/Milk
Environment="PATH=/path/to/Milk/venv/bin"
ExecStart=/path/to/Milk/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

3. Start and enable the service:
```bash
sudo systemctl start milk
sudo systemctl enable milk
```

## SSL Configuration (Recommended)

1. Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx  # For Nginx
# OR
sudo apt install certbot python3-certbot-apache  # For Apache
```

2. Obtain SSL certificate:
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com  # For Nginx
# OR
sudo certbot --apache -d your-domain.com -d www.your-domain.com  # For Apache
```

## Monitoring and Maintenance

1. Check application logs:
```bash
sudo journalctl -u milk
```

2. Monitor Nginx/Apache logs:
```bash
sudo tail -f /var/log/nginx/error.log  # For Nginx
# OR
sudo tail -f /var/log/apache2/error.log  # For Apache
```

3. Regular maintenance:
   - Keep Python packages updated: `pip install -r requirements.txt --upgrade`
   - Monitor disk space for generated images
   - Regularly backup the database and important files
   - Check SSL certificate expiration

## Security Considerations

1. Keep all software updated
2. Use strong passwords
3. Configure firewall rules
4. Enable HTTPS
5. Set up rate limiting
6. Implement proper error handling
7. Regular security audits

## Troubleshooting

1. Check application logs for errors
2. Verify file permissions
3. Ensure all services are running
4. Check DNS configuration
5. Verify SSL certificate status
6. Monitor system resources

For additional help or issues, please open an issue in the repository. 