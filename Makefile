FILENAME?=$(shell git branch --show-current)
.PHONY: adr-new
adr-new:
	@echo "Creating new ADR for $(FILENAME)"
	@cp adrs/00-adr-template.md adrs/$(shell date +%Y-%m-%d)-$(FILENAME).md
	@echo "Created ADR at adrs/$(shell date +%Y-%m-%d)-$(FILENAME).md"
