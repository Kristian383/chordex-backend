import os
import shutil
from datetime import datetime, timedelta

# Configuration
db_path = 'data.db'                 # Path to SQLite database
backup_dir = 'database_backup'      # Directory to store backups
retention_days = 30                 # Number of days to keep old backups

def backup_database():
    # Ensure backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Generate backup file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_filename = f'database_backup_{timestamp}.db'
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Create a backup
    shutil.copy2(db_path, backup_path)
    print(f'Backup created: {backup_path}')
    
    # Remove old backups
    clean_old_backups()

def clean_old_backups():
    # Remove backups older than the retention period
    now = datetime.now()
    for filename in os.listdir(backup_dir):
        file_path = os.path.join(backup_dir, filename)
        if os.path.isfile(file_path):
            file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if (now - file_creation_time) > timedelta(days=retention_days):
                os.remove(file_path)
                print(f'Removed old backup: {file_path}')

if __name__ == '__main__':
    backup_database()
