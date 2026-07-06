# Security Policy

## Supported Versions

This is a Proof-of-Concept project. Security updates are applied to the main branch.

## Reporting a Vulnerability

If you discover a security vulnerability in Ecovilance, please open an issue on GitHub or contact me directly.

## Security Considerations

### Current Limitations (Known for PoC)
- Storage: Data is stored in a local CSV file. In production, this should be replaced with an immutable database or blockchain.
- Authentication: No digital signatures are used. The system proves data wasn't tampered with, but not WHO logged it.
- API Security: Uses HTTP (not HTTPS) for API calls. Production should enforce TLS.
- Access Control: No authentication/authorization for the audit script.

### Future Enhancements
- RSA/ECDSA digital signatures for non-repudiation
- Migration to immutable storage (e.g., IPFS, blockchain)
- HTTPS enforcement for all API communications
- Role-based access control for audit functions