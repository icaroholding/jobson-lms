#!/bin/bash
# Script di inizializzazione del bench Frappe in produzione.
# Eseguito dentro il container `frappe` del docker-compose.prod.yml.
# È idempotente: se il bench esiste già, fa solo `bench start`.

set -eo pipefail

: "${SITE_NAME:?SITE_NAME non impostata}"
: "${DB_ROOT_PASSWORD:?DB_ROOT_PASSWORD non impostata}"
: "${ADMIN_PASSWORD:?ADMIN_PASSWORD non impostata}"
: "${DOMAIN:?DOMAIN non impostata}"
LMS_REPO="${LMS_REPO:-https://github.com/icaroholding/jobson-lms}"
LMS_BRANCH="${LMS_BRANCH:-develop}"

export PATH="${NVM_DIR}/versions/node/v${NODE_VERSION_DEVELOP}/bin/:${PATH}"

cd /home/frappe

if [ -d "frappe-bench/apps/frappe" ]; then
  echo "✅ Bench già inizializzato — avvio servizi..."
  cd frappe-bench
  exec bench start
fi

echo "🚀 Inizializzo un nuovo bench (Frappe v15)..."
bench init --skip-redis-config-generation --frappe-branch version-15 frappe-bench
cd frappe-bench

echo "🔗 Collego i servizi Docker..."
bench set-mariadb-host mariadb
bench set-redis-cache-host redis://redis:6379
bench set-redis-queue-host redis://redis:6379
bench set-redis-socketio-host redis://redis:6379

# Rimuovi redis e watch dal Procfile (usiamo i container esterni)
sed -i '/redis/d' ./Procfile
sed -i '/watch/d' ./Procfile

echo "📦 Scarico Jobson Academy da ${LMS_REPO} (branch ${LMS_BRANCH})..."
bench get-app --branch "$LMS_BRANCH" lms "$LMS_REPO"

echo "🏗️  Creo il site $SITE_NAME..."
bench new-site "$SITE_NAME" \
  --mariadb-root-password "$DB_ROOT_PASSWORD" \
  --admin-password "$ADMIN_PASSWORD" \
  --no-mariadb-socket

echo "🎓 Installo l'app lms sul site..."
bench --site "$SITE_NAME" install-app lms

echo "⚙️  Configurazione produzione..."
bench --site "$SITE_NAME" set-config developer_mode 0
bench --site "$SITE_NAME" set-config host_name "https://$DOMAIN"
bench --site "$SITE_NAME" clear-cache
bench use "$SITE_NAME"

echo "✅ Setup completato. Avvio bench..."
exec bench start
