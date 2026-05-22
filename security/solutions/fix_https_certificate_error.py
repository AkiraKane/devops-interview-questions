#!/usr/bin/env python3
"""
Fix HTTPS Certificate Error
Company: Github | Difficulty: Medium

Generate self-signed SSL certificate with Subject Alternative Name (SAN)
for IP 127.0.0.1 to fix hostname verification failures.
"""

from __future__ import annotations

import subprocess
import os
import tempfile
from pathlib import Path


def generate_certificate_with_san(
    output_key: str = "server.key",
    output_crt: str = "server.crt",
    ip_address: str = "127.0.0.1",
    common_name: str = "example"
) -> None:
    """
    Generate self-signed certificate with SAN for local IP.

    Args:
        output_key: Output private key file
        output_crt: Output certificate file
        ip_address: IP address for SAN
        common_name: CN for the certificate
    """
    # Create OpenSSL config with SAN
    config = f"""[req]
default_bits        = 2048
prompt             = no
default_md         = sha256
x509_extensions    = v3_req
distinguished_name  = dn

[dn]
CN = {common_name}

[v3_req]
basicConstraints    = CA:FALSE
keyUsage            = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage    = serverAuth
subjectAltName      = @alt_names

[alt_names]
IP.1 = {ip_address}
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.cnf', delete=False) as f:
        f.write(config)
        config_file = f.name

    try:
        # Generate key
        subprocess.run(
            ["openssl", "genrsa", "-out", output_key, "2048"],
            check=True,
            capture_output=True
        )

        # Generate certificate with SAN
        subprocess.run([
            "openssl", "req", "-new", "-x509",
            "-key", output_key,
            "-out", output_crt,
            "-days", "365",
            "-config", config_file
        ], check=True, capture_output=True)

        print(f"Created {output_key} and {output_crt} with SAN for IP:{ip_address}")

    finally:
        os.unlink(config_file)


def verify_certificate_san(cert_file: str) -> None:
    """Verify the certificate has SAN for 127.0.0.1."""
    result = subprocess.run(
        ["openssl", "x509", "-in", cert_file, "-noout", "-text"],
        capture_output=True,
        text=True
    )

    # Extract and print SAN
    lines = result.stdout.split("\n")
    in_san = False
    for line in lines:
        if "Subject Alternative Name" in line:
            in_san = True
        elif in_san:
            print(f"  {line.strip()}")
            if line.strip() and not line.strip().startswith("IP:"):
                in_san = False


def main():
    print("Fix HTTPS Certificate Error")
    print("=" * 28)

    print("\n1. Generate certificate with SAN for IP:127.0.0.1:")
    print("   openssl req -x509 -newkey rsa:2048 -keyout server.key \\")
    print("     -out server.crt -days 365 -nodes \\")
    print("     -subj '/CN=example' \\")
    print("     -addext 'subjectAltName=IP:127.0.0.1'")
    print()
    generate_certificate_with_san()

    print("\n2. Verify certificate has SAN:")
    print("   openssl x509 -in server.crt -noout -text | grep -A2 'Subject Alternative'")
    verify_certificate_san("server.crt")

    print("\n3. Test with curl:")
    print("   curl -v https://127.0.0.1:8443")


if __name__ == "__main__":
    main()