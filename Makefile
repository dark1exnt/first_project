PY_SRCS=booking config

.PHONY: help install lint fmt type security cc mi hal raw check

help:
	@echo "Доступные цели:"
	@echo " lint - ruff check (с автофиксом)"
	@echo " fmt - ruff format"
	@echo " type - mypy (проверка типов)"
	@echo " security - bandit (скан безопасности)"
	@echo " cc - radon cc (цикломатическая сложность) + quality gate"
	@echo " mi - radon mi (индекс поддерживаемости) + quality gate"
	@echo " hal - radon hal (метрика халстеда)"
	@echo " raw - radon raw (SLOC, LLOC, комментарии, число функций/классов)"
	@echo " check - быстрый локальный quality gate (ruff+mypy+bandit+radon)"

# Ruff
lint:
	poetry run ruff check $(PY_SRCS) --fix

fmt:
	poetry run ruff format $(PY_SRCS)

# Mypy
type:
	poetry run mypy $(PY_SRCS)

# Bandit
security:
	poetry run bandit -r $(PY_SRCS) -lll -x migrations

# Radon
cc:
	poetry run radon cc -s -a $(PY_SRCS)
	@# QUALITY GATE: проваливаем, если есть элементы со сложностью E/F
	@if poetry run radon cc -s $(PY_SRCS) | grep -E '\- [EF] '; then \
		echo "❌ Radon CC: обнаружены функции со сложностью E/F"; \
		exit 1; \
	else \
		echo "✅ Radon CC: нет функций с E/F"; \
	fi

mi:
	poetry run radon mi $(PY_SRCS)

hal:
	poetry run radon hal $(PY_SRCS)

raw:
	poetry run radon raw $(PY_SRCS)

# Полный прогон
check: lint fmt type security cc hal raw