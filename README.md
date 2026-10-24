# Payment Status Checker

A student mini-project prototype: a Python REST API that looks up simulated payment statuses in PostgreSQL. It is containerized with Docker Compose and intended for later AWS deployment.

## Local run (Mac)

1. Install Docker Desktop and start it.
2. Open Terminal and change into this project folder.
3. Run:

   ```bash
   docker compose up --build
   ```

4. Test these URLs in a browser:

   - `http://localhost:5000/`
   - `http://localhost:5000/health`
   - `http://localhost:5000/payments/PAY1001`
   - `http://localhost:5000/payments/PAY1002`
   - `http://localhost:5000/payments/PAY1003`
   - `http://localhost:5000/payments/NO-SUCH-ID` (expected 404)

5. Stop the project with `Ctrl+C`, then run `docker compose down`.
   Data is stored in a named Docker volume. To remove the database data too, use `docker compose down -v`.

## Important

- The included records are mock/sample data only, not real payment transactions.
- This is a learning prototype, not a production banking service.
- Do not publish the sample database password or use it in AWS. For deployment, configure secrets securely.
- Availability, latency, SLA, TTR, and recovery values must be measured in actual tests; do not report target values as observed results.
