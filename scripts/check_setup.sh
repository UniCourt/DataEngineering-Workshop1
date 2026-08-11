#!/usr/bin/env bash
#
# check_setup.sh — Verify that the workshop environment is ready.
#
# Usage:
#   chmod +x scripts/check_setup.sh
#   ./scripts/check_setup.sh
#
# Exit codes:
#   0  All checks passed
#   1  One or more checks failed
#

# NOTE: We intentionally do NOT use "set -e" here. This is a diagnostic script
# that must run every check and show the full report — it should never abort early.
set -u

# ---------------------------------------------------------------------------
# Colors (disabled automatically when stdout is not a terminal)
# ---------------------------------------------------------------------------
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    YELLOW='\033[1;33m'
    BOLD='\033[1m'
    NC='\033[0m' # No Color
else
    GREEN=''
    RED=''
    YELLOW=''
    BOLD=''
    NC=''
fi

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
PASS=0
FAIL=0

pass() {
    PASS=$((PASS + 1))
    echo -e "  ${GREEN}[OK]${NC}   $1"
}

fail() {
    FAIL=$((FAIL + 1))
    echo -e "  ${RED}[FAIL]${NC} $1"
}

warn() {
    echo -e "  ${YELLOW}[WARN]${NC} $1"
}

header() {
    echo ""
    echo -e "${BOLD}$1${NC}"
}

# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

header "Workshop Environment Check"
echo "=============================="

# --- Git -------------------------------------------------------------------
header "1. Git"
if command -v git >/dev/null 2>&1; then
    pass "git: $(git --version 2>&1)"
else
    fail "git is not installed"
fi

# --- Docker ----------------------------------------------------------------
header "2. Docker"
if command -v docker >/dev/null 2>&1; then
    pass "docker: $(docker --version 2>&1)"
else
    fail "docker is not installed"
fi

# --- Docker Compose --------------------------------------------------------
header "3. Docker Compose"
if docker compose version >/dev/null 2>&1; then
    pass "docker compose: $(docker compose version 2>&1)"
elif command -v docker-compose >/dev/null 2>&1; then
    warn "Found legacy docker-compose: $(docker-compose --version 2>&1)"
    warn "Consider upgrading to the Docker Compose plugin (docker compose)"
    PASS=$((PASS + 1))
else
    fail "docker compose is not available"
fi

# --- Python 3 --------------------------------------------------------------
header "4. Python 3"
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    pass "python3: $PYTHON_VERSION"

    # Check minimum version (3.9)
    MINOR=$(python3 -c "import sys; print(sys.version_info.minor)" 2>/dev/null || echo "0")
    if [ "$MINOR" -lt 9 ]; then
        warn "Python 3.9+ is recommended (you have $PYTHON_VERSION)"
    fi
else
    fail "python3 is not installed"
fi

# --- pip3 ------------------------------------------------------------------
header "5. pip3"
if command -v pip3 >/dev/null 2>&1; then
    pass "pip3: $(pip3 --version 2>&1 | head -n 1)"
else
    fail "pip3 is not installed"
fi

# --- Docker daemon ---------------------------------------------------------
header "6. Docker Daemon"
if docker info >/dev/null 2>&1; then
    pass "Docker daemon is running"
else
    fail "Docker daemon is not reachable (is it running? do you have permission?)"
fi

# --- Container execution ---------------------------------------------------
header "7. Docker Container Execution"
if docker run --rm hello-world >/dev/null 2>&1; then
    pass "Successfully ran hello-world container"
else
    fail "Could not run a Docker container"
fi

# --- GitHub SSH (optional) --------------------------------------------------
header "8. GitHub SSH Access (optional)"
SSH_OUTPUT=$(ssh -T git@github.com 2>&1 || true)
if echo "$SSH_OUTPUT" | grep -q "successfully authenticated"; then
    pass "SSH connection to GitHub works"
else
    warn "SSH to GitHub did not succeed — this is optional but recommended"
    warn "Output: $SSH_OUTPUT"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "=============================="
header "Summary"
echo -e "  Passed: ${GREEN}${PASS}${NC}"
if [ "$FAIL" -gt 0 ]; then
    echo -e "  Failed: ${RED}${FAIL}${NC}"
    echo ""
    echo -e "${RED}Some checks failed.${NC} See docs/setup_and_troubleshooting.md for solutions."
    exit 1
else
    echo -e "  Failed: ${GREEN}0${NC}"
    echo ""
    echo -e "${GREEN}Workshop environment looks ready! 🎉${NC}"
    exit 0
fi
