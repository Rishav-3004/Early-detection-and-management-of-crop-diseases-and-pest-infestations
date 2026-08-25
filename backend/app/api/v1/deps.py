from typing import Optional
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.services.auth_service import auth_service
from app.models.user import User, UserRole

security_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not auth_credentials:
        raise UnauthorizedException("Missing authentication token")
    
    token = auth_credentials.credentials
    payload = decode_token(token)
    
    if payload.get("type") != "access":
        raise UnauthorizedException("Invalid token type. Access token required.")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token subject")

    user = await auth_service.get_user_by_id(db, user_id)
    if not user.is_active:
        raise UnauthorizedException("Account is disabled")

    return user

async def get_current_active_farmer(current_user: User = Depends(get_current_user)) -> User:
    # Farmers, Experts and Admins can access farmer capabilities
    return current_user

async def require_expert(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.EXPERT.value, UserRole.ADMIN.value]:
        raise ForbiddenException("Agricultural Expert privileges required")
    return current_user

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN.value:
        raise ForbiddenException("Administrator privileges required")
    return current_user
