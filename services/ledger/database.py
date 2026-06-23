from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from base import Base

DATABASE_URL = "postgresql+asyncpg://creditcore:creditcore@localhost:5432/creditcore"

# when your app starts, SQLAlchemy opens several connections (say 5) and keeps them ready
engine = create_async_engine(DATABASE_URL, echo=True)

# AsyncSessionLocal() creates a new session
# So each request gets its own session
# but all sessions share the connection pool underneath.
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# expire_on_commit=False — 
# by default, after you commit, SQLAlchemy marks all objects in the session as "expired"
# This causes problems in async code because that lazy fetch might happen outside the session context
# Setting this to False means objects keep their values after commit without needing another database round trip
