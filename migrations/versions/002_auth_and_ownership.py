from alembic import op
import sqlalchemy as sa

revision = '002_auth_and_ownership'
down_revision = '64cae5288649'
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False, server_default='member'),
        sa.Column('is_locked', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("role IN ('member','admin')", name='users_role_valid'),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create profiles table
    op.create_table(
        'profiles',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('age_years', sa.Integer(), nullable=True),
        sa.Column('sex_for_equation', sa.String(10), nullable=True),
        sa.Column('activity_level', sa.String(30), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            'age_years IS NULL OR (age_years >= 19 AND age_years <= 78)',
            name='profiles_age_range',
        ),
        sa.CheckConstraint(
            "sex_for_equation IS NULL OR sex_for_equation IN ('male','female')",
            name='profiles_sex_valid',
        ),
        sa.CheckConstraint(
            "activity_level IS NULL OR activity_level IN "
            "('sedentary','lightly_active','moderately_active','active','very_active')",
            name='profiles_activity_valid',
        ),
    )

    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('token_hash', sa.String(64), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('expires_at > created_at', name='sessions_expiry_after_created'),
        sa.CheckConstraint(
            'revoked_at IS NULL OR revoked_at >= created_at',
            name='sessions_revoked_after_created',
        ),
    )
    op.create_index('ix_sessions_user_id', 'sessions', ['user_id'], unique=False)
    op.create_index('ix_sessions_token_hash', 'sessions', ['token_hash'], unique=True)

    # Add user_id to measurements as nullable so existing rows can be backfilled
    op.add_column('measurements', sa.Column('user_id', sa.Integer(), nullable=True))

    # Create the Demo User that will own the existing fictional measurements
    op.execute("""
        INSERT INTO users (email, password_hash, role, is_locked)
        VALUES ('demo@example.com', 'placeholder_hash_for_demo', 'member', false)
        ON CONFLICT (email) DO NOTHING;
    """)

    # Assign all existing ownerless measurements to the Demo User
    op.execute("""
        UPDATE measurements
        SET user_id = (SELECT id FROM users WHERE email = 'demo@example.com')
        WHERE user_id IS NULL;
    """)

    # Enforce NOT NULL and add the foreign key now that every row has an owner
    op.alter_column('measurements', 'user_id', nullable=False)
    op.create_foreign_key('fk_measurements_user_id', 'measurements', 'users', ['user_id'], ['id'])

    # History index proposed by the Sprint 1 ERD
    op.create_index(
        'ix_measurements_user_created',
        'measurements',
        ['user_id', sa.text('created_at DESC'), sa.text('id DESC')],
        unique=False,
    )


def downgrade():
    op.drop_index('ix_measurements_user_created', table_name='measurements')
    op.drop_constraint('fk_measurements_user_id', 'measurements', type_='foreignkey')
    op.drop_column('measurements', 'user_id')

    op.drop_index('ix_sessions_token_hash', table_name='sessions')
    op.drop_index('ix_sessions_user_id', table_name='sessions')
    op.drop_table('sessions')
    op.drop_table('profiles')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')