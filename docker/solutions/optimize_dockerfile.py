#!/usr/bin/env python3
"""
Optimize Dockerfile - Multi-Stage Build
Company: Shopify | Difficulty: Medium

Rewrite Dockerfile using multi-stage build to reduce image size from 800MB to <200MB.
Use Alpine for the final stage and only copy the compiled binary.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


BEFORE_DOCKERFILE = """
# Before: Bloated image (~550MB)
FROM golang:1.21
WORKDIR /app
COPY . .
RUN go build -o myapp .
RUN go install some-dependencies  # Unnecessary in production
ENTRYPOINT ["./myapp"]
# Size: 550MB+
"""

OPTIMIZED_DOCKERFILE = """
# After: Multi-stage build (~45MB)
# Stage 1: Build
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o myapp .

# Stage 2: Runtime
FROM alpine:latest
RUN apk --no-cache add ca-certificates tzdata
WORKDIR /app
COPY --from=builder /app/myapp .
COPY --from=builder /app/config ./config
EXPOSE 8080
ENTRYPOINT ["./myapp"]
# Size: ~45MB (with Alpine)
"""

RUST_BEFORE = """
# Before: Rust with full cargo image
FROM rust:1.70
WORKDIR /app
COPY . .
RUN cargo build --release
RUN strip target/release/myapp
ENTRYPOINT ["target/release/myapp"]
"""

RUST_AFTER = """
# Multi-stage for Rust
FROM rust:1.70-alpine AS builder
RUN apk add --no-cache musl-dev openssl-dev
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release && rm -rf src
RUN strip target/release/myapp

FROM alpine:3.18
RUN apk add --no-cache openssl
COPY --from=builder /app/target/release/myapp /usr/local/bin/
ENTRYPOINT ["myapp"]
"""


def build_optimized_image(dockerfile_path: str = "Dockerfile", tag: str = "myapp:fixed") -> None:
    """
    Build the optimized multi-stage image.

    Args:
        dockerfile_path: Path to Dockerfile
        tag: Tag for the built image
    """
    print(f"Building optimized image: {tag}")
    subprocess.run(
        ["docker", "build", "-f", dockerfile_path, "-t", tag, "."],
        check=True
    )


def check_image_size(image_name: str) -> None:
    """Check image size."""
    result = subprocess.run(
        ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}\t{{.Size}}"],
        capture_output=True,
        text=True
    )
    for line in result.stdout.split("\n"):
        if image_name in line:
            print(f"  {line}")


def main():
    print("Optimize Dockerfile - Multi-Stage Build")
    print("=" * 40)

    print("\n1. BEFORE (bloated ~550MB):")
    print(BEFORE_DOCKERFILE)

    print("\n2. AFTER (optimized ~45MB):")
    print(OPTIMIZED_DOCKERFILE)

    print("\n3. Key optimizations:")
    print("   - Multi-stage builds separate build from runtime")
    print("   - Use alpine:latest for minimal base image")
    print("   - Use CGO_ENABLED=0 for static binaries")
    print("   - Use -ldflags='-w -s' to strip debug symbols")
    print("   - Only copy final binary to runtime stage")

    print("\n4. Build and verify:")
    print("   docker build -t myapp:fixed .")
    print("   docker images myapp")


if __name__ == "__main__":
    main()