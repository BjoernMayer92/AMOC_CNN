PROJECT_NAME = CNN
REPO_NAME = cnn

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif


initialize_git:
	@echo "Initalizing git ... "
	git init
	git add .
	git commit -m "initial commit"

activate:
	@echo "Activating virtual environment..."
	source activate $(PROJECT_NAME)

create_environment:
ifeq (True,$(HAS_CONDA))
	conda env create -f requirements.yml
endif
@echo "New conda env created. Activate with: \nsource activate $(ROJECT_NAME)"

update_environment:
	conda env update --file requirements.yml

delete_environment:
	conda env remove -n $(PROJECT_NAME)

lint:
	flake8 src

setup: initialize_git create_environment
