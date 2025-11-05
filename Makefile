    .PHONY: check wheel deb rpm exe clean

    check:
	python -m compileall -q src

    wheel:
	rm -rf dist && mkdir -p dist
	python -m pip install -U build
	python -m build

    deb:
	fpm -s dir -t deb -n gsh-prizma-cdsauav -v 1.2.4r1 --prefix /opt/gsh-prizma 	  --after-install packaging/postinst.sh 	  --description "GSH Prizma Gen3 CDSA UAV" 	  src run_dev_verbose.sh

    rpm:
	fpm -s dir -t rpm -n gsh-prizma-cdsauav -v 1.2.4r1 --prefix /opt/gsh-prizma 	  --after-install packaging/postinst.sh 	  --description "GSH Prizma Gen3 CDSA UAV" 	  src run_dev_verbose.sh

    exe:
	python -m pip install -U pyinstaller
	pyinstaller --noconfirm --noconsole -n GSHPrizmaCDSAUAV src/gsh_prizma/ui/app.py

    clean:
	rm -rf build dist __pycache__ *.spec
