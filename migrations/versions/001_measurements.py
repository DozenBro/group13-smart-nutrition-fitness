from alembic import op
import sqlalchemy as sa

revision = '001_measurements'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'measurements',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('weight_kg', sa.Numeric(5, 2), nullable=False),
        sa.Column('height_cm', sa.Numeric(5, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint('weight_kg > 0 AND weight_kg <= 500', name='weight_range'),
        sa.CheckConstraint('height_cm >= 50 AND height_cm <= 250', name='height_range'),
    )


def downgrade():
    op.drop_table('measurements')

