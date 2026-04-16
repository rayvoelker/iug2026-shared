# Sierra SSO Technical Implementation Guide

A deep-dive companion to the [Sierra Staff and Single Sign-On session notes](../../iug2026-private/sessions/wednesday-apr15-sierra-sso.md) from IUG 2026. Aimed at library systems administrators considering or actively implementing SAML SSO for Sierra staff authentication.

---

## Table of Contents

1. [SAML 2.0 Protocol Fundamentals](#1-saml-20-protocol-fundamentals)
2. [Setting Up Your Identity Provider](#2-setting-up-your-identity-provider)
3. [Sierra-Specific Configuration](#3-sierra-specific-configuration)
4. [Keycloak and the Future of Innovative Identity](#4-keycloak-and-the-future-of-innovative-identity)
5. [SCIM and Automated User Provisioning](#5-scim-and-automated-user-provisioning)
6. [MFA Deep Dive](#6-mfa-deep-dive)
7. [Passwordless Authentication (FIDO2/WebAuthn)](#7-passwordless-authentication-fido2webauthn)
8. [Conditional Access — Skip MFA on Trusted Networks](#8-conditional-access--skip-mfa-on-trusted-networks)
9. [SAML Debugging and Troubleshooting](#9-saml-debugging-and-troubleshooting)
10. [Links and References](#10-links-and-references)

---

## 1. SAML 2.0 Protocol Fundamentals

### What's Actually Happening

SAML (Security Assertion Markup Language) is an XML-based standard for exchanging authentication data between two parties:

- **Identity Provider (IdP)** — the system that knows who your users are (Azure AD, Google, Shibboleth, Okta)
- **Service Provider (SP)** — the application that needs to verify identity (Sierra)

Sierra acts as the **SP**. Your organization's directory service acts as the **IdP**.

### The Login Flow (SP-Initiated — What Sierra Uses)

```
Staff member                Sierra (SP)                Your IdP
    |                           |                         |
    |-- launches Sierra ------->|                         |
    |                           |-- AuthnRequest -------->|
    |                           |   (base64-encoded XML)  |
    |                           |                         |
    |<------------- redirect to IdP login page -----------|
    |                                                     |
    |-- enters credentials + MFA ----------------------->|
    |                                                     |
    |                           |<-- SAML Response -------|
    |                           |   (signed XML assertion)|
    |                           |                         |
    |                           |-- validates signature   |
    |                           |-- extracts SSO ID       |
    |                           |-- matches to staff acct |
    |                           |                         |
    |<-- logged in -------------|                         |
```

The key thing: **Sierra never sees the user's password.** It only receives a signed assertion from your IdP saying "this person authenticated successfully, and their username/email/uid is X."

### IdP-Initiated Flow

User starts at the IdP portal (Azure MyApps, Google apps launcher, Okta dashboard) and clicks a Sierra tile. The IdP generates a SAML Response directly without a preceding AuthnRequest. This works but is less secure — there's no request-response correlation, making replay attacks easier. SP-initiated (what Sierra does) is preferred.

### Metadata Exchange

Before SSO works, the SP and IdP need to exchange metadata — XML documents describing each party's configuration:

**SP Metadata (Sierra provides this):**
- `entityID` — Sierra's unique identifier (a URL)
- `AssertionConsumerService` — the ACS URL where the IdP sends responses
- SP's X.509 certificate (for optional request signing)

**IdP Metadata (your IdP provides this):**
- `entityID` — your IdP's unique identifier
- `SingleSignOnService` — the URL Sierra sends AuthnRequests to
- IdP's X.509 signing certificate (Sierra uses this to verify assertions are genuine)

In Sierra's admin interface, you paste in your IdP's metadata URL. Sierra generates its own SP metadata URL that you give to your IdP admin.

### What's Inside a SAML Assertion

The signed XML assertion the IdP sends back contains:

```xml
<saml:Assertion>
  <saml:Issuer>https://idp.yourlibrary.org</saml:Issuer>
  <ds:Signature>...</ds:Signature>

  <saml:Subject>
    <saml:NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress">
      jsmith@library.org
    </saml:NameID>
    <saml:SubjectConfirmation>
      <saml:SubjectConfirmationData
        Recipient="https://sierra.library.org/saml/acs"
        NotOnOrAfter="2026-04-15T14:35:00Z"/>
    </saml:SubjectConfirmation>
  </saml:Subject>

  <saml:Conditions NotBefore="2026-04-15T14:29:00Z"
                   NotOnOrAfter="2026-04-15T14:35:00Z">
    <saml:AudienceRestriction>
      <saml:Audience>https://sierra.library.org/saml/metadata</saml:Audience>
    </saml:AudienceRestriction>
  </saml:Conditions>

  <saml:AttributeStatement>
    <saml:Attribute Name="uid">
      <saml:AttributeValue>jsmith</saml:AttributeValue>
    </saml:Attribute>
    <saml:Attribute Name="email">
      <saml:AttributeValue>jsmith@library.org</saml:AttributeValue>
    </saml:Attribute>
  </saml:AttributeStatement>
</saml:Assertion>
```

The critical parts:
- **Issuer** — must match the IdP entityID Sierra expects
- **Signature** — proves the assertion is genuine and untampered
- **Subject/NameID** — the user's identity
- **Conditions** — time window the assertion is valid (typically 5 minutes)
- **AudienceRestriction** — must match Sierra's entityID
- **AttributeStatement** — the attribute Sierra matches against the SSO ID field (e.g., `uid`, `email`)

### NameID Formats

| Format | When to Use |
|--------|-------------|
| `emailAddress` | Most common; user's email as identifier |
| `persistent` | Opaque pairwise ID; good for privacy |
| `unspecified` | Let the IdP decide |

For Sierra, **emailAddress** or **unspecified** with a uid attribute is typical.

### Signing and Encryption

- **Response signing** (required): IdP signs the assertion with its private key. Sierra validates using the IdP's public certificate from metadata.
- **Request signing** (optional): Sierra signs its AuthnRequest so the IdP can verify legitimacy.
- **Assertion encryption** (optional): IdP encrypts the assertion with Sierra's public key. Adds PII protection beyond TLS.
- **Algorithm**: RSA-SHA256 is the current standard. SHA-1 is deprecated — do not use.

---

## 2. Setting Up Your Identity Provider

### Google Workspace

Available on all paid editions (Business, Education, Nonprofits).

**Steps:**

1. Sign in to [admin.google.com](https://admin.google.com)
2. Navigate to **Apps > Web and mobile apps**
3. Click **Add app > Add custom SAML app**
4. Enter app name (e.g., "Sierra ILS"), optionally upload an icon
5. **Google IdP Information page** — download or copy:
   - SSO URL: `https://accounts.google.com/o/saml2/idp?idpid=<your_id>`
   - Entity ID: `https://accounts.google.com/o/saml2?idpid=<your_id>`
   - Certificate (download the PEM file)
   - Or download the full IdP metadata XML
6. **Service Provider Details** — enter values from Sierra's SAML config:
   - ACS URL (from Sierra's SP metadata)
   - Entity ID (from Sierra's SP metadata)
   - Name ID format: `EMAIL` (or `PERSISTENT`)
   - Name ID: Primary email
   - Check "Signed response" if Sierra requires it
7. **Attribute mapping** — add the attribute Sierra expects:
   - e.g., `uid` → Basic Information > Primary email (or Username)
8. Click **Finish**
9. **Enable for users**: By default the app is OFF. Select your staff OU and set to **ON**
10. Allow up to 24 hours for propagation (usually much faster)

**Gotcha for free nonprofit tier**: No bulk YubiKey management — each key must be registered per-account manually in the admin console.

**Reference**: [Google — Set up custom SAML app](https://support.google.com/a/answer/6087519)

### Microsoft Entra ID (Azure AD)

1. Sign in to [entra.microsoft.com](https://entra.microsoft.com)
2. Navigate to **Identity > Applications > Enterprise applications**
3. Click **New application > Create your own application**
4. Name it "Sierra ILS", select "Integrate any other application"
5. Go to **Single sign-on > SAML**
6. **Basic SAML Configuration**:
   - Identifier (Entity ID): Sierra's entityID from SP metadata
   - Reply URL (ACS URL): Sierra's ACS URL from SP metadata
7. **Attributes & Claims**: Configure the attribute Sierra expects (e.g., `uid` mapped to `user.userprincipalname` or `user.mailnickname`)
8. **SAML Certificates**: Download the Federation Metadata XML (this is your IdP metadata to give to Sierra)
9. **Users and groups**: Assign staff users/groups to the application

**Reference**: [Microsoft — SAML SSO for apps](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso)

### Shibboleth

What RIT uses (as discussed in the session). Shibboleth is the standard in academic libraries.

- Shibboleth IdP is self-hosted (typically by your university's central IT)
- Configuration lives in XML files on the IdP server
- Your IdP admin adds Sierra as a relying party by importing Sierra's SP metadata
- Attribute release policies control which attributes the IdP sends to Sierra
- Often integrated with InCommon Federation for cross-institutional trust

**Reference**: [Shibboleth IdP Documentation](https://shibboleth.atlassian.net/wiki/spaces/IDP5/overview)

### Any SAML 2.0 IdP

Sierra supports **any SAML 2.0 compliant IdP**. The general process is always:

1. Get Sierra's SP metadata URL from Sierra Admin > SAML Configuration
2. Import that into your IdP
3. Get your IdP's metadata URL
4. Import that into Sierra's SAML Configuration
5. Configure the attribute mapping (what attribute = SSO ID)
6. Upload SSO IDs for staff (CSV or manual)
7. Test in test mode
8. Enable

---

## 3. Sierra-Specific Configuration

### Requirements

- Sierra **6.1+** (6.0 added staff SAML for Web/Admin only; 6.1 extended to Desktop and Web Management Reports)
- Permission **725 (SAML Administrator)** assigned to the configuring staff account
- Access to your IdP administrator

### Configuration Steps (Sierra Admin App)

**Back End Management > SAML Configuration:**

**Identity Providers tab > ADD:**

| Field | Description | Notes |
|-------|-------------|-------|
| Name | Unique identifier (min 3 chars) | Displayed on the login button. **Immutable once created.** |
| Usage | Patrons, Staff, or Both | Can have separate IdPs for patron vs. staff |
| Metadata URL | Your IdP's metadata endpoint | Must be HTTPS, min 12 chars |
| Attribute | IdP response attribute to match against SSO IDs | e.g., `uid`, `email`, `username` |
| Duration in Seconds | Session validity | Default 3600; align with IdP session settings |

**Upload SSO IDs tab:**

- CSV format: `username,sso_id` (header row ignored)
- `username` = Sierra login name (**case-sensitive**)
- `sso_id` = matching attribute from IdP (**case-sensitive**, must be unique)
- Errors block the entire upload — fix all errors before retrying
- Can also set SSO IDs individually per user in the staff record

**Management tab:**

- **ENABLE STAFF AUTH** (or ENABLE PATRON AUTH)
- Triggers automatic restart of CAS server and staff webapps — **plan for off-hours**
- After modifying IdP settings, manually restart CAS server via **RESTART CAS SERVER**

### Test Mode

You can configure and test SAML **without affecting production**. Set up the IdP, upload SSO IDs, and test the flow before clicking ENABLE. Justin Newcomer specifically mentioned this in the session: "It's self-service now. You can just go into the admin website and set it up yourself in test mode without interfering with production."

### SSO ID Management Tips (from the session)

- SSO IDs can be **changed live** — useful for testing (swap your SSO ID to a test account, login as that account, swap it back)
- When provisioning new users, adding the SSO ID is just part of the standard process
- For student employees: set a random legacy password they never receive; SSO is their only login path
- Clone permissions from similar accounts when onboarding: "Takes longer to close the ticket than to actually click 'copy from other supervisor'"

### What Still Requires Legacy Passwords

| Application | SSO Support | Workaround |
|-------------|-------------|------------|
| Sierra Desktop Client | Yes (6.1+) | — |
| Sierra Web | Yes (6.0+) | — |
| Admin App | Yes (6.0+) | — |
| Web Management Reports | Yes (6.1+) | — |
| Decision Center | **No** | Must have legacy password |
| Circa | **No** | Must have legacy password; Justin considering vibe-coding a replacement |
| Circulation overrides | **Legacy only** | Supervisor override pop-up uses legacy credentials |
| Innovative mobile worklists | **No** | On the roadmap (seen in a slide) |
| Vega mobile worklists | **No** | On the roadmap |

---

## 4. Keycloak and the Future of Innovative Identity

### What Is Keycloak

[Keycloak](https://www.keycloak.org/) is an open-source Identity and Access Management (IAM) server maintained by CNCF (formerly Red Hat). It provides:

- SSO and Single Sign-Out
- Identity brokering (act as intermediary between apps and upstream IdPs)
- User federation (LDAP/AD integration)
- Support for OIDC, OAuth 2.0, and SAML 2.0
- Fine-grained authorization
- Multi-tenancy via "realms"

### Why This Matters for Sierra/Polaris/Vega

At the SSO session, an attendee (appearing to be from Innovative's engineering side) mentioned:

> "The way that Vega runs currently is through Keycloak... they are planning on actually making Keycloak a shared service and then pushing it across to Polaris and Sierra. So when you put in your IdeaLab requests, if that pushed up, that'll show there's a lot of power... that'll get Keycloak down to Polaris, and it'll push it over to the Vega side, which is all under one single piece and not us all biking the happenings, little things into each module."

### What Keycloak as a Shared Service Would Mean

```
                        [Keycloak]
                       /     |     \
                      /      |      \
              [Sierra]  [Polaris]  [Vega]
                 SAML    OIDC      OIDC
```

**Identity Brokering** — Keycloak sits between your apps and your IdP:

```
[Sierra] <--SAML--> [Keycloak] <--OIDC--> [Azure AD]
                               <--SAML--> [Shibboleth]
                               <--OIDC--> [Google]
                               <--LDAP--> [Active Directory]
```

Benefits:
- **Protocol translation**: Sierra speaks SAML, but your IdP might prefer OIDC — Keycloak handles the conversion
- **One integration point**: Configure your IdP once in Keycloak; all Innovative products inherit it
- **Consistent login experience** across Sierra, Polaris, Vega
- **Easier "bring your own IdP"**: Keycloak's admin console makes adding new IdPs straightforward
- **Multi-tenancy**: Each library/consortium gets its own Keycloak "realm" in a hosted environment
- **Open source**: No per-user IAM licensing costs

### Key Keycloak Concepts

| Concept | What It Is |
|---------|------------|
| **Realm** | Isolated tenant — own users, groups, clients, IdPs. Think of it as a separate identity domain per library system. |
| **Client** | An application registered in Keycloak (Sierra would be a SAML client, Vega an OIDC client) |
| **Identity Broker** | Configuration to delegate auth to an external IdP (Azure AD, Google, Shibboleth, etc.) |
| **User Federation** | Direct connection to LDAP/AD — Keycloak queries the directory at login time |
| **Protocol Mappers** | Rules for which attributes/claims appear in tokens and assertions sent to clients |

**Reference**: [Keycloak Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/index.html)

---

## 5. SCIM and Automated User Provisioning

### The Problem

Right now, Sierra SSO ID management is manual:
- Upload a CSV of `username,sso_id` pairs
- Or set the SSO ID individually per staff record
- When someone leaves, manually remove their account
- No automatic group/permission mapping from your IdP

### What SCIM Would Solve

**SCIM (System for Cross-domain Identity Management)** is a REST API standard (RFC 7643/7644) for automatically syncing users and groups between your IdP and applications.

### How It Works

```
[HR System] --> [IdP (Azure/Okta/Google)] --> SCIM API --> [Sierra]
                                                           - Create user
                                                           - Set SSO ID
                                                           - Assign permissions
                                                           - Deactivate on departure
```

**The API model:**

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/Users` | `POST` | Create a new staff account |
| `/Users/{id}` | `GET` | Retrieve a staff account |
| `/Users/{id}` | `PATCH` | Update attributes (name change, department transfer) |
| `/Users/{id}` | `DELETE` | Deprovisioning (staff departure) |
| `/Groups` | `POST/PATCH` | Create/update permission groups |
| `/Groups/{id}` | `PATCH` | Add/remove members from groups |

**Example: New staff member provisioned automatically:**

```json
POST /Users
{
  "userName": "jsmith",
  "name": { "givenName": "Jane", "familyName": "Smith" },
  "emails": [{ "value": "jsmith@library.org", "primary": true }],
  "active": true,
  "groups": [{ "value": "circ-staff" }],
  "urn:sierra:ssoId": "jsmith@library.org"
}
```

### SCIM vs. CSV Upload

| | CSV Upload (current) | SCIM (aspirational) |
|---|---|---|
| **Timing** | Batch (manual trigger) | Real-time |
| **Deprovisioning** | Often forgotten | Automatic when user deactivated in IdP |
| **Group/permissions** | Managed separately in Sierra | Could map IdP groups to Sierra permissions |
| **Error handling** | Errors block entire upload | Per-record HTTP error responses |
| **Audit trail** | Spreadsheet-level | Full HTTP request/response logs |
| **Effort for 10 new hires** | ~30 min manual work | Zero — automatic |

### Current State

**Sierra does not support SCIM today.** This is aspirational — worth requesting via IdeaLab. If Keycloak becomes the shared identity layer, Keycloak does have SCIM support that could potentially bridge the gap.

**Which IdPs support SCIM as a client (pushing to apps):**
- Microsoft Entra ID — robust built-in SCIM provisioning
- Okta — robust SCIM 2.0 support
- Google Workspace — supports SCIM provisioning
- JumpCloud, OneLogin, Ping Identity — all support SCIM

---

## 6. MFA Deep Dive

### Why Regular Push MFA Is No Longer Enough

Standard push sends a simple "Approve / Deny" notification. This is vulnerable to **MFA fatigue (prompt bombing)**:

1. Attacker obtains stolen credentials (phishing, dark web)
2. Attacker repeatedly attempts login, triggering push after push
3. Victim taps "Approve" out of frustration, confusion, or at 2 AM half-asleep
4. Optionally, attacker calls victim posing as IT: "just approve the prompt"

**Real breaches from MFA fatigue:**

| Organization | Date | What Happened |
|---|---|---|
| Uber | Sep 2022 | Lapsus$ bombarded a contractor's phone + posed as IT via WhatsApp |
| Cisco | May 2022 | Voice phishing combined with push bombing; gained VPN access |
| Microsoft | Mar 2022 | Lapsus$ used MFA fatigue + session token replay; 37 GB source code stolen |

### Verified Push / Number Matching — The Fix

What RIT uses (Duo "Verified Push"). Microsoft calls it "number matching."

1. User enters credentials at login page
2. Login page displays a **two-digit number** (e.g., "37")
3. Push notification asks: "Enter the number shown on your sign-in screen: ___"
4. User must type "37" into the authenticator app
5. If correct, authentication succeeds

**Why it works**: The user must be actively looking at both the login screen AND their phone. An attacker triggering prompts from their own browser sees a different number — the victim has no number to enter, so there's nothing to mindlessly approve.

**Additional defenses to layer on top:**
- Show app name, location, device, and IP in the push notification
- Rate-limit MFA prompts (e.g., 3 per 5 minutes, then lockout)
- Let users report suspicious prompts from the notification itself
- Turn off SMS-based MFA (vulnerable to SIM swapping)

**Platform support:**

| Platform | Feature Name | Status |
|---|---|---|
| Microsoft Authenticator | Number matching | Mandatory for all tenants since May 2023 |
| Cisco Duo | Verified Duo Push | Available in Duo 4.x+; enable per policy |
| Okta Verify | Number Challenge | Configurable per policy |
| Google | Risk-based challenges | Similar protection via context, not explicit number matching |

### What RIT Does (from the session)

- Duo with **verified push** (type 3 numbers — "we're supposed to be thankful we only have to type 3")
- Disabled SMS MFA
- Disabled regular push
- Disabled phone-call-based MFA (switched to digital phones — can't MFA from the phone you're calling from)
- YubiKey for Duo web auth (self-enrollment)
- Don't support Duo offline codes ("don't want to deal with ingesting all those random seeds")

**References:**
- [CISA — Implement Number Matching in MFA](https://www.cisa.gov/sites/default/files/publications/fact-sheet-implement-number-matching-in-mfa-applications-508c.pdf)
- [MFA Fatigue Attacks — BeyondTrust](https://www.beyondtrust.com/resources/glossary/mfa-fatigue-attack)

---

## 7. Passwordless Authentication (FIDO2/WebAuthn)

This came up in the session discussion. Justin is interested but cautious.

### The Standards

- **FIDO2** = **WebAuthn** (W3C browser API) + **CTAP2** (how the browser talks to security keys over USB/NFC/BLE)
- **Passkeys** = the user-facing term for FIDO2 discoverable credentials

### How It Works

**Registration:**
1. User visits site, initiates passkey registration
2. Site sends a challenge to the browser
3. Browser invokes the authenticator (YubiKey or platform biometric)
4. Authenticator generates a **public/private key pair** bound to this site's origin
5. Private key **never leaves the device**
6. Public key is stored server-side

**Authentication:**
1. User visits site, initiates login
2. Site sends a challenge
3. User touches the YubiKey + enters the PIN (or uses biometric)
4. Authenticator signs the challenge with the private key
5. Site verifies the signature with the stored public key

**Why it's phishing-resistant**: The credential is bound to the **exact origin** (e.g., `https://sierra.library.org`). A phishing site at `https://sierra-library.evil.com` simply can't trigger the credential.

### Types of Authenticators

| Type | Examples | Pros | Cons |
|------|----------|------|------|
| **Hardware security keys** | YubiKey 5, Google Titan, Feitian | Strongest security; hardware-bound; no battery | Must carry it; costs $25-70/key; limited credential slots (25 on YubiKey 5) |
| **Platform authenticators** | Windows Hello, Touch ID, Face ID | Very convenient; built into device | Tied to one device |
| **Synced passkeys** | iCloud Keychain, Google Password Manager, 1Password | Sync across devices | Less secure than hardware-bound (cloud compromise risk) |

### The PIN Question

Justin's concern from the session: "If somebody didn't have a password and all they needed was the YubiKey, and they know who the user is... I don't like that."

The answer: **YubiKeys require a FIDO2 PIN**.

- The PIN is stored **locally on the YubiKey**, never sent over the network
- The PIN unlocks the key's ability to sign challenges
- 8 incorrect PIN attempts **locks the FIDO2 application permanently** (requires full reset, destroying all credentials)
- So it's still two factors: something you **have** (the key) + something you **know** (the PIN)
- A short PIN is fine because the attacker needs both the physical key AND the PIN, and gets only 8 tries

### For Sierra Specifically

Passwordless happens at the **IdP layer**, not in Sierra:

1. Configure FIDO2 security keys in your IdP (Azure AD, Google, Okta all support FIDO2)
2. Register YubiKeys for staff
3. Staff authenticate to the IdP with their YubiKey (passwordless)
4. IdP issues a SAML assertion to Sierra
5. Sierra never needs to know about FIDO2 — it just receives a valid SAML assertion

**No changes to Sierra required** to go passwordless — it's all in how you configure your IdP.

### Password Policy (from the session)

Modern standard (what RIT does, per NIST SP 800-63B):
- **16 characters minimum**
- **Set once, never rotate** — unless detected on a breach/compromise list
- **No complexity requirements** (length matters more than special characters)

**Reference**: [NIST SP 800-63B — Digital Identity Guidelines](https://pages.nist.gov/800-63-4/sp800-63b.html)

---

## 8. Conditional Access — Skip MFA on Trusted Networks

An attendee described this setup: MFA required off-network, skipped on the library's network. "If somebody forgets their phone, they're not going to be unable to work when they get in."

### Microsoft Entra ID

**Step 1: Create a Named Location**
1. Entra admin center > **Protection > Conditional Access > Named locations**
2. **+ IP ranges location**
3. Name it (e.g., "Library Network")
4. Check **Mark as trusted location**
5. Add your **public** IP ranges (the IP your traffic exits from, not internal 192.168.x.x addresses)

**Step 2: Create the Conditional Access Policy**
1. **Protection > Conditional Access > Policies > + New policy**
2. Name: "Require MFA except library network"
3. **Users**: Include All users. **Exclude break-glass accounts.**
4. **Target resources**: All cloud apps (or select Sierra SSO app)
5. **Network**: Include Any network. Exclude your Named Location.
6. **Grant**: Require multifactor authentication
7. **Enable**: Start in **Report-only** mode. Monitor sign-in logs for a week. Switch to **On** when validated.

**Critical**: Always exclude at least one emergency/break-glass account from ALL conditional access policies.

### Google Workspace

**Step 1: Create an Access Level**
1. Admin console > **Security > Access and data control > Context-Aware Access**
2. **Create access level**
3. Name: "On campus network"
4. Conditions: IP subnet = your campus IP ranges
5. Save

**Step 2: Assign to Apps**
1. In Context-Aware Access > **Assign access levels**
2. Select staff OU
3. Assign the access level to relevant apps

**Step 3: Configure 2-Step Verification**
1. **Security > Authentication > 2-Step verification**
2. Set enforcement policy for staff OU
3. Context-Aware Access and 2SV work together — stronger methods required off-network

**References:**
- [Microsoft — Conditional Access with Named Locations](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-assignment-network)
- [Google — Context-Aware Access](https://support.google.com/a/answer/9275380)

---

## 9. SAML Debugging and Troubleshooting

### Essential Tool: SAML-tracer

Install the **SAML-tracer** browser extension before you do anything else:
- [Firefox](https://addons.mozilla.org/en-US/firefox/addon/saml-tracer/)
- [Chrome](https://chromewebstore.google.com/detail/saml-tracer/mhfbofhkdalfnnmhpahndkonakbephkf)

Open it before attempting login. It intercepts HTTP traffic, detects SAML messages, and decodes them into readable XML. This is how you'll diagnose every SSO problem.

### The Debugging Checklist

1. Open SAML-tracer
2. Attempt the SSO login that's failing
3. Find the AuthnRequest (SP → IdP) — verify `Issuer` and `AssertionConsumerServiceURL`
4. Find the SAML Response (IdP → SP) — check `<StatusCode>`
5. If status is not `Success`, the IdP rejected the request — check IdP logs
6. If status is `Success`, check these fields in the assertion:

| Field | What to Check | Common Failure |
|-------|---------------|---------------|
| **Issuer** | Matches the IdP entityID Sierra expects? | IdP entityID changed or SP misconfigured |
| **Destination** | Matches Sierra's ACS URL exactly? | Trailing slash, HTTP vs HTTPS |
| **Audience** | Matches Sierra's entityID? | SP entityID mismatch |
| **NotBefore / NotOnOrAfter** | Timestamps valid relative to Sierra's clock? | **Clock skew** |
| **Recipient** | Matches ACS URL? | URL mismatch |
| **Signature** | Validates against IdP certificate? | Expired cert, cert rotation not applied |
| **NameID / Attributes** | Contains the expected attribute with the expected value? | Wrong attribute name, empty value, case mismatch |

### Common Problems and Fixes

**Clock Skew**
- **Symptom**: "Assertion expired" or silent login failure
- **Cause**: Sierra server's clock differs from IdP by more than the assertion validity window (~5 min)
- **Diagnosis**: Compare `NotBefore`/`NotOnOrAfter` in the assertion with Sierra server's time (`date -u`)
- **Fix**: Ensure NTP is running on the Sierra server. On Linux: `timedatectl status` to verify.

**Certificate Mismatch**
- **Symptom**: "Signature validation failed"
- **Cause**: IdP rotated its signing certificate but Sierra still has the old one
- **Diagnosis**: Extract cert from the Response's `<ds:X509Certificate>`, compare with Sierra's config
- **Fix**: Re-download IdP metadata and re-import into Sierra. Proactively monitor cert expiry dates.

**ACS URL Mismatch**
- **Symptom**: IdP error page, or Response goes nowhere
- **Cause**: ACS URL in IdP doesn't exactly match Sierra's actual endpoint
- **Watch for**: trailing slashes, HTTP vs HTTPS, port numbers, path case
- **Fix**: Copy the ACS URL from Sierra's SP metadata and paste it exactly into IdP config

**Attribute Name Mismatch**
- **Symptom**: User authenticates but Sierra says "user not found" or wrong account
- **Cause**: IdP sends `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` but Sierra expects `email`
- **Diagnosis**: Inspect `<AttributeStatement>` in SAML-tracer. Compare attribute `Name` values with what Sierra expects.
- **Fix**: Configure attribute mapping / claim rules in your IdP to send the attribute name Sierra expects.

**SSO ID Case Mismatch**
- **Symptom**: User authenticates at IdP but Sierra says no matching account
- **Cause**: SSO ID in Sierra is `JSmith` but IdP sends `jsmith`
- **Fix**: SSO IDs are **case-sensitive**. Make them match exactly.

### Command-Line Tools

```bash
# Inspect a certificate's details and expiry
openssl x509 -text -noout -in idp-cert.pem

# Verify an XML signature (requires xmlsec1)
xmlsec1 --verify --pubkey-cert-pem idp-cert.pem response.xml

# Decode a base64 SAML message from a URL parameter
echo "PHNhbWxwOl..." | base64 -d | xmllint --format -

# Decode a deflated + base64 SAML message (HTTP-Redirect binding)
echo "fZJNT8Mw..." | base64 -d | python3 -c "import sys,zlib; print(zlib.decompress(sys.stdin.buffer.read(),-15).decode())"
```

**References:**
- [SAML Debugging Handbook — Scalekit](https://www.scalekit.com/blog/saml-debugging-handbook-2026-how-to-diagnose-log-and-resolve-sso-failures)
- [Common SAML Errors — WorkOS](https://workos.com/guide/common-saml-errors)
- [SAML-tracer on GitHub](https://github.com/simplesamlphp/SAML-tracer)

---

## 10. Links and References

### Sierra Documentation (may require customer login)

- [SAML-Based Authentication for Staff — Overview](https://documentation.iii.com/sierrahelp/Content/sgil/sgil_saml_verification.html)
- [Configuring SAML Authentication](https://documentation.iii.com/sierrahelp/Content/sadmin/sadmin_backend_saml.html)
- [Configuring an Identity Provider](https://documentation.iii.com/sierrahelp/Content/sadmin/sadmin_backend_saml_addidp.html)
- [Uploading SSO IDs to Staff Accounts](https://documentation.iii.com/sierrahelp/Content/sadmin/sadmin_backend_saml_ssoid.html)
- [Enabling SAML Authentication](https://documentation.iii.com/sierrahelp/Content/sadmin/sadmin_backend_saml_enable.html)
- [Restarting the CAS Server](https://documentation.iii.com/sierrahelp/Content/sadmin/sadmin_backend_saml_cas.html)
- [Sierra Desktop Login with SAML](https://documentation.iii.com/sierrahelp/Content/sdesktop/sdesktop_logging_in.html)

### Polaris SSO Documentation

- [Polaris OAuth/ADFS Guide (PDF)](https://documentation.iii.com/polaris/PolarisPDFGuides/PolarisOAuthADFS_7.2.pdf)
- [Polaris OIDC Guide (PDF)](https://documentation.iii.com/polaris/PolarisPDFGuides/PolarisOAuthOpenIDConnect_7.3.pdf)

### Identity Provider Setup

- [Google Workspace — Custom SAML App](https://support.google.com/a/answer/6087519)
- [Google SAML Error Reference](https://support.google.com/a/answer/6301076)
- [Microsoft Entra ID — SAML SSO](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso)
- [Shibboleth IdP Documentation](https://shibboleth.atlassian.net/wiki/spaces/IDP5/overview)
- [Keycloak Documentation](https://www.keycloak.org/documentation)

### SAML Protocol

- [OASIS SAML V2.0 Technical Overview](https://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html)
- [Understanding SAML — Okta Developer](https://developer.okta.com/docs/concepts/saml/)

### SCIM / Provisioning

- [SCIM Protocol Reference](https://scim.cloud/)
- [Understanding SCIM — Okta Developer](https://developer.okta.com/docs/concepts/scim/)
- [Microsoft Entra SCIM Tutorial](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/use-scim-to-provision-users-and-groups)

### MFA and Security

- [CISA — Implement Number Matching in MFA](https://www.cisa.gov/sites/default/files/publications/fact-sheet-implement-number-matching-in-mfa-applications-508c.pdf)
- [NIST SP 800-63B — Digital Identity Guidelines](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [Duo Security Documentation](https://duo.com/docs)
- [Token2 Hardware Tokens](https://www.token2.com/)

### Passwordless / FIDO2

- [FIDO2 Passwordless — Yubico](https://www.yubico.com/authentication-standards/fido2/)
- [YubiKey FIDO2 Guide](https://docs.yubico.com/software/yubikey/tools/authenticator/auth-guide/fido2.html)
- [Understanding YubiKey PINs](https://support.yubico.com/hc/en-us/articles/4402836718866-Understanding-YubiKey-PINs)

### Debugging Tools

- [SAML-tracer (Firefox)](https://addons.mozilla.org/en-US/firefox/addon/saml-tracer/)
- [SAML-tracer (Chrome)](https://chromewebstore.google.com/detail/saml-tracer/mhfbofhkdalfnnmhpahndkonakbephkf)
- [SAML Decoder — SAMLTool](https://www.samltool.com/decode.php)

### Library Identity / Federation

- [FIM4L — Federated Identity Management for Libraries](https://www.fim4l.org/)
- [InCommon — Making Federation Work for Libraries](https://incommon.org/news/making-federation-work-for-libraries/)

### Community

- [Innovative Idea Exchange](https://ideas.iii.com) — upvote Justin's upcoming MFA requirement request
- [IUG Forum](https://forum.innovativeusers.org)
