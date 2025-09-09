"""Update onboarding for 5-screen flow

Revision ID: 002
Revises: 001
Create Date: 2025-09-07 01:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Update the onboarding_sessions table to reflect the 5-screen streamlined flow.
    Changes the default total_steps from 12 to 5.
    """
    # Update default value for total_steps column
    op.execute("ALTER TABLE onboarding_sessions ALTER COLUMN total_steps SET DEFAULT 5")
    
    # Update existing sessions that haven't been completed to use the new step count
    # Only update sessions that are still at the default 12 steps and not completed
    op.execute("""
        UPDATE onboarding_sessions 
        SET total_steps = 5 
        WHERE total_steps = 12 
        AND is_completed = false
    """)
    
    # Add comment to the column explaining the 5-screen flow
    op.execute("""
        COMMENT ON COLUMN onboarding_sessions.total_steps IS 
        '5-Screen Streamlined Flow: Welcome, Age Verification, Registration, Preferences, Skill Goals'
    """)


def downgrade() -> None:
    """
    Revert the changes to the onboarding_sessions table.
    """
    # Revert default value for total_steps column
    op.execute("ALTER TABLE onboarding_sessions ALTER COLUMN total_steps SET DEFAULT 12")
    
    # Update sessions back to 12 steps if they were at 5 and not completed
    op.execute("""
        UPDATE onboarding_sessions 
        SET total_steps = 12 
        WHERE total_steps = 5 
        AND is_completed = false
    """)
    
    # Remove the comment
    op.execute("COMMENT ON COLUMN onboarding_sessions.total_steps IS NULL")