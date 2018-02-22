.PHONY: examples

examples:
	tfu
	@echo
	tfu targets --help
	@echo
	tfu targets elasticsearch.master
	@echo
	tfu nodes --help
	@echo
	tfu nodes nodes.yml elasticsearch.master
	@echo
	tfu nodes -o txt nodes.yml elasticsearch.master
