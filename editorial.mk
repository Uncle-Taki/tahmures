# Tahmures editorial validation targets.
# Add this line to the repository root Makefile:
#
#   -include editorial.mk

PYTHON ?= python3

.PHONY: editorial-check
.PHONY: validate-reference-parity
.PHONY: validate-protected-parity
.PHONY: validate-fa-editorial
.PHONY: validate-editorial-status

validate-reference-parity:
	$(PYTHON) scripts/validate_reference_parity.py

validate-protected-parity:
	$(PYTHON) scripts/validate_protected_parity.py

validate-fa-editorial:
	$(PYTHON) scripts/validate_fa_editorial.py

validate-editorial-status:
	$(PYTHON) scripts/validate_editorial_status.py

editorial-check:
	$(PYTHON) scripts/editorial_check.py
