from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserUpdateRequest, PasswordChangeRequest
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import ConflictException, UnauthorizedException, NotFoundException, ValidationException

class AuthService:
    async def register(self, db: AsyncSession, data: RegisterRequest) -> TokenResponse:
        # Check if email exists
        query = select(User).where(User.email == data.email.lower())
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise ConflictException("A user with this email address already exists.")

        user = User(
            name=data.name.strip(),
            email=data.email.lower().strip(),
            password_hash=get_password_hash(data.password),
            phone=data.phone.strip() if data.phone else None,
            role=data.role,
            language=data.language or "en",
            is_active=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        access_token = create_access_token(subject=user.id, role=user.role)
        refresh_token = create_refresh_token(subject=user.id, role=user.role)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            language=user.language
        )

    async def login(self, db: AsyncSession, data: LoginRequest) -> TokenResponse:
        query = select(User).where(User.email == data.email.lower().strip())
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.password_hash):
            raise UnauthorizedException("Invalid email or password.")

        if not user.is_active:
            raise UnauthorizedException("This account is currently deactivated.")

        access_token = create_access_token(subject=user.id, role=user.role)
        refresh_token = create_refresh_token(subject=user.id, role=user.role)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            language=user.language
        )

    async def refresh(self, db: AsyncSession, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid refresh token")

        user_id = payload.get("sub")
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive")

        new_access = create_access_token(subject=user.id, role=user.role)
        new_refresh = create_refresh_token(subject=user.id, role=user.role)

        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            user_id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            language=user.language
        )

    async def get_user_by_id(self, db: AsyncSession, user_id: str) -> User:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")
        return user

    async def update_profile(self, db: AsyncSession, user_id: str, data: UserUpdateRequest) -> User:
        user = await self.get_user_by_id(db, user_id)
        if data.name is not None:
            user.name = data.name.strip()
        if data.phone is not None:
            user.phone = data.phone.strip()
        if data.language is not None:
            user.language = data.language
        if data.is_active is not None:
            user.is_active = data.is_active

        await db.commit()
        await db.refresh(user)
        return user

    async def change_password(self, db: AsyncSession, user_id: str, data: PasswordChangeRequest) -> bool:
        user = await self.get_user_by_id(db, user_id)
        if not verify_password(data.current_password, user.password_hash):
            raise ValidationException("Current password does not match.")
        
        user.password_hash = get_password_hash(data.new_password)
        await db.commit()
        return True

auth_service = AuthService()
