"""Implement full Standup Automation engine

Revision ID: dd8382861925
Revises: e000357afba3
Create Date: 2026-02-17 03:04:16.054929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dd8382861925'
down_revision: Union[str, Sequence[str], None] = 'e000357afba3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create enum type manually
    session_status = postgresql.ENUM('ACTIVE', 'CLOSED', name='sessionstatus')
    session_status.create(op.get_bind())

    op.add_column('standup_configs', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.drop_column('standup_configs', 'schedule')
    op.drop_constraint(op.f('standup_responses_config_id_fkey'), 'standup_responses', type_='foreignkey')
    op.drop_column('standup_responses', 'content')
    op.drop_column('standup_responses', 'config_id')
    op.drop_column('standup_responses', 'date')
    op.add_column('standup_sessions', sa.Column('project_id', sa.UUID(), nullable=True))
    op.add_column('standup_sessions', sa.Column('started_at', sa.DateTime(), nullable=True))
    op.add_column('standup_sessions', sa.Column('ends_at', sa.DateTime(), nullable=True))
    
    # Use explicit USING cast for PostgreSQL
    op.alter_column('standup_sessions', 'status',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('ACTIVE', 'CLOSED', name='sessionstatus'),
               existing_nullable=True,
               postgresql_using='status::sessionstatus')
               
    op.create_foreign_key(None, 'standup_sessions', 'projects', ['project_id'], ['id'])
    op.drop_column('standup_sessions', 'closes_at')
    op.drop_column('standup_sessions', 'date')
    op.add_column('standup_summaries', sa.Column('summary_text', sa.Text(), nullable=True))
    op.add_column('standup_summaries', sa.Column('blockers_json', sa.JSON(), nullable=True))
    op.drop_constraint(op.f('standup_summaries_config_id_fkey'), 'standup_summaries', type_='foreignkey')
    op.drop_column('standup_summaries', 'config_id')
    op.drop_column('standup_summaries', 'date')
    op.drop_column('standup_summaries', 'summary_content')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('standup_summaries', sa.Column('summary_content', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('standup_summaries', sa.Column('date', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('standup_summaries', sa.Column('config_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key(op.f('standup_summaries_config_id_fkey'), 'standup_summaries', 'standup_configs', ['config_id'], ['id'])
    op.drop_column('standup_summaries', 'blockers_json')
    # ... rest of downgrade ...
    op.drop_column('standup_summaries', 'summary_text')
    op.add_column('standup_sessions', sa.Column('date', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('standup_sessions', sa.Column('closes_at', sa.DateTime(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'standup_sessions', type_='foreignkey')
    op.alter_column('standup_sessions', 'status',
               existing_type=sa.Enum('ACTIVE', 'CLOSED', name='sessionstatus'),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.drop_column('standup_sessions', 'ends_at')
    op.drop_column('standup_sessions', 'started_at')
    op.drop_column('standup_sessions', 'project_id')
    op.add_column('standup_responses', sa.Column('date', sa.DATE(), autoincrement=False, nullable=True))
    # ... rest of downgrade ...
    op.add_column('standup_responses', sa.Column('config_id', sa.UUID(), autoincrement=False, nullable=True))
    op.add_column('standup_responses', sa.Column('content', sa.JSON(), autoincrement=False, nullable=True))
    op.create_foreign_key(op.f('standup_responses_config_id_fkey'), 'standup_responses', 'standup_configs', ['config_id'], ['id'])
    op.add_column('standup_configs', sa.Column('schedule', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('standup_configs', 'is_active')

    # Drop enum type manually
    session_status = postgresql.ENUM('ACTIVE', 'CLOSED', name='sessionstatus')
    session_status.drop(op.get_bind())
