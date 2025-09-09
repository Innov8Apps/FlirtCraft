"""Add skill_goals and birth_date for premium onboarding

Revision ID: 003
Revises: 002
Create Date: 2025-09-07 11:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add birth_date to users table
    op.add_column('users', sa.Column('birth_date', sa.Date(), nullable=True))
    
    # Add skill_goals to user_profiles table
    op.add_column('user_profiles', sa.Column('skill_goals', postgresql.ARRAY(sa.String()), nullable=False, server_default='{}'))


def downgrade() -> None:
    # Remove skill_goals from user_profiles table
    op.drop_column('user_profiles', 'skill_goals')
    
    # Remove birth_date from users table
    op.drop_column('users', 'birth_date')