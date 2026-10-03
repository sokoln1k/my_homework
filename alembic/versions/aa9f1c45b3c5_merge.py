"""merge

Revision ID: aa9f1c45b3c5
Revises: 4bec28cb6fce, c5c33560bf82
Create Date: 2026-09-03 12:32:42.847793

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aa9f1c45b3c5"
down_revision: Union[str, Sequence[str], None] = ("4bec28cb6fce", "c5c33560bf82")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
