all:
	@echo "make run -- run program"
	@echo "make db  -- init database"

run:
	python -m cfhqd

db:
	python -m cfhqd.db
