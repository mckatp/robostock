#!/bin/bash
# =============================================================================
# RoboStock – PostgreSQL Backup Script
# Runs daily via cron. Creates a compressed, timestamped dump and removes
# backups older than RETENTION_DAYS.
# =============================================================================

set -euo pipefail

# ── Configuration ─────────────────────────────────────────────────────────────
DB_NAME="robostock_db"
DB_USER="murshid_robostock"
DB_HOST="127.0.0.1"
DB_PORT="5432"
BACKUP_DIR="/home/user/robostock/backups"
RETENTION_DAYS=7
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"
LOG_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S')]"

# ── Run backup ─────────────────────────────────────────────────────────────────
echo "${LOG_PREFIX} Starting backup → ${BACKUP_FILE}"

pg_dump \
    --host="${DB_HOST}" \
    --port="${DB_PORT}" \
    --username="${DB_USER}" \
    --no-password \
    --format=plain \
    "${DB_NAME}" \
  | gzip > "${BACKUP_FILE}"

# Verify the file was created and is non-empty
if [ -s "${BACKUP_FILE}" ]; then
    SIZE=$(du -sh "${BACKUP_FILE}" | cut -f1)
    echo "${LOG_PREFIX} Backup successful: ${BACKUP_FILE} (${SIZE})"
else
    echo "${LOG_PREFIX} ERROR: Backup file is empty or was not created!" >&2
    rm -f "${BACKUP_FILE}"
    exit 1
fi

# ── Retention: remove backups older than RETENTION_DAYS ───────────────────────
DELETED=$(find "${BACKUP_DIR}" -maxdepth 1 -name "${DB_NAME}_*.sql.gz" \
          -mtime "+${RETENTION_DAYS}" -print -delete | wc -l)

if [ "${DELETED}" -gt 0 ]; then
    echo "${LOG_PREFIX} Pruned ${DELETED} backup(s) older than ${RETENTION_DAYS} days."
fi

echo "${LOG_PREFIX} Done."
