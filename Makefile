LUIGI=python2 -m luigi --module all_luigi_tasks AllLuigiTasks
LUIGI_DEV_ARGS=--local-scheduler

run:
	$(LUIGI)

rundev:
	$(LUIGI) $(LUIGI_DEV_ARGS)

server:
	@pgrep luigid && echo "luigid is already running" || { nohup luigid & }

setup:
	pip install -r requirements.txt
