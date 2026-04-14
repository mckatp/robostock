#!/bin/bash
# =============================================================================
# RoboStock – PostgreSQL Restore Script
# Usage: ./restore_db.sh <backup_file.sql.gz>
# Example: ./restore_db.sh robostock_db_2026-03-09_02-00.sql.gz
#
# WARNING: This will DROP and recreate the database. All current data will be
#          replaced with the contents of the backup file.
# =============================================================================

set -euo pipefail

# ── Configuration ─────────────────────────────────────────────────────────────
DB_NAME="robostock_db"
DB_USER="murshid_robostock"
DB_HOST="127.0.0.1"
DB_PORT="5432"
BACKUP_DIR="/home/user/robostock/backups"

# ── Argument check ─────────────────────────────────────────────────────────────
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <backup_file>"
    echo ""
    echo "Available backups:"
    ls -1t "${BACKUP_DIR}"/*.sql.gz "${BACKUP_DIR}"/*.dump 2>/dev/null || echo "  (none found)"
    exit 1
fi

BACKUP_FILE="$1"

# If only filename given (no path), look inside BACKUP_DIR
if [ ! -f "${BACKUP_FILE}" ]; then
    BACKUP_FILE="${BACKUP_DIR}/${1}"
fi

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "ERROR: Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

# ── Safety confirmation ────────────────────────────────────────────────────────
echo "============================================================"
echo "  DATABASE RESTORE – RoboStock"
echo "============================================================"
echo "  Database : ${DB_NAME}"
echo "  Host     : ${DB_HOST}:${DB_PORT}"
echo "  Restoring: ${BACKUP_FILE}"
echo "============================================================"
echo ""
echo "WARNING: This will DESTROY all current data in '${DB_NAME}'"
echo "         and replace it with the contents of the backup."
echo ""
read -r -p "Type 'yes' to confirm: " CONFIRM
if [ "${CONFIRM}" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

# ── Load Credentials from .env ────────────────────────────────────────────────
if [ -f "/home/user/robostock/.env" ]; then
    # Simple grep/sed to get values without needing a full env parser
    DB_PASSWORD=$(grep "^DB_PASSWORD=" /home/user/robostock/.env | cut -d'=' -f2 | tr -d "'\"")
    export PGPASSWORD="${DB_PASSWORD}"
fi

echo ""
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting restore..."

# ── Stop gunicorn to prevent DB connections during restore ────────────────────
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stopping robostock service..."
sudo systemctl stop robostock || true

# ── Drop and recreate the database ────────────────────────────────────────────
# We use sudo -u postgres to leverage peer authentication on the local socket.
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Dropping and recreating database as superuser..."
sudo -u postgres psql --command="DROP DATABASE IF EXISTS ${DB_NAME};"
sudo -u postgres psql --command="CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

# ── Restore ────────────────────────────────────────────────────────────────────
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restoring from backup..."

if [[ "${BACKUP_FILE}" == *.dump ]]; then
    # Custom format dump
    pg_restore \
        --host="${DB_HOST}" \
        --port="${DB_PORT}" \
        --username="${DB_USER}" \
        --dbname="${DB_NAME}" \
        --clean --if-exists \
        --no-owner --no-privileges \
        "${BACKUP_FILE}"
elif [[ "${BACKUP_FILE}" == *.sql.gz ]]; then
    # Gzip'd SQL format
    gunzip -c "${BACKUP_FILE}" | psql \
        --host="${DB_HOST}" \
        --port="${DB_PORT}" \
        --username="${DB_USER}" \
        --dbname="${DB_NAME}" \
        --quiet
else
    echo "ERROR: Unsupported backup format. Use .dump or .sql.gz"
    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restore complete."

# ── Restart gunicorn ──────────────────────────────────────────────────────────
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restarting robostock service..."
sudo systemctl start robostock

echo ""
echo "============================================================"
echo "  Restore finished successfully! ✓"
echo "============================================================"
