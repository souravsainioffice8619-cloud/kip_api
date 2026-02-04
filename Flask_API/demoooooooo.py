"""Database utility helpers using SQLAlchemy.

Requires environment variable `DATABASE_URL`, e.g.:
  postgresql+psycopg2://user:password@localhost:5432/dbname

Install requirements:
  pip install sqlalchemy psycopg2-binary
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_URL', '').strip()

# If DATABASE_URL isn't set we can build it from DB_* vars in .env
if not DATABASE_URL:
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_NAME')
    if db_user and db_password and db_name:
        # Validate port is numeric; fall back to 5432 on invalid
        try:
            int(db_port)
        except Exception:
            db_port = '5432'
        # URL-encode credentials to handle special characters
        try:
            from urllib.parse import quote_plus
            user_enc = quote_plus(db_user)
            pw_enc = quote_plus(db_password)
        except Exception:
            user_enc = db_user
            pw_enc = db_password
        DATABASE_URL = f"postgresql+psycopg2://{user_enc}:{pw_enc}@{db_host}:{db_port}/{db_name}"

_engine: Engine | None = None


def get_engine() -> Engine:
    """Return a SQLAlchemy engine, creating it if necessary."""
    global _engine
    if _engine is None:
        if not DATABASE_URL:
            raise RuntimeError('DATABASE_URL is not set. Set DATABASE_URL or DB_USER/DB_PASSWORD/DB_NAME in .env')
        
        # Actually create the engine
        try:
            _engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging SQL queries
            print(f"Created database engine with URL: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")
        except Exception as e:
            raise RuntimeError(f"Failed to create database engine: {str(e)}")
    
    return _engine


def get_connection():
    """Get a database connection."""
    engine = get_engine()
    return engine.connect()


# Optional: Add a function to test the connection
def test_connection():
    """Test the database connection."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


# Optional: Initialize on import if you want immediate feedback
if __name__ == "__main__":
    # Test the connection when run directly
    test_connection()
else:
    # Or test when imported
    # test_connection()  # Uncomment if you want immediate feedback on import
    pass