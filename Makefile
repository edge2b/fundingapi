gen-doc:
	swagger-codegen generate -i api/api.yaml -l html2 -o api/

gen-schema:
	rm -f fundingapi/schema/jsonschema.py
	venv/bin/python -mfundingapi.schema --source api/api.yaml  --destination fundingapi/schema/jsonschema.py

test: venv
	venv/bin/pytest -s -v --flake8

tarantool:
	mkdir -p data && cd data && ../scripts/tarantool.lua

venv:
	virtualenv --python=python3 venv
	venv/bin/pip install -r requirements.txt

api/swagger-editor:
	@echo install swagger editor
	@wget -q https://github.com/swagger-api/swagger-editor/releases/download/v2.10.4/swagger-editor.zip -O - | tar -xvf - -C api/
	@ln -sf ../../api.yaml api/swagger-editor/spec-files/
	@cp api/swagger_editor_config.json api/swagger-editor/config/defaults.json

api/node_modules:
	@echo install http-server
	@cd api && npm install

open-doc: api/swagger-editor api/node_modules
	@echo open browser to http://127.0.0.1:8081/
	@./api/node_modules/.bin/http-server api/swagger-editor
