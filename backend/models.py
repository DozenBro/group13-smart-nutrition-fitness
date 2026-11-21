from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Measurement(Base):
    __tablename__ = 'measurements'
    __table_args__ = (
        CheckConstraint('weight_kg > 0 AND weight_kg <= 500', name='weight_range'),
        CheckConstraint('height_cm >= 50 AND height_cm <= 250', name='height_range'),
    )

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
