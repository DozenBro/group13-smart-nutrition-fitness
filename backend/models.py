from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, CheckConstraint, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Measurement(Base):
    __tablename__ = 'measurements'
    __table_args__ = (
        CheckConstraint('weight_kg > 0 AND weight_kg <= 500', name='weight_range'),
        CheckConstraint('height_cm >= 50 AND height_cm <= 250', name='height_range'),
    )

    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True) # Nullable temporarily for migration
    user: Mapped["User | None"] = relationship(back_populates="measurements")
    id: Mapped[int] = mapped_column(primary_key=True)
    weight_kg: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    height_cm: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

class Food(Base):
    __tablename__ = 'foods'
    __table_args__ = (
        CheckConstraint('calories >= 0', name='food_calories_non_negative'),
        CheckConstraint('protein_g >= 0', name='food_protein_non_negative'),
        CheckConstraint('carbs_g >= 0', name='food_carbs_non_negative'),
        CheckConstraint('fat_g >= 0', name='food_fat_non_negative'),
        CheckConstraint('price_vnd >= 0', name='food_price_non_negative'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    portion_desc: Mapped[str] = mapped_column(String(100))  # Eg: "one medium bowl (~350g)"
    calories: Mapped[Decimal] = mapped_column(Numeric(7, 2))
    protein_g: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    carbs_g: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    fat_g: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    price_vnd: Mapped[int] = mapped_column(Integer)
    meal_slot: Mapped[str] = mapped_column(String(50), index=True)  # Eg: "breakfast,lunch,dinner"
    preference_tags: Mapped[str | None] = mapped_column(Text, nullable=True)  # Eg: "high-protein,no-pork"
    nutrition_source: Mapped[str] = mapped_column(String(255))
    price_source: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default='true')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # Unique=true for name_vi and is_active satisfied the standard (AC4 & AC5) of US-AD03
    # Ensures that re-importing the sample data file does not result in duplicates
    # Preserves the historical integrity of users' existing menus even when an administrator deletes or hides an item.

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint("role IN ('member','admin')", name='users_role_valid'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default='member', nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions: Mapped[list["Session"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    measurements: Mapped[list["Measurement"]] = relationship(back_populates="user")

class Profile(Base):
    __tablename__ = 'profiles'
    __table_args__ = (
        CheckConstraint(
            'age_years IS NULL OR (age_years >= 19 AND age_years <= 78)',
            name='profiles_age_range',
        ),
        CheckConstraint(
            "sex_for_equation IS NULL OR sex_for_equation IN ('male','female')",
            name='profiles_sex_valid',
        ),
        CheckConstraint(
            "activity_level IS NULL OR activity_level IN "
            "('sedentary','lightly_active','moderately_active','active','very_active')",
            name='profiles_activity_valid',
        ),
    )
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    age_years: Mapped[int | None] = mapped_column(nullable=True)
    sex_for_equation: Mapped[str | None] = mapped_column(String(10), nullable=True) # 'male' or 'female'
    activity_level: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="profile")

class Session(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        CheckConstraint('expires_at > created_at', name='sessions_expiry_after_created'),
        CheckConstraint(
            'revoked_at IS NULL OR revoked_at >= created_at',
            name='sessions_revoked_after_created',
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="sessions")