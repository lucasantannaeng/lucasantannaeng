# BLAST Protocol - Task Plan

## 6 Fronts of Compliance

### Risco 1 — Verificação de Idade no Cadastro (ECA Digital & LGPD Art. 14)
- [ ] Audit all projects for user registration/auth flows.
- [ ] Implement date of birth collection with age calculation.
- [ ] Block under 18 without parental consent (13-17 with verifiable consent).
- [ ] Add unit tests for edge cases.

### Risco 2 — Fontes Self-Hosted (LGPD / Transferência Internacional de IP)
- [ ] Identify external Google Fonts links.
- [ ] Download woff2 files locally.
- [ ] Replace with @font-face rules.
- [ ] Verify build succeeds.

### Risco 3 — Telemetria & Gravação de Sessão (LGPD Art. 7 e 18)
- [ ] Detect telemetry SDKs (PostHog, Hotjar, Clarity, LogRocket).
- [ ] Enforce maskAllInputs: true and blockClass.
- [ ] Ensure SDK loads only after explicit opt-in.
- [ ] Add consent banner integration.

### Risco 4 — Compliance em E-mails de Marketing (CDC, Marco Civil e LGPD)
- [ ] Create standardized email footer component.
- [ ] Include 1-click unsubscribe, CNPJ, Razão Social, endereço físico.
- [ ] Replace all marketing email templates.

### Risco 5 — Transparência em Assinaturas Recorrentes (CDC Art. 31, 49 e Dec. 7.962/2013)
- [ ] Front: display price, periodicity, renewal/cancellation policy near CTA.
- [ ] Backend: idempotent job for pre-renewal notification (7 days).
- [ ] Handle timezone, prevent duplicate sends.

### Risco 6 — Canal de Denúncia de Direitos Autorais & Notice-and-Takedown (Marco Civil Art. 19/20 e LDA 9.610/98)
- [ ] Public page /copyright-report with form (URL, titularity, proof, contact).
- [ ] Backend quarantine pipeline with immutable audit log.
- [ ] Immediate content quarantine upon formal notice.
