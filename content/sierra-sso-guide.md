---
title: "Sierra SSO Technical Implementation Guide"
template: session
day: wednesday
date: "April 15"
description: "Technical deep-dive on SAML SSO for Sierra staff authentication: protocol fundamentals, IdP setup, Sierra configuration, Keycloak, SCIM provisioning, MFA, passwordless auth, conditional access, and SAML debugging."
---

<div class="card">
  <p>A deep-dive companion to the <a href="sierra-sso.html">Sierra Staff and Single Sign-On session notes</a> from IUG 2026. This guide is aimed at library systems administrators considering or actively implementing SAML SSO for Sierra staff authentication. It covers the full stack: SAML protocol fundamentals, identity provider setup, Sierra-specific configuration, Keycloak&rsquo;s emerging role, automated provisioning, MFA hardening, passwordless authentication, conditional access policies, and SAML debugging.</p>
</div>

<!-- Table of Contents -->

<h2>Table of Contents</h2>

<div class="section-list">
  <div class="section-item">
    <ol style="margin: 0.25rem 0 0 1.5rem;">
      <li><a href="#saml-fundamentals">SAML 2.0 Protocol Fundamentals</a></li>
      <li><a href="#idp-setup">Setting Up Your Identity Provider</a></li>
      <li><a href="#sierra-config">Sierra-Specific Configuration</a></li>
      <li><a href="#keycloak">Keycloak and the Future of Innovative Identity</a></li>
      <li><a href="#scim">SCIM and Automated User Provisioning</a></li>
      <li><a href="#mfa">MFA Deep Dive</a></li>
      <li><a href="#passwordless">Passwordless Authentication (FIDO2/WebAuthn)</a></li>
      <li><a href="#conditional-access">Conditional Access &mdash; Skip MFA on Trusted Networks</a></li>
      <li><a href="#debugging">SAML Debugging and Troubleshooting</a></li>
      <li><a href="#references">Links and References</a></li>
    </ol>
  </div>
</div>

<!-- Section 1: SAML 2.0 Protocol Fundamentals -->

<h2 id="saml-fundamentals">1. SAML 2.0 Protocol Fundamentals</h2>

<div class="card">
  <p>SAML (Security Assertion Markup Language) is an XML-based standard for exchanging authentication data between two parties:</p>
  <ul style="margin: 0.75rem 0 0 1.5rem;">
    <li><strong>Identity Provider (IdP)</strong> &mdash; the system that knows who your users are (Azure AD, Google, Shibboleth, Okta)</li>
    <li><strong>Service Provider (SP)</strong> &mdash; the application that needs to verify identity (Sierra)</li>
  </ul>
  <p style="margin-top: 0.75rem;">Sierra acts as the <strong>SP</strong>. Your organization&rsquo;s directory service acts as the <strong>IdP</strong>.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>The Login Flow (SP-Initiated &mdash; What Sierra Uses)</h3>
    <pre style="background: #f5f5f5; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem; line-height: 1.5;">Staff member                Sierra (SP)                Your IdP
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
    |<-- logged in -------------|                         |</pre>
    <p style="margin-top: 0.75rem;">The key thing: <strong>Sierra never sees the user&rsquo;s password.</strong> It only receives a signed assertion from your IdP saying &ldquo;this person authenticated successfully, and their username/email/uid is X.&rdquo;</p>
  </div>

  <div class="section-item">
    <h3>IdP-Initiated Flow</h3>
    <p>User starts at the IdP portal (Azure MyApps, Google apps launcher, Okta dashboard) and clicks a Sierra tile. The IdP generates a SAML Response directly without a preceding AuthnRequest. This works but is less secure &mdash; there&rsquo;s no request-response correlation, making replay attacks easier. SP-initiated (what Sierra does) is preferred.</p>
  </div>

  <div class="section-item">
    <h3>Metadata Exchange</h3>
    <p>Before SSO works, the SP and IdP need to exchange metadata &mdash; XML documents describing each party&rsquo;s configuration:</p>
    <p style="margin-top: 0.75rem;"><strong>SP Metadata (Sierra provides this):</strong></p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">entityID</code> &mdash; Sierra&rsquo;s unique identifier (a URL)</li>
      <li><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">AssertionConsumerService</code> &mdash; the ACS URL where the IdP sends responses</li>
      <li>SP&rsquo;s X.509 certificate (for optional request signing)</li>
    </ul>
    <p style="margin-top: 0.75rem;"><strong>IdP Metadata (your IdP provides this):</strong></p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">entityID</code> &mdash; your IdP&rsquo;s unique identifier</li>
      <li><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">SingleSignOnService</code> &mdash; the URL Sierra sends AuthnRequests to</li>
      <li>IdP&rsquo;s X.509 signing certificate (Sierra uses this to verify assertions are genuine)</li>
    </ul>
    <p style="margin-top: 0.75rem;">In Sierra&rsquo;s admin interface, you paste in your IdP&rsquo;s metadata URL. Sierra generates its own SP metadata URL that you give to your IdP admin.</p>
  </div>

  <div class="section-item">
    <h3>What&rsquo;s Inside a SAML Assertion</h3>
    <p>The signed XML assertion the IdP sends back contains:</p>
    <pre style="background: #f5f5f5; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem; line-height: 1.4; margin-top: 0.75rem;">&lt;saml:Assertion&gt;
  &lt;saml:Issuer&gt;https://idp.yourlibrary.org&lt;/saml:Issuer&gt;
  &lt;ds:Signature&gt;...&lt;/ds:Signature&gt;

  &lt;saml:Subject&gt;
    &lt;saml:NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"&gt;
      jsmith@library.org
    &lt;/saml:NameID&gt;
    &lt;saml:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer"&gt;
      &lt;saml:SubjectConfirmationData
        Recipient="https://sierra.library.org/saml/acs"
        NotOnOrAfter="2026-04-15T14:35:00Z"/&gt;
    &lt;/saml:SubjectConfirmation&gt;
  &lt;/saml:Subject&gt;

  &lt;saml:Conditions NotBefore="2026-04-15T14:29:00Z"
                   NotOnOrAfter="2026-04-15T14:35:00Z"&gt;
    &lt;saml:AudienceRestriction&gt;
      &lt;saml:Audience&gt;https://sierra.library.org/saml/metadata&lt;/saml:Audience&gt;
    &lt;/saml:AudienceRestriction&gt;
  &lt;/saml:Conditions&gt;

  &lt;saml:AttributeStatement&gt;
    &lt;saml:Attribute Name="uid"&gt;
      &lt;saml:AttributeValue&gt;jsmith&lt;/saml:AttributeValue&gt;
    &lt;/saml:Attribute&gt;
    &lt;saml:Attribute Name="email"&gt;
      &lt;saml:AttributeValue&gt;jsmith@library.org&lt;/saml:AttributeValue&gt;
    &lt;/saml:Attribute&gt;
  &lt;/saml:AttributeStatement&gt;
&lt;/saml:Assertion&gt;</pre>
    <p style="margin-top: 0.75rem;">The critical parts:</p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Issuer</strong> &mdash; must match the IdP entityID Sierra expects</li>
      <li><strong>Signature</strong> &mdash; proves the assertion is genuine and untampered</li>
      <li><strong>Subject/NameID</strong> &mdash; the user&rsquo;s identity</li>
      <li><strong>Conditions</strong> &mdash; time window the assertion is valid (typically 5 minutes)</li>
      <li><strong>AudienceRestriction</strong> &mdash; must match Sierra&rsquo;s entityID</li>
      <li><strong>AttributeStatement</strong> &mdash; the attribute Sierra matches against the SSO ID field</li>
    </ul>
  </div>

  <div class="section-item">
    <h3>NameID Formats</h3>
    <table style="margin-top: 0.5rem;">
      <thead>
        <tr>
          <th>Format</th>
          <th>When to Use</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">emailAddress</code></td>
          <td>Most common; user&rsquo;s email as identifier</td>
        </tr>
        <tr>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">persistent</code></td>
          <td>Opaque pairwise ID; good for privacy</td>
        </tr>
        <tr>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">unspecified</code></td>
          <td>Let the IdP decide</td>
        </tr>
      </tbody>
    </table>
    <p style="margin-top: 0.75rem;">For Sierra, <strong>emailAddress</strong> or <strong>unspecified</strong> with a uid attribute is typical.</p>
  </div>

  <div class="section-item">
    <h3>Signing and Encryption</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Response signing</strong> (required): IdP signs the assertion with its private key. Sierra validates using the IdP&rsquo;s public certificate from metadata.</li>
      <li><strong>Request signing</strong> (optional): Sierra signs its AuthnRequest so the IdP can verify legitimacy.</li>
      <li><strong>Assertion encryption</strong> (optional): IdP encrypts the assertion with Sierra&rsquo;s public key. Adds PII protection beyond TLS.</li>
      <li><strong>Algorithm</strong>: RSA-SHA256 is the current standard. SHA-1 is deprecated &mdash; do not use.</li>
    </ul>
  </div>
</div>

<!-- Section 2: Setting Up Your Identity Provider -->

<h2 id="idp-setup">2. Setting Up Your Identity Provider</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Google Workspace</h3>
    <p>Available on all paid editions (Business, Education, Nonprofits).</p>
    <ol style="margin: 0.75rem 0 0 1.5rem;">
      <li>Sign in to <a href="https://admin.google.com">admin.google.com</a></li>
      <li>Navigate to <strong>Apps &gt; Web and mobile apps</strong></li>
      <li>Click <strong>Add app &gt; Add custom SAML app</strong></li>
      <li>Enter app name (e.g., &ldquo;Sierra ILS&rdquo;), optionally upload an icon</li>
      <li><strong>Google IdP Information page</strong> &mdash; download or copy:
        <ul style="margin: 0.25rem 0 0 1.5rem;">
          <li>SSO URL: <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">https://accounts.google.com/o/saml2/idp?idpid=&lt;your_id&gt;</code></li>
          <li>Entity ID: <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">https://accounts.google.com/o/saml2?idpid=&lt;your_id&gt;</code></li>
          <li>Certificate (download the PEM file)</li>
          <li>Or download the full IdP metadata XML</li>
        </ul>
      </li>
      <li><strong>Service Provider Details</strong> &mdash; enter values from Sierra&rsquo;s SAML config:
        <ul style="margin: 0.25rem 0 0 1.5rem;">
          <li>ACS URL (from Sierra&rsquo;s SP metadata)</li>
          <li>Entity ID (from Sierra&rsquo;s SP metadata)</li>
          <li>Name ID format: <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">EMAIL</code> (or <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">PERSISTENT</code>)</li>
          <li>Name ID: Primary email</li>
          <li>Check &ldquo;Signed response&rdquo; if Sierra requires it</li>
        </ul>
      </li>
      <li><strong>Attribute mapping</strong> &mdash; add the attribute Sierra expects (e.g., <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">uid</code> mapped to Primary email or Username)</li>
      <li>Click <strong>Finish</strong></li>
      <li><strong>Enable for users</strong>: By default the app is OFF. Select your staff OU and set to <strong>ON</strong></li>
      <li>Allow up to 24 hours for propagation (usually much faster)</li>
    </ol>
    <p style="margin-top: 0.75rem;"><strong>Gotcha for free nonprofit tier</strong>: No bulk YubiKey management &mdash; each key must be registered per-account manually in the admin console.</p>
    <p style="margin-top: 0.5rem;"><strong>Reference</strong>: <a href="https://support.google.com/a/answer/6087519">Google &mdash; Set up custom SAML app</a></p>
  </div>

  <div class="section-item">
    <h3>Microsoft Entra ID (Azure AD)</h3>
    <ol style="margin: 0.75rem 0 0 1.5rem;">
      <li>Sign in to <a href="https://entra.microsoft.com">entra.microsoft.com</a></li>
      <li>Navigate to <strong>Identity &gt; Applications &gt; Enterprise applications</strong></li>
      <li>Click <strong>New application &gt; Create your own application</strong></li>
      <li>Name it &ldquo;Sierra ILS&rdquo;, select &ldquo;Integrate any other application&rdquo;</li>
      <li>Go to <strong>Single sign-on &gt; SAML</strong></li>
      <li><strong>Basic SAML Configuration</strong>:
        <ul style="margin: 0.25rem 0 0 1.5rem;">
          <li>Identifier (Entity ID): Sierra&rsquo;s entityID from SP metadata</li>
          <li>Reply URL (ACS URL): Sierra&rsquo;s ACS URL from SP metadata</li>
        </ul>
      </li>
      <li><strong>Attributes &amp; Claims</strong>: Configure the attribute Sierra expects (e.g., <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">uid</code> mapped to <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">user.userprincipalname</code> or <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">user.mailnickname</code>)</li>
      <li><strong>SAML Certificates</strong>: Download the Federation Metadata XML (this is your IdP metadata to give to Sierra)</li>
      <li><strong>Users and groups</strong>: Assign staff users/groups to the application</li>
    </ol>
    <p style="margin-top: 0.75rem;"><strong>Reference</strong>: <a href="https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso">Microsoft &mdash; SAML SSO for apps</a></p>
  </div>

  <div class="section-item">
    <h3>Shibboleth</h3>
    <p>What RIT uses (as discussed in the session). Shibboleth is the standard in academic libraries.</p>
    <ul style="margin: 0.75rem 0 0 1.5rem;">
      <li>Shibboleth IdP is self-hosted (typically by your university&rsquo;s central IT)</li>
      <li>Configuration lives in XML files on the IdP server</li>
      <li>Your IdP admin adds Sierra as a relying party by importing Sierra&rsquo;s SP metadata</li>
      <li>Attribute release policies control which attributes the IdP sends to Sierra</li>
      <li>Often integrated with InCommon Federation for cross-institutional trust</li>
    </ul>
    <p style="margin-top: 0.75rem;"><strong>Reference</strong>: <a href="https://shibboleth.atlassian.net/wiki/spaces/IDP5/overview">Shibboleth IdP Documentation</a></p>
  </div>

  <div class="section-item">
    <h3>Any SAML 2.0 IdP &mdash; General Process</h3>
    <p>Sierra supports <strong>any SAML 2.0 compliant IdP</strong>. The general process is always:</p>
    <ol style="margin: 0.75rem 0 0 1.5rem;">
      <li>Get Sierra&rsquo;s SP metadata URL from Sierra Admin &gt; SAML Configuration</li>
      <li>Import that into your IdP</li>
      <li>Get your IdP&rsquo;s metadata URL</li>
      <li>Import that into Sierra&rsquo;s SAML Configuration</li>
      <li>Configure the attribute mapping (what attribute = SSO ID)</li>
      <li>Upload SSO IDs for staff (CSV or manual)</li>
      <li>Test in test mode</li>
      <li>Enable</li>
    </ol>
  </div>
</div>

<!-- Section 3: Sierra-Specific Configuration -->

<h2 id="sierra-config">3. Sierra-Specific Configuration</h2>

<div class="card">
  <p><strong>Requirements:</strong></p>
  <ul style="margin: 0.75rem 0 0 1.5rem;">
    <li>Sierra <strong>6.1+</strong> (6.0 added staff SAML for Web/Admin only; 6.1 extended to Desktop and Web Management Reports)</li>
    <li>Permission <strong>725 (SAML Administrator)</strong> assigned to the configuring staff account</li>
    <li>Access to your IdP administrator</li>
  </ul>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>Configuration Steps (Sierra Admin App)</h3>
    <p><strong>Back End Management &gt; SAML Configuration &gt; Identity Providers tab &gt; ADD:</strong></p>
    <table style="margin-top: 0.75rem;">
      <thead>
        <tr>
          <th>Field</th>
          <th>Description</th>
          <th>Notes</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Name</td>
          <td>Unique identifier (min 3 chars)</td>
          <td>Displayed on the login button. <strong>Immutable once created.</strong></td>
        </tr>
        <tr>
          <td>Usage</td>
          <td>Patrons, Staff, or Both</td>
          <td>Can have separate IdPs for patron vs. staff</td>
        </tr>
        <tr>
          <td>Metadata URL</td>
          <td>Your IdP&rsquo;s metadata endpoint</td>
          <td>Must be HTTPS, min 12 chars</td>
        </tr>
        <tr>
          <td>Attribute</td>
          <td>IdP response attribute to match against SSO IDs</td>
          <td>e.g., <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">uid</code>, <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">email</code>, <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">username</code></td>
        </tr>
        <tr>
          <td>Duration in Seconds</td>
          <td>Session validity</td>
          <td>Default 3600; align with IdP session settings</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section-item">
    <h3>Upload SSO IDs</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li>CSV format: <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">username,sso_id</code> (header row ignored)</li>
      <li><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">username</code> = Sierra login name (<strong>case-sensitive</strong>)</li>
      <li><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">sso_id</code> = matching attribute from IdP (<strong>case-sensitive</strong>, must be unique)</li>
      <li>Errors block the entire upload &mdash; fix all errors before retrying</li>
      <li>Can also set SSO IDs individually per user in the staff record</li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Management Tab</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>ENABLE STAFF AUTH</strong> (or ENABLE PATRON AUTH)</li>
      <li>Triggers automatic restart of CAS server and staff webapps &mdash; <strong>plan for off-hours</strong></li>
      <li>After modifying IdP settings, manually restart CAS server via <strong>RESTART CAS SERVER</strong></li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Test Mode</h3>
    <p>You can configure and test SAML <strong>without affecting production</strong>. Set up the IdP, upload SSO IDs, and test the flow before clicking ENABLE. Justin Newcomer specifically mentioned this in the session: &ldquo;It&rsquo;s self-service now. You can just go into the admin website and set it up yourself in test mode without interfering with production.&rdquo;</p>
  </div>

  <div class="section-item">
    <h3>SSO ID Management Tips (from the session)</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li>SSO IDs can be <strong>changed live</strong> &mdash; useful for testing (swap your SSO ID to a test account, login as that account, swap it back)</li>
      <li>When provisioning new users, adding the SSO ID is just part of the standard process</li>
      <li>For student employees: set a random legacy password they never receive; SSO is their only login path</li>
      <li>Clone permissions from similar accounts when onboarding: &ldquo;Takes longer to close the ticket than to actually click &lsquo;copy from other supervisor&rsquo;&rdquo;</li>
    </ul>
  </div>

  <div class="section-item">
    <h3>What Still Requires Legacy Passwords</h3>
    <table style="margin-top: 0.5rem;">
      <thead>
        <tr>
          <th>Application</th>
          <th>SSO Support</th>
          <th>Workaround</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Sierra Desktop Client</td>
          <td>Yes (6.1+)</td>
          <td>&mdash;</td>
        </tr>
        <tr>
          <td>Sierra Web</td>
          <td>Yes (6.0+)</td>
          <td>&mdash;</td>
        </tr>
        <tr>
          <td>Admin App</td>
          <td>Yes (6.0+)</td>
          <td>&mdash;</td>
        </tr>
        <tr>
          <td>Web Management Reports</td>
          <td>Yes (6.1+)</td>
          <td>&mdash;</td>
        </tr>
        <tr>
          <td>Decision Center</td>
          <td><strong>No</strong></td>
          <td>Must have legacy password</td>
        </tr>
        <tr>
          <td>Circa</td>
          <td><strong>No</strong></td>
          <td>Must have legacy password; Justin considering vibe-coding a replacement</td>
        </tr>
        <tr>
          <td>Circulation overrides</td>
          <td><strong>Legacy only</strong></td>
          <td>Supervisor override pop-up uses legacy credentials</td>
        </tr>
        <tr>
          <td>Innovative mobile worklists</td>
          <td><strong>No</strong></td>
          <td>On the roadmap</td>
        </tr>
        <tr>
          <td>Vega mobile worklists</td>
          <td><strong>No</strong></td>
          <td>On the roadmap</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- Section 4: Keycloak -->

<h2 id="keycloak">4. Keycloak and the Future of Innovative Identity</h2>

<div class="card">
  <p><a href="https://www.keycloak.org/">Keycloak</a> is an open-source Identity and Access Management (IAM) server maintained by CNCF (formerly Red Hat). It provides SSO, identity brokering, user federation (LDAP/AD), support for OIDC, OAuth 2.0, and SAML 2.0, fine-grained authorization, and multi-tenancy via &ldquo;realms.&rdquo;</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>Why This Matters for Sierra/Polaris/Vega</h3>
    <p>At the SSO session, an attendee (appearing to be from Innovative&rsquo;s engineering side) mentioned that Vega currently runs through Keycloak and that there are plans to make Keycloak a shared service across Polaris and Sierra. If enough customers request this via IdeaLab, it could accelerate adoption.</p>
  </div>

  <div class="section-item">
    <h3>What Keycloak as a Shared Service Would Mean</h3>
    <pre style="background: #f5f5f5; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem; line-height: 1.5;">                        [Keycloak]
                       /     |     \
                      /      |      \
              [Sierra]  [Polaris]  [Vega]
                 SAML    OIDC      OIDC</pre>
    <p style="margin-top: 0.75rem;"><strong>Identity Brokering</strong> &mdash; Keycloak sits between your apps and your IdP:</p>
    <pre style="background: #f5f5f5; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem; line-height: 1.5; margin-top: 0.5rem;">[Sierra] &lt;--SAML--&gt; [Keycloak] &lt;--OIDC--&gt; [Azure AD]
                               &lt;--SAML--&gt; [Shibboleth]
                               &lt;--OIDC--&gt; [Google]
                               &lt;--LDAP--&gt; [Active Directory]</pre>
    <p style="margin-top: 0.75rem;">Benefits:</p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Protocol translation</strong>: Sierra speaks SAML, but your IdP might prefer OIDC &mdash; Keycloak handles the conversion</li>
      <li><strong>One integration point</strong>: Configure your IdP once in Keycloak; all Innovative products inherit it</li>
      <li><strong>Consistent login experience</strong> across Sierra, Polaris, Vega</li>
      <li><strong>Easier &ldquo;bring your own IdP&rdquo;</strong>: Keycloak&rsquo;s admin console makes adding new IdPs straightforward</li>
      <li><strong>Multi-tenancy</strong>: Each library/consortium gets its own Keycloak &ldquo;realm&rdquo; in a hosted environment</li>
      <li><strong>Open source</strong>: No per-user IAM licensing costs</li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Key Keycloak Concepts</h3>
    <table style="margin-top: 0.5rem;">
      <thead>
        <tr>
          <th>Concept</th>
          <th>What It Is</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Realm</strong></td>
          <td>Isolated tenant &mdash; own users, groups, clients, IdPs. Think of it as a separate identity domain per library system.</td>
        </tr>
        <tr>
          <td><strong>Client</strong></td>
          <td>An application registered in Keycloak (Sierra would be a SAML client, Vega an OIDC client)</td>
        </tr>
        <tr>
          <td><strong>Identity Broker</strong></td>
          <td>Configuration to delegate auth to an external IdP (Azure AD, Google, Shibboleth, etc.)</td>
        </tr>
        <tr>
          <td><strong>User Federation</strong></td>
          <td>Direct connection to LDAP/AD &mdash; Keycloak queries the directory at login time</td>
        </tr>
        <tr>
          <td><strong>Protocol Mappers</strong></td>
          <td>Rules for which attributes/claims appear in tokens and assertions sent to clients</td>
        </tr>
      </tbody>
    </table>
    <p style="margin-top: 0.75rem;"><strong>Reference</strong>: <a href="https://www.keycloak.org/docs/latest/server_admin/index.html">Keycloak Server Administration Guide</a></p>
  </div>
</div>

<!-- Section 5: SCIM -->

<h2 id="scim">5. SCIM and Automated User Provisioning</h2>

<div class="card">
  <p><strong>The problem:</strong> Right now, Sierra SSO ID management is manual &mdash; upload a CSV of <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">username,sso_id</code> pairs, or set the SSO ID individually per staff record. When someone leaves, manually remove their account. No automatic group/permission mapping from your IdP.</p>
  <p style="margin-top: 0.75rem;"><strong>SCIM (System for Cross-domain Identity Management)</strong> is a REST API standard (RFC 7643/7644) for automatically syncing users and groups between your IdP and applications. <strong>Sierra does not support SCIM today</strong> &mdash; this is aspirational and worth requesting via IdeaLab.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>How SCIM Would Work</h3>
    <pre style="background: #f5f5f5; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem; line-height: 1.5;">[HR System] --&gt; [IdP (Azure/Okta/Google)] --&gt; SCIM API --&gt; [Sierra]
                                                             - Create user
                                                             - Set SSO ID
                                                             - Assign permissions
                                                             - Deactivate on departure</pre>
  </div>

  <div class="section-item">
    <h3>The API Model</h3>
    <table style="margin-top: 0.5rem;">
      <thead>
        <tr>
          <th>Endpoint</th>
          <th>Method</th>
          <th>What It Does</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">/Users</code></td>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">POST</code></td>
          <td>Create a new staff account</td>
        </tr>
        <tr>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">/Users/{id}</code></td>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">GET</code></td>
          <td>Retrieve a staff account</td>
        </tr>
        <tr>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">/Users/{id}</code></td>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">PATCH</code></td>
          <td>Update attributes (name change, department transfer)</td>
        </tr>
        <tr>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">/Users/{id}</code></td>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">DELETE</code></td>
          <td>Deprovisioning (staff departure)</td>
        </tr>
        <tr>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">/Groups</code></td>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">POST/PATCH</code></td>
          <td>Create/update permission groups</td>
        </tr>
        <tr>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">/Groups/{id}</code></td>
          <td><code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">PATCH</code></td>
          <td>Add/remove members from groups</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section-item">
    <h3>SCIM vs. CSV Upload</h3>
    <table style="margin-top: 0.5rem;">
      <thead>
        <tr>
          <th></th>
          <th>CSV Upload (current)</th>
          <th>SCIM (aspirational)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Timing</strong></td>
          <td>Batch (manual trigger)</td>
          <td>Real-time</td>
        </tr>
        <tr>
          <td><strong>Deprovisioning</strong></td>
          <td>Often forgotten</td>
          <td>Automatic when user deactivated in IdP</td>
        </tr>
        <tr>
          <td><strong>Group/permissions</strong></td>
          <td>Managed separately in Sierra</td>
          <td>Could map IdP groups to Sierra permissions</td>
        </tr>
        <tr>
          <td><strong>Error handling</strong></td>
          <td>Errors block entire upload</td>
          <td>Per-record HTTP error responses</td>
        </tr>
        <tr>
          <td><strong>Audit trail</strong></td>
          <td>Spreadsheet-level</td>
          <td>Full HTTP request/response logs</td>
        </tr>
        <tr>
          <td><strong>Effort for 10 new hires</strong></td>
          <td>~30 min manual work</td>
          <td>Zero &mdash; automatic</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section-item">
    <h3>IdPs That Support SCIM as a Client</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Microsoft Entra ID</strong> &mdash; robust built-in SCIM provisioning</li>
      <li><strong>Okta</strong> &mdash; robust SCIM 2.0 support</li>
      <li><strong>Google Workspace</strong> &mdash; supports SCIM provisioning</li>
      <li><strong>JumpCloud, OneLogin, Ping Identity</strong> &mdash; all support SCIM</li>
    </ul>
    <p style="margin-top: 0.75rem;">If Keycloak becomes the shared identity layer, Keycloak does have SCIM support that could potentially bridge the gap.</p>
  </div>
</div>

<!-- Section 6: MFA Deep Dive -->

<h2 id="mfa">6. MFA Deep Dive</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Why Regular Push MFA Is No Longer Enough</h3>
    <p>Standard push sends a simple &ldquo;Approve / Deny&rdquo; notification. This is vulnerable to <strong>MFA fatigue (prompt bombing)</strong>:</p>
    <ol style="margin: 0.75rem 0 0 1.5rem;">
      <li>Attacker obtains stolen credentials (phishing, dark web)</li>
      <li>Attacker repeatedly attempts login, triggering push after push</li>
      <li>Victim taps &ldquo;Approve&rdquo; out of frustration, confusion, or at 2 AM half-asleep</li>
      <li>Optionally, attacker calls victim posing as IT: &ldquo;just approve the prompt&rdquo;</li>
    </ol>
  </div>

  <div class="section-item">
    <h3>Real Breaches from MFA Fatigue</h3>
    <table style="margin-top: 0.5rem;">
      <thead>
        <tr>
          <th>Organization</th>
          <th>Date</th>
          <th>What Happened</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Uber</td>
          <td>Sep 2022</td>
          <td>Lapsus$ bombarded a contractor&rsquo;s phone + posed as IT via WhatsApp</td>
        </tr>
        <tr>
          <td>Cisco</td>
          <td>May 2022</td>
          <td>Voice phishing combined with push bombing; gained VPN access</td>
        </tr>
        <tr>
          <td>Microsoft</td>
          <td>Mar 2022</td>
          <td>Lapsus$ used MFA fatigue + session token replay; 37 GB source code stolen</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section-item">
    <h3>Verified Push / Number Matching &mdash; The Fix</h3>
    <p>What RIT uses (Duo &ldquo;Verified Push&rdquo;). Microsoft calls it &ldquo;number matching.&rdquo;</p>
    <ol style="margin: 0.75rem 0 0 1.5rem;">
      <li>User enters credentials at login page</li>
      <li>Login page displays a <strong>number</strong> (e.g., &ldquo;37&rdquo;) &mdash; Microsoft uses 2 digits, Duo uses 3</li>
      <li>Push notification asks: &ldquo;Enter the number shown on your sign-in screen: ___&rdquo;</li>
      <li>User must type &ldquo;37&rdquo; into the authenticator app</li>
      <li>If correct, authentication succeeds</li>
    </ol>
    <p style="margin-top: 0.75rem;"><strong>Why it works</strong>: The user must be actively looking at both the login screen AND their phone. An attacker triggering prompts from their own browser sees a different number &mdash; the victim has no number to enter, so there&rsquo;s nothing to mindlessly approve.</p>
  </div>

  <div class="section-item">
    <h3>Additional Defenses to Layer On</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li>Show app name, location, device, and IP in the push notification</li>
      <li>Rate-limit MFA prompts (e.g., 3 per 5 minutes, then lockout)</li>
      <li>Let users report suspicious prompts from the notification itself</li>
      <li>Turn off SMS-based MFA (vulnerable to SIM swapping)</li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Platform Support for Number Matching</h3>
    <table style="margin-top: 0.5rem;">
      <thead>
        <tr>
          <th>Platform</th>
          <th>Feature Name</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Microsoft Authenticator</td>
          <td>Number matching</td>
          <td>Mandatory for all tenants since May 2023</td>
        </tr>
        <tr>
          <td>Cisco Duo</td>
          <td>Verified Duo Push</td>
          <td>Available in Duo 4.x+; enable per policy</td>
        </tr>
        <tr>
          <td>Okta Verify</td>
          <td>Number Challenge</td>
          <td>Configurable per policy</td>
        </tr>
        <tr>
          <td>Google</td>
          <td>Risk-based challenges</td>
          <td>Similar protection via context, not explicit number matching</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section-item">
    <h3>What RIT Does (from the session)</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li>Duo with <strong>verified push</strong> (type 3 numbers &mdash; &ldquo;we&rsquo;re supposed to be thankful we only have to type 3&rdquo;)</li>
      <li>Disabled SMS MFA</li>
      <li>Disabled regular push</li>
      <li>Disabled phone-call-based MFA (switched to digital phones &mdash; can&rsquo;t MFA from the phone you&rsquo;re calling from)</li>
      <li>YubiKey for Duo web auth (self-enrollment)</li>
      <li>Don&rsquo;t support Duo offline codes (&ldquo;don&rsquo;t want to deal with ingesting all those random seeds&rdquo;)</li>
    </ul>
    <p style="margin-top: 0.75rem;"><strong>References:</strong></p>
    <ul style="margin: 0.25rem 0 0 1.5rem;">
      <li><a href="https://www.cisa.gov/sites/default/files/publications/fact-sheet-implement-number-matching-in-mfa-applications-508c.pdf">CISA &mdash; Implement Number Matching in MFA</a></li>
      <li><a href="https://www.beyondtrust.com/resources/glossary/mfa-fatigue-attack">MFA Fatigue Attacks &mdash; BeyondTrust</a></li>
    </ul>
  </div>
</div>

<!-- Section 7: Passwordless Authentication -->

<h2 id="passwordless">7. Passwordless Authentication (FIDO2/WebAuthn)</h2>

<div class="card">
  <p>This came up in the session discussion. Justin is interested but cautious. Passwordless happens at the <strong>IdP layer</strong>, not in Sierra &mdash; <strong>no changes to Sierra are required</strong> to go passwordless.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>The Standards</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>FIDO2</strong> = <strong>WebAuthn</strong> (W3C browser API) + <strong>CTAP2</strong> (how the browser talks to security keys over USB/NFC/BLE)</li>
      <li><strong>Passkeys</strong> = the user-facing term for FIDO2 discoverable credentials</li>
    </ul>
  </div>

  <div class="section-item">
    <h3>How It Works</h3>
    <p><strong>Registration:</strong></p>
    <ol style="margin: 0.5rem 0 0 1.5rem;">
      <li>User visits site, initiates passkey registration</li>
      <li>Site sends a challenge to the browser</li>
      <li>Browser invokes the authenticator (YubiKey or platform biometric)</li>
      <li>Authenticator generates a <strong>public/private key pair</strong> bound to this site&rsquo;s origin</li>
      <li>Private key <strong>never leaves the device</strong></li>
      <li>Public key is stored server-side</li>
    </ol>
    <p style="margin-top: 0.75rem;"><strong>Authentication:</strong></p>
    <ol style="margin: 0.5rem 0 0 1.5rem;">
      <li>User visits site, initiates login</li>
      <li>Site sends a challenge</li>
      <li>User touches the YubiKey + enters the PIN (or uses biometric)</li>
      <li>Authenticator signs the challenge with the private key</li>
      <li>Site verifies the signature with the stored public key</li>
    </ol>
    <p style="margin-top: 0.75rem;"><strong>Why it&rsquo;s phishing-resistant</strong>: The credential is bound to the <strong>exact origin</strong> (e.g., <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">https://sierra.library.org</code>). A phishing site at <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">https://sierra-library.evil.com</code> simply can&rsquo;t trigger the credential.</p>
  </div>

  <div class="section-item">
    <h3>Types of Authenticators</h3>
    <table style="margin-top: 0.5rem;">
      <thead>
        <tr>
          <th>Type</th>
          <th>Examples</th>
          <th>Pros</th>
          <th>Cons</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Hardware security keys</strong></td>
          <td>YubiKey 5, Google Titan, Feitian</td>
          <td>Strongest security; hardware-bound; no battery</td>
          <td>Must carry it; costs $25&ndash;70/key; limited credential slots (25 on YubiKey 5)</td>
        </tr>
        <tr>
          <td><strong>Platform authenticators</strong></td>
          <td>Windows Hello, Touch ID, Face ID</td>
          <td>Very convenient; built into device</td>
          <td>Tied to one device</td>
        </tr>
        <tr>
          <td><strong>Synced passkeys</strong></td>
          <td>iCloud Keychain, Google Password Manager, 1Password</td>
          <td>Sync across devices</td>
          <td>Less secure than hardware-bound (cloud compromise risk)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section-item">
    <h3>The PIN Question</h3>
    <p>Justin&rsquo;s concern from the session: &ldquo;If somebody didn&rsquo;t have a password and all they needed was the YubiKey, and they know who the user is&hellip; I don&rsquo;t like that.&rdquo;</p>
    <p style="margin-top: 0.75rem;">The answer: <strong>YubiKeys require a FIDO2 PIN.</strong></p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li>The PIN is stored <strong>locally on the YubiKey</strong>, never sent over the network</li>
      <li>The PIN unlocks the key&rsquo;s ability to sign challenges</li>
      <li>8 incorrect PIN attempts <strong>locks the FIDO2 application permanently</strong> (requires full reset, destroying all credentials)</li>
      <li>So it&rsquo;s still two factors: something you <strong>have</strong> (the key) + something you <strong>know</strong> (the PIN)</li>
      <li>A short PIN is fine because the attacker needs both the physical key AND the PIN, and gets only 8 tries</li>
    </ul>
  </div>

  <div class="section-item">
    <h3>For Sierra Specifically</h3>
    <ol style="margin: 0.5rem 0 0 1.5rem;">
      <li>Configure FIDO2 security keys in your IdP (Azure AD, Google, Okta all support FIDO2)</li>
      <li>Register YubiKeys for staff</li>
      <li>Staff authenticate to the IdP with their YubiKey (passwordless)</li>
      <li>IdP issues a SAML assertion to Sierra</li>
      <li>Sierra never needs to know about FIDO2 &mdash; it just receives a valid SAML assertion</li>
    </ol>
  </div>

  <div class="section-item">
    <h3>Password Policy (from the session)</h3>
    <p>Modern standard (what RIT does, per NIST SP 800-63B):</p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>16 characters minimum</strong></li>
      <li><strong>Set once, never rotate</strong> &mdash; unless detected on a breach/compromise list</li>
      <li><strong>No complexity requirements</strong> (length matters more than special characters)</li>
    </ul>
    <p style="margin-top: 0.75rem;"><strong>Reference</strong>: <a href="https://pages.nist.gov/800-63-4/sp800-63b.html">NIST SP 800-63B &mdash; Digital Identity Guidelines</a></p>
  </div>
</div>

<!-- Section 8: Conditional Access -->

<h2 id="conditional-access">8. Conditional Access &mdash; Skip MFA on Trusted Networks</h2>

<div class="card">
  <p>An attendee described this setup: MFA required off-network, skipped on the library&rsquo;s network. &ldquo;If somebody forgets their phone, they&rsquo;re not going to be unable to work when they get in.&rdquo;</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>Microsoft Entra ID</h3>
    <p><strong>Step 1: Create a Named Location</strong></p>
    <ol style="margin: 0.5rem 0 0 1.5rem;">
      <li>Entra admin center &gt; <strong>Protection &gt; Conditional Access &gt; Named locations</strong></li>
      <li><strong>+ IP ranges location</strong></li>
      <li>Name it (e.g., &ldquo;Library Network&rdquo;)</li>
      <li>Check <strong>Mark as trusted location</strong></li>
      <li>Add your <strong>public</strong> IP ranges (the IP your traffic exits from, not internal 192.168.x.x addresses)</li>
    </ol>
    <p style="margin-top: 0.75rem;"><strong>Step 2: Create the Conditional Access Policy</strong></p>
    <ol style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Protection &gt; Conditional Access &gt; Policies &gt; + New policy</strong></li>
      <li>Name: &ldquo;Require MFA except library network&rdquo;</li>
      <li><strong>Users</strong>: Include All users. <strong>Exclude break-glass accounts.</strong></li>
      <li><strong>Target resources</strong>: All cloud apps (or select Sierra SSO app)</li>
      <li><strong>Network</strong>: Include Any network. Exclude your Named Location.</li>
      <li><strong>Grant</strong>: Require multifactor authentication</li>
      <li><strong>Enable</strong>: Start in <strong>Report-only</strong> mode. Monitor sign-in logs for a week. Switch to <strong>On</strong> when validated.</li>
    </ol>
    <p style="margin-top: 0.75rem;"><strong>Critical</strong>: Always exclude at least one emergency/break-glass account from ALL conditional access policies.</p>
  </div>

  <div class="section-item">
    <h3>Google Workspace</h3>
    <p><strong>Step 1: Create an Access Level</strong></p>
    <ol style="margin: 0.5rem 0 0 1.5rem;">
      <li>Admin console &gt; <strong>Security &gt; Access and data control &gt; Context-Aware Access</strong></li>
      <li><strong>Create access level</strong></li>
      <li>Name: &ldquo;On campus network&rdquo;</li>
      <li>Conditions: IP subnet = your campus IP ranges</li>
      <li>Save</li>
    </ol>
    <p style="margin-top: 0.75rem;"><strong>Step 2: Assign to Apps</strong></p>
    <ol style="margin: 0.5rem 0 0 1.5rem;">
      <li>In Context-Aware Access &gt; <strong>Assign access levels</strong></li>
      <li>Select staff OU</li>
      <li>Assign the access level to relevant apps</li>
    </ol>
    <p style="margin-top: 0.75rem;"><strong>Step 3: Configure 2-Step Verification</strong></p>
    <ol style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Security &gt; Authentication &gt; 2-Step verification</strong></li>
      <li>Set enforcement policy for staff OU</li>
      <li>Context-Aware Access and 2SV work together &mdash; stronger methods required off-network</li>
    </ol>
    <p style="margin-top: 0.75rem;"><strong>References:</strong></p>
    <ul style="margin: 0.25rem 0 0 1.5rem;">
      <li><a href="https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-assignment-network">Microsoft &mdash; Conditional Access with Named Locations</a></li>
      <li><a href="https://support.google.com/a/answer/9275380">Google &mdash; Context-Aware Access</a></li>
    </ul>
  </div>
</div>

<!-- Section 9: SAML Debugging -->

<h2 id="debugging">9. SAML Debugging and Troubleshooting</h2>

<div class="card">
  <p><strong>Essential tool: SAML-tracer.</strong> Install the browser extension before you do anything else: <a href="https://addons.mozilla.org/en-US/firefox/addon/saml-tracer/">Firefox</a> | <a href="https://chromewebstore.google.com/detail/saml-tracer/mhfbofhkdalfnnmhpahndkonakbephkf">Chrome</a>. Open it before attempting login. It intercepts HTTP traffic, detects SAML messages, and decodes them into readable XML. This is how you&rsquo;ll diagnose every SSO problem.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>The Debugging Checklist</h3>
    <ol style="margin: 0.5rem 0 0 1.5rem;">
      <li>Open SAML-tracer</li>
      <li>Attempt the SSO login that&rsquo;s failing</li>
      <li>Find the AuthnRequest (SP to IdP) &mdash; verify <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">Issuer</code> and <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">AssertionConsumerServiceURL</code></li>
      <li>Find the SAML Response (IdP to SP) &mdash; check <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">&lt;StatusCode&gt;</code></li>
      <li>If status is not <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">Success</code>, the IdP rejected the request &mdash; check IdP logs</li>
      <li>If status is <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">Success</code>, inspect the assertion fields (see table below)</li>
    </ol>
  </div>

  <div class="section-item">
    <h3>Assertion Field Checklist</h3>
    <table style="margin-top: 0.5rem;">
      <thead>
        <tr>
          <th>Field</th>
          <th>What to Check</th>
          <th>Common Failure</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Issuer</strong></td>
          <td>Matches the IdP entityID Sierra expects?</td>
          <td>IdP entityID changed or SP misconfigured</td>
        </tr>
        <tr>
          <td><strong>Destination</strong></td>
          <td>Matches Sierra&rsquo;s ACS URL exactly?</td>
          <td>Trailing slash, HTTP vs HTTPS</td>
        </tr>
        <tr>
          <td><strong>Audience</strong></td>
          <td>Matches Sierra&rsquo;s entityID?</td>
          <td>SP entityID mismatch</td>
        </tr>
        <tr>
          <td><strong>NotBefore / NotOnOrAfter</strong></td>
          <td>Timestamps valid relative to Sierra&rsquo;s clock?</td>
          <td><strong>Clock skew</strong></td>
        </tr>
        <tr>
          <td><strong>Recipient</strong></td>
          <td>Matches ACS URL?</td>
          <td>URL mismatch</td>
        </tr>
        <tr>
          <td><strong>Signature</strong></td>
          <td>Validates against IdP certificate?</td>
          <td>Expired cert, cert rotation not applied</td>
        </tr>
        <tr>
          <td><strong>NameID / Attributes</strong></td>
          <td>Contains expected attribute with expected value?</td>
          <td>Wrong attribute name, empty value, case mismatch</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section-item">
    <h3>Common Problems and Fixes</h3>
    <p><strong>Clock Skew</strong></p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Symptom</strong>: &ldquo;Assertion expired&rdquo; or silent login failure</li>
      <li><strong>Cause</strong>: Sierra server&rsquo;s clock differs from IdP by more than the assertion validity window (~5 min)</li>
      <li><strong>Diagnosis</strong>: Compare <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">NotBefore</code>/<code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">NotOnOrAfter</code> in the assertion with Sierra server&rsquo;s time (<code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">date -u</code>)</li>
      <li><strong>Fix</strong>: Ensure NTP is running. On Linux: <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">timedatectl status</code> to verify.</li>
    </ul>
    <p style="margin-top: 0.75rem;"><strong>Certificate Mismatch</strong></p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Symptom</strong>: &ldquo;Signature validation failed&rdquo;</li>
      <li><strong>Cause</strong>: IdP rotated its signing certificate but Sierra still has the old one</li>
      <li><strong>Diagnosis</strong>: Extract cert from the Response&rsquo;s <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">&lt;ds:X509Certificate&gt;</code>, compare with Sierra&rsquo;s config</li>
      <li><strong>Fix</strong>: Re-download IdP metadata and re-import into Sierra. Proactively monitor cert expiry dates.</li>
    </ul>
    <p style="margin-top: 0.75rem;"><strong>ACS URL Mismatch</strong></p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Symptom</strong>: IdP error page, or Response goes nowhere</li>
      <li><strong>Cause</strong>: ACS URL in IdP doesn&rsquo;t exactly match Sierra&rsquo;s actual endpoint</li>
      <li><strong>Watch for</strong>: trailing slashes, HTTP vs HTTPS, port numbers, path case</li>
      <li><strong>Fix</strong>: Copy the ACS URL from Sierra&rsquo;s SP metadata and paste it exactly into IdP config</li>
    </ul>
    <p style="margin-top: 0.75rem;"><strong>Attribute Name Mismatch</strong></p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Symptom</strong>: User authenticates but Sierra says &ldquo;user not found&rdquo; or wrong account</li>
      <li><strong>Cause</strong>: IdP sends <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress</code> but Sierra expects <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">email</code></li>
      <li><strong>Diagnosis</strong>: Inspect <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">&lt;AttributeStatement&gt;</code> in SAML-tracer. Compare attribute <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">Name</code> values with what Sierra expects.</li>
      <li><strong>Fix</strong>: Configure attribute mapping / claim rules in your IdP to send the attribute name Sierra expects.</li>
    </ul>
    <p style="margin-top: 0.75rem;"><strong>SSO ID Case Mismatch</strong></p>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><strong>Symptom</strong>: User authenticates at IdP but Sierra says no matching account</li>
      <li><strong>Cause</strong>: SSO ID in Sierra is <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">JSmith</code> but IdP sends <code style="background: #f5f5f5; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.85rem;">jsmith</code></li>
      <li><strong>Fix</strong>: SSO IDs are <strong>case-sensitive</strong>. Make them match exactly.</li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Command-Line Tools</h3>
    <pre style="background: #f5f5f5; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem; line-height: 1.5;"># Inspect a certificate's details and expiry
openssl x509 -text -noout -in idp-cert.pem

# Verify an XML signature (requires xmlsec1)
xmlsec1 --verify --pubkey-cert-pem idp-cert.pem response.xml

# Decode a base64 SAML message from a URL parameter
echo "PHNhbWxwOl..." | base64 -d | xmllint --format -

# Decode a deflated + base64 SAML message (HTTP-Redirect binding)
echo "fZJNT8Mw..." | base64 -d | python3 -c \
  "import sys,zlib; print(zlib.decompress(sys.stdin.buffer.read(),-15).decode())"</pre>
    <p style="margin-top: 0.75rem;"><strong>References:</strong></p>
    <ul style="margin: 0.25rem 0 0 1.5rem;">
      <li><a href="https://workos.com/blog/saml-assertion-failures-debugging-guide">SAML Assertion Failures Debugging Guide &mdash; WorkOS</a></li>
      <li><a href="https://workos.com/guide/common-saml-errors">Common SAML Errors &mdash; WorkOS</a></li>
      <li><a href="https://github.com/simplesamlphp/SAML-tracer">SAML-tracer on GitHub</a></li>
    </ul>
  </div>
</div>

<!-- Section 10: Links and References -->

<h2 id="references">10. Links and References</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Sierra Documentation (may require customer login)</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sgil/sgil_saml_verification.html">SAML-Based Authentication for Staff &mdash; Overview</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sadmin/sadmin_backend_saml.html">Configuring SAML Authentication</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sadmin/sadmin_backend_saml_addidp.html">Configuring an Identity Provider</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sadmin/sadmin_backend_saml_ssoid.html">Uploading SSO IDs to Staff Accounts</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sadmin/sadmin_backend_saml_enable.html">Enabling SAML Authentication</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sadmin/sadmin_backend_saml_cas.html">Restarting the CAS Server</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sdesktop/sdesktop_logging_in.html">Sierra Desktop Login with SAML</a></li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Polaris SSO Documentation</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><a href="https://documentation.iii.com/polaris/PolarisPDFGuides/PolarisOAuthADFS_7.2.pdf">Polaris OAuth/ADFS Guide (PDF)</a></li>
      <li><a href="https://documentation.iii.com/polaris/PolarisPDFGuides/PolarisOAuthOpenIDConnect_7.3.pdf">Polaris OIDC Guide (PDF)</a></li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Identity Provider Setup</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><a href="https://support.google.com/a/answer/6087519">Google Workspace &mdash; Custom SAML App</a></li>
      <li><a href="https://support.google.com/a/answer/6301076">Google SAML Error Reference</a></li>
      <li><a href="https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso">Microsoft Entra ID &mdash; SAML SSO</a></li>
      <li><a href="https://shibboleth.atlassian.net/wiki/spaces/IDP5/overview">Shibboleth IdP Documentation</a></li>
      <li><a href="https://www.keycloak.org/documentation">Keycloak Documentation</a></li>
    </ul>
  </div>

  <div class="section-item">
    <h3>SAML Protocol</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><a href="https://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html">OASIS SAML V2.0 Technical Overview</a></li>
      <li><a href="https://developer.okta.com/docs/concepts/saml/">Understanding SAML &mdash; Okta Developer</a></li>
    </ul>
  </div>

  <div class="section-item">
    <h3>SCIM / Provisioning</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><a href="https://scim.cloud/">SCIM Protocol Reference</a></li>
      <li><a href="https://developer.okta.com/docs/concepts/scim/">Understanding SCIM &mdash; Okta Developer</a></li>
      <li><a href="https://learn.microsoft.com/en-us/entra/identity/app-provisioning/use-scim-to-provision-users-and-groups">Microsoft Entra SCIM Tutorial</a></li>
    </ul>
  </div>

  <div class="section-item">
    <h3>MFA and Security</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><a href="https://www.cisa.gov/sites/default/files/publications/fact-sheet-implement-number-matching-in-mfa-applications-508c.pdf">CISA &mdash; Implement Number Matching in MFA</a></li>
      <li><a href="https://pages.nist.gov/800-63-4/sp800-63b.html">NIST SP 800-63B &mdash; Digital Identity Guidelines</a></li>
      <li><a href="https://duo.com/docs">Duo Security Documentation</a></li>
      <li><a href="https://www.token2.com/">Token2 Hardware Tokens</a></li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Passwordless / FIDO2</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><a href="https://www.yubico.com/authentication-standards/fido2/">FIDO2 Passwordless &mdash; Yubico</a></li>
      <li><a href="https://docs.yubico.com/software/yubikey/tools/authenticator/auth-guide/fido2.html">YubiKey FIDO2 Guide</a></li>
      <li><a href="https://support.yubico.com/hc/en-us/articles/4402836718866-Understanding-YubiKey-PINs">Understanding YubiKey PINs</a></li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Debugging Tools</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><a href="https://addons.mozilla.org/en-US/firefox/addon/saml-tracer/">SAML-tracer (Firefox)</a></li>
      <li><a href="https://chromewebstore.google.com/detail/saml-tracer/mhfbofhkdalfnnmhpahndkonakbephkf">SAML-tracer (Chrome)</a></li>
      <li><a href="https://www.samltool.com/decode.php">SAML Decoder &mdash; SAMLTool</a></li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Library Identity / Federation</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><a href="https://www.fim4l.org/">FIM4L &mdash; Federated Identity Management for Libraries</a></li>
      <li><a href="https://incommon.org/news/making-federation-work-for-libraries/">InCommon &mdash; Making Federation Work for Libraries</a></li>
    </ul>
  </div>

  <div class="section-item">
    <h3>Community</h3>
    <ul style="margin: 0.5rem 0 0 1.5rem;">
      <li><a href="https://ideas.iii.com">Innovative Idea Exchange</a> &mdash; upvote Justin&rsquo;s upcoming MFA requirement request</li>
      <li><a href="https://forum.innovativeusers.org">IUG Forum</a></li>
    </ul>
  </div>
</div>
