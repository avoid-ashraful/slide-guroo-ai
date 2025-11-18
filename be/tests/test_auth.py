"""
Comprehensive authentication tests for SlideGuroo API
"""
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from main import app
from database import Base, get_db
from db_models import User
from auth_utils import get_password_hash

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://slideguroo:slideguroo123@localhost:5432/slideguroo_test_db"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=False
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test"""
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session):
    """Create a test client with database override"""
    async def override_get_db():
        try:
            yield db_session
        except Exception:
            await db_session.rollback()
            raise

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session):
    """Create a test user"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("TestPassword123!"),
        full_name="Test User",
        is_verified=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


class TestUserRegistration:
    """Tests for user registration"""

    @pytest.mark.asyncio
    async def test_register_success(self, client):
        """Test successful user registration"""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "SecurePassword123!",
                "full_name": "New User"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert data["full_name"] == "New User"
        assert data["is_verified"] is False
        assert "id" in data

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",  # Same as test_user
                "username": "differentuser",
                "password": "SecurePassword123!",
                "full_name": "Different User"
            }
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, client, test_user):
        """Test registration with duplicate username"""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "different@example.com",
                "username": "testuser",  # Same as test_user
                "password": "SecurePassword123!",
                "full_name": "Different User"
            }
        )

        assert response.status_code == 400
        assert "already taken" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "invalidemail",
                "username": "newuser",
                "password": "SecurePassword123!",
                "full_name": "New User"
            }
        )

        assert response.status_code == 422  # Validation error


class TestUserLogin:
    """Tests for user login"""

    @pytest.mark.asyncio
    async def test_login_success(self, client, test_user):
        """Test successful login"""
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password"""
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "WrongPassword123!"
            }
        )

        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "Password123!"
            }
        )

        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()


class TestEmailVerification:
    """Tests for email verification"""

    @pytest.mark.asyncio
    async def test_verify_email_success(self, client, db_session):
        """Test successful email verification"""
        # Create unverified user with verification token
        user = User(
            email="unverified@example.com",
            username="unverified",
            hashed_password=get_password_hash("Password123!"),
            full_name="Unverified User",
            is_verified=False,
            verification_token="test_verification_token"
        )
        db_session.add(user)
        await db_session.commit()

        response = await client.post(
            "/api/auth/verify-email",
            json={"token": "test_verification_token"}
        )

        assert response.status_code == 200
        assert "verified successfully" in response.json()["message"].lower()

    @pytest.mark.asyncio
    async def test_verify_email_invalid_token(self, client):
        """Test email verification with invalid token"""
        response = await client.post(
            "/api/auth/verify-email",
            json={"token": "invalid_token"}
        )

        assert response.status_code == 400


class TestPasswordReset:
    """Tests for password reset flow"""

    @pytest.mark.asyncio
    async def test_forgot_password_success(self, client, test_user):
        """Test successful password reset request"""
        response = await client.post(
            "/api/auth/forgot-password",
            json={"email": "test@example.com"}
        )

        assert response.status_code == 200
        assert "reset link sent" in response.json()["message"].lower()

    @pytest.mark.asyncio
    async def test_forgot_password_nonexistent_email(self, client):
        """Test password reset with non-existent email"""
        response = await client.post(
            "/api/auth/forgot-password",
            json={"email": "nonexistent@example.com"}
        )

        # Should return 200 for security (don't reveal if email exists)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_reset_password_success(self, client, db_session):
        """Test successful password reset"""
        # Create user with reset token
        user = User(
            email="resetuser@example.com",
            username="resetuser",
            hashed_password=get_password_hash("OldPassword123!"),
            full_name="Reset User",
            is_verified=True,
            reset_token="test_reset_token"
        )
        db_session.add(user)
        await db_session.commit()

        response = await client.post(
            "/api/auth/reset-password",
            json={
                "token": "test_reset_token",
                "new_password": "NewPassword123!"
            }
        )

        assert response.status_code == 200
        assert "reset successfully" in response.json()["message"].lower()

    @pytest.mark.asyncio
    async def test_reset_password_invalid_token(self, client):
        """Test password reset with invalid token"""
        response = await client.post(
            "/api/auth/reset-password",
            json={
                "token": "invalid_token",
                "new_password": "NewPassword123!"
            }
        )

        assert response.status_code == 400


class TestProtectedEndpoints:
    """Tests for protected endpoints"""

    @pytest.mark.asyncio
    async def test_get_current_user_success(self, client, test_user):
        """Test getting current user info with valid token"""
        # Login to get token
        login_response = await client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!"
            }
        )
        token = login_response.json()["access_token"]

        # Get current user
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_protected_endpoint_no_token(self, client):
        """Test accessing protected endpoint without token"""
        response = await client.get("/api/auth/me")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_protected_endpoint_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401


class TestIntegration:
    """Integration tests for complete auth flows"""

    @pytest.mark.asyncio
    async def test_complete_registration_and_login_flow(self, client):
        """Test complete user registration and login flow"""
        # Step 1: Register
        register_response = await client.post(
            "/api/auth/register",
            json={
                "email": "integration@example.com",
                "username": "integrationuser",
                "password": "IntegrationPass123!",
                "full_name": "Integration User"
            }
        )

        assert register_response.status_code == 201
        user_data = register_response.json()

        # Step 2: Login (should work even if not verified)
        login_response = await client.post(
            "/api/auth/login",
            json={
                "email": "integration@example.com",
                "password": "IntegrationPass123!"
            }
        )

        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Step 3: Access protected endpoint
        me_response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert me_response.status_code == 200
        assert me_response.json()["email"] == "integration@example.com"

    @pytest.mark.asyncio
    async def test_complete_password_reset_flow(self, client, test_user, db_session):
        """Test complete password reset flow"""
        # Step 1: Request password reset
        forgot_response = await client.post(
            "/api/auth/forgot-password",
            json={"email": "test@example.com"}
        )

        assert forgot_response.status_code == 200

        # Get the reset token from the database
        await db_session.refresh(test_user)
        reset_token = test_user.reset_token

        assert reset_token is not None

        # Step 2: Reset password with token
        reset_response = await client.post(
            "/api/auth/reset-password",
            json={
                "token": reset_token,
                "new_password": "NewTestPassword123!"
            }
        )

        assert reset_response.status_code == 200

        # Step 3: Login with new password
        login_response = await client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "NewTestPassword123!"
            }
        )

        assert login_response.status_code == 200

        # Step 4: Verify old password doesn't work
        old_login_response = await client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!"  # Old password
            }
        )

        assert old_login_response.status_code == 401
