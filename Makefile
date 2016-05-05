PYTHON ?= /usr/bin/env python

clean:
	@ echo "[INFO] Cleaning files: *.pyc"
	@ find . -name "*.pyc" -delete


hadoop-env-config: clean
	@ echo "[INFO] Compiling to binary, hadoop-env-config"
	@ cd $(shell pwd)/hadoop_env_config/; zip --quiet -r ../hadoop-env-config *
	@ echo '#!$(PYTHON)' > hadoop-env-config
	@ mv hadoop-env-config.zip hadoop-env-config
	@ chmod a+x hadoop-env-config
