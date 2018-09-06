MKDIR_P_OUTPUT = mkdir -p output

run:
	${MKDIR_P_OUTPUT}
	python -m unittest tests.test.TestCCLog.test_csv > output/run_output.txt

goodcrc:
	${MKDIR_P_OUTPUT}
	python -m unittest tests.test.TestCCLog.test_csv_goodcrc > output/goodcrc_output.txt

init:
	pip install -r requirements.txt

clean:
	rm -rf output/
