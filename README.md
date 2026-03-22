# API Shield

PII sanitization middleware for AI-integrated services.

When your application forwards user input to an external AI provider, sensitive data such as names, IDs, phone numbers, and emails leaves your infrastructure. API Shield intercepts that data before it's sent, strips the PII, and returns clean text — with no changes to your existing flow.

```
your service  →  API Shield  →  ChatGPT / Claude / Gemini
                 (sanitize)
```

Deploys as an independent microservice in your existing K8s cluster. No infrastructure changes required.

---

## Sanitization layers

**Layer 1 — Regex** (Spring Boot)
Deterministic, sub-millisecond detection of structured PII: Israeli IDs, credit cards, phone numbers, emails.

**Layer 2 — NLP** (Presidio + spaCy)
Statistical model for unstructured PII: names, locations, organizations, dates.

---

## Deploy

```bash
git clone https://github.com/harels12/api-shield
cd api-shield
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

```bash
kubectl get service spring-service -n api-shield
```

---

## Usage

Replace your AI calls with a sanitization step:

```
GET /clean?text=<input>
```

Detect without sanitizing:
```
GET /detect?text=<input>
```

#### Example — sanitize before sending to OpenAI

```python
# before
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": user_message}],
)

# after
sanitized = requests.get("http://api-shield.internal/clean", params={"text": user_message}).text
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": sanitized}],
)

# "I'm John Smith, ID 123456782" → "I'm [PERSON], ID [ISRAELI_ID]"
```

---

## Stack

- **Spring Boot 4** — REST API, regex detection, WebFlux HTTP client
- **FastAPI** — Python service
- **Presidio + spaCy** — NLP entity recognition
- **Docker** — multi-stage builds
- **Kubernetes** — independent scaling, resource limits, internal DNS
- **GitHub Actions** — image build and push on every commit to main
