.PHONY: run


# 默认值
in ?= ""
out ?= /fuzz_output
cmd ?= ""
stg ?= COVERAGE


# 运行命令
run:
	@CMD="python3 ./src/main.py"; \
	if [ "$(in)" != "" ]; then \
		CMD="$${CMD} -i $(in)"; \
	fi; \
	if [ "$(out)" != "" ]; then \
		CMD="$${CMD} -o $(out)"; \
	fi; \
	if [ "$(cmd)" != "" ]; then \
		CMD="$${CMD} --cmd=\"$(cmd)\""; \
	fi; \
    if [ "$(stg)" != "" ]; then \
		CMD="$${CMD} -s $(stg)"; \
	fi; \
	echo "Executing: $$CMD"; \
	$$CMD