import pytest
import pytest_asyncio
import io
import uuid
from PIL import Image
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.database import Base, get_db
from app.core.security import get_password_hash, create_access_token
from app.models.user import User, UserRole
from app.main import app

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    async with TestSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def farmer_user(db_session: AsyncSession) -> User:
    uid = uuid.uuid4().hex[:6]
    user = User(
        name="Test Farmer",
        email=f"farmer_{uid}@example.com",
        password_hash=get_password_hash("Password123!"),
        role=UserRole.FARMER.value,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def expert_user(db_session: AsyncSession) -> User:
    uid = uuid.uuid4().hex[:6]
    user = User(
        name="Dr. Test Expert",
        email=f"expert_{uid}@example.com",
        password_hash=get_password_hash("Password123!"),
        role=UserRole.EXPERT.value,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession) -> User:
    uid = uuid.uuid4().hex[:6]
    user = User(
        name="Test Admin",
        email=f"admin_{uid}@example.com",
        password_hash=get_password_hash("Password123!"),
        role=UserRole.ADMIN.value,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
def farmer_token(farmer_user: User) -> str:
    return create_access_token(subject=farmer_user.id, role=farmer_user.role)

@pytest.fixture
def expert_token(expert_user: User) -> str:
    return create_access_token(subject=expert_user.id, role=expert_user.role)

@pytest.fixture
def admin_token(admin_user: User) -> str:
    return create_access_token(subject=admin_user.id, role=admin_user.role)

@pytest.fixture
def sample_leaf_image_bytes() -> bytes:
    img = Image.new("RGB", (200, 200), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()
