#!/usr/bin/env python3
"""
Solution for: Secure Internal Service Communication

Company: Dropbox | Difficulty: Medium

Scenario:
Set up cert-manager with a SelfSigned ClusterIssuer to bootstrap a CA certificate.

Task:
Create a CA Issuer from that CA, then issue a TLS certificate (web-cert)
for DNS names web.preparesh.svc and web.preparesh.svc.cluster.local in
namespace preparesh.

Solution Approach:
- Create SelfSigned ClusterIssuer
- Create a self-signed CA Certificate
- Create a CA Issuer using the CA certificate
- Issue the final TLS certificate from the CA Issuer
"""

import subprocess
import json


def apply_manifest(manifest):
    """Apply a Kubernetes manifest."""
    result = subprocess.run(
        ['kubectl', 'apply', '-f', '-'],
        input=json.dumps(manifest),
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Applied: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def setup_cert_manager():
    """Set up the full cert-manager chain."""

    # Step 1: SelfSigned ClusterIssuer (bootstrap)
    selfsigned_issuer = {
        "apiVersion": "cert-manager.io/v1",
        "kind": "ClusterIssuer",
        "metadata": {"name": "selfsigned-issuer"},
        "spec": {"selfSigned": {}}
    }
    print("1. Creating SelfSigned ClusterIssuer...")
    apply_manifest(selfsigned_issuer)

    # Step 2: CA Certificate (self-signed, used as CA)
    ca_cert = {
        "apiVersion": "cert-manager.io/v1",
        "kind": "Certificate",
        "metadata": {"name": "ca-certificate", "namespace": "preparesh"},
        "spec": {
            "isCA": True,
            "commonName": "ca-certificate",
            "secretName": "ca-key-pair",
            "privateKey": {"algorithm": "RSA", "size": 2048},
            "issuerRef": {
                "name": "selfsigned-issuer",
                "kind": "ClusterIssuer",
                "group": "cert-manager.io"
            }
        }
    }
    print("2. Creating CA Certificate...")
    apply_manifest(ca_cert)

    # Step 3: CA Issuer (uses the CA cert to sign other certs)
    ca_issuer = {
        "apiVersion": "cert-manager.io/v1",
        "kind": "Issuer",
        "metadata": {"name": "ca-issuer", "namespace": "preparesh"},
        "spec": {
            "ca": {"secretName": "ca-key-pair"}
        }
    }
    print("3. Creating CA Issuer...")
    apply_manifest(ca_issuer)

    # Step 4: TLS Certificate for the web service
    web_cert = {
        "apiVersion": "cert-manager.io/v1",
        "kind": "Certificate",
        "metadata": {"name": "web-cert", "namespace": "preparesh"},
        "spec": {
            "secretName": "web-tls",
            "dnsNames": [
                "web.preparesh.svc",
                "web.preparesh.svc.cluster.local"
            ],
            "issuerRef": {
                "name": "ca-issuer",
                "kind": "Issuer",
                "group": "cert-manager.io"
            }
        }
    }
    print("4. Issuing TLS certificate (web-cert)...")
    apply_manifest(web_cert)


def verify():
    """Verify certificates are issued."""
    result = subprocess.run(
        ['kubectl', 'get', 'certificate', '-n', 'preparesh'],
        capture_output=True, text=True
    )
    print(f"\nCertificates:\n{result.stdout}")

    result = subprocess.run(
        ['kubectl', 'get', 'secret', 'web-tls', '-n', 'preparesh'],
        capture_output=True, text=True
    )
    print(f"TLS Secret:\n{result.stdout}")

    result = subprocess.run(
        ['kubectl', 'get', 'clusterissuer', 'issuer', '-n', 'preparesh'],
        capture_output=True, text=True
    )
    print(f"Issuers:\n{result.stdout}")


def main():
    print("=== Secure Internal Service Communication ===\n")

    subprocess.run(['kubectl', 'create', 'namespace', 'preparesh'],
                   capture_output=True, text=True)

    print("Setting up cert-manager chain...\n")
    setup_cert_manager()

    print("\nVerifying...")
    verify()

    print("\nChain: SelfSigned Issuer -> CA Certificate -> CA Issuer -> web-cert")


if __name__ == '__main__':
    main()
