# Deploy di produzione — Jobson Academy

Stack: MariaDB 10.11 + Redis 7 + Frappe bench + Caddy 2 (HTTPS automatico via Let's Encrypt).

Pensato per **uso interno aziendale / piccole comunità di utenti** (5-100 utenti). Per scalare oltre serve una configurazione con `frappe_docker` ufficiale (worker separati, gunicorn production).

## Requisiti

- VPS Linux con Docker + Docker Compose (es. Hetzner CX23, ≥ 4 GB RAM)
- Un dominio/sottodominio (es. `learn.jobsonai.com`) con record **A** che punta all'IP del server
- Porte **80** e **443** raggiungibili pubblicamente (Caddy ne ha bisogno per Let's Encrypt)

## Setup (sul server, via SSH)

```bash
# 1. Clona il repo nella directory dei progetti
cd /opt
git clone https://github.com/icaroholding/jobson-lms.git jobson-academy
cd jobson-academy/deploy

# 2. Copia e compila il file .env con i tuoi valori
cp .env.example .env
nano .env   # ← imposta DOMAIN, LETSENCRYPT_EMAIL, password random

# 3. Avvia lo stack (il primo avvio impiega ~10 minuti per scaricare e buildare)
docker compose -f docker-compose.prod.yml up -d

# 4. Segui i log dell'inizializzazione
docker compose -f docker-compose.prod.yml logs -f frappe
```

Quando nei log del container `frappe` vedi `Setup completato. Avvio bench...` seguito dalle righe di `honcho` con i vari servizi attivi (web, socketio, scheduler, worker_*), il sito è pronto.

Vai su `https://<DOMAIN>` e fai login con:

- Utente: `Administrator`
- Password: quella che hai messo in `ADMIN_PASSWORD` nel `.env`

## Configurazione post-deploy

Dopo il primo login su `https://<DOMAIN>/app`:

1. **Email/SMTP** → `/app/email-account` → crea un nuovo Email Account con `enable_outgoing = 1` e `default_outgoing = 1`.
2. **LMS Settings** → `/app/lms-settings` → disabilita `Allow Guest Access`, abilita `Disable Signup`.
3. **Website Settings** → `/app/website-settings` → imposta `home_page = login`.
4. **Creazione utenti** → `/app/user` → "New" → flag "Send Welcome Email" per ogni utente.

## Comandi utili

```bash
# Stato dei container
docker compose -f docker-compose.prod.yml ps

# Log live di tutti i servizi
docker compose -f docker-compose.prod.yml logs -f

# Log solo del Frappe / solo di Caddy
docker compose -f docker-compose.prod.yml logs -f frappe
docker compose -f docker-compose.prod.yml logs -f caddy

# Riavviare tutto
docker compose -f docker-compose.prod.yml restart

# Entrare nel container frappe (per comandi bench manuali)
docker compose -f docker-compose.prod.yml exec frappe bash
# Una volta dentro:
cd /home/frappe/frappe-bench
bench --site learn.jobsonai.com <comando>

# Fermare tutto (dati preservati nei volumi)
docker compose -f docker-compose.prod.yml down

# Fermare tutto E CANCELLARE I DATI (attenzione!)
docker compose -f docker-compose.prod.yml down -v
```

## Backup

Backup database + sito su disco del server:

```bash
docker compose -f docker-compose.prod.yml exec frappe bash -c \
  "cd /home/frappe/frappe-bench && bench --site \$SITE_NAME backup --with-files"
```

I file finiscono in `/home/frappe/frappe-bench/sites/<site>/private/backups/` dentro il volume Docker `frappe-bench`.

Per un backup automatico giornaliero, crea un cron sul VPS:

```bash
# /etc/cron.d/jobson-academy-backup
0 3 * * * root cd /opt/jobson-academy/deploy && docker compose -f docker-compose.prod.yml exec -T frappe bash -c "cd /home/frappe/frappe-bench && bench --site \$SITE_NAME backup --with-files" > /var/log/jobson-backup.log 2>&1
```

## Aggiornamenti

```bash
# Aggiorna i file di deploy dal repo
cd /opt/jobson-academy
git pull

# Aggiorna l'app LMS dentro il bench
cd deploy
docker compose -f docker-compose.prod.yml exec frappe bash -c \
  "cd /home/frappe/frappe-bench && bench update --pull --no-backup --reset"
```

## Troubleshooting

### Caddy non ottiene il certificato HTTPS
- Verifica che DNS `A` sia propagato: `dig <DOMAIN> +short` deve rispondere l'IP del server
- Verifica porte aperte: `ss -tlnp | grep -E ':80|:443'`
- Caddy log: `docker compose -f docker-compose.prod.yml logs caddy`

### Frappe non parte
- Primo avvio richiede ~10 min (download bench, npm install, migrations)
- Se si blocca: `docker compose -f docker-compose.prod.yml logs frappe | tail -100`
- Per ripartire da zero: `docker compose -f docker-compose.prod.yml down -v` e rilancia il setup

### Email non arrivano
- Verifica SMTP in `/app/email-account`: test con "Send Test Email"
- Alcuni provider VPS (Hetzner, DigitalOcean) **bloccano la porta 25 in uscita** per anti-spam → usa un SMTP relay (Brevo, SendGrid, Resend) sulla porta 587 TLS
