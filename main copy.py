from utility import utility as util,printing
from OneDrive import OneDrive as OD
from complete_tests import complete_tests
import datetime
import time
import sys
from termcolor import cprint
import json

if len(sys.argv) > 1:
	all_args = [i.lower() for i in sys.argv[1:]]
	while all_args:
		cprint(("_-"*40+"\n")*2,"magenta")
		if all_args[0] == "auto":
			tests = [1,2,3,4,5]
		else:
			tests = [float(i) for i in all_args[0].replace("[","").replace("]","").split(",") ]
		del all_args[0]
		driver = util.set_driver_options(all_args,silent=False)
		try:
			for test in tests:
				if test == 1:
					complete_tests.one_drive_download_test(driver,userId='dtsai')
				elif test == 2:
					complete_tests.summary_list_check(driver)
				elif test == 3:
					complete_tests.name_consistency(driver)
				elif test == 4:
					complete_tests.list_tab_cross_check(driver)
				elif test == 5:
					complete_tests.total_num_items_check(driver)
				elif test == 6:
					OD(num_files=50,pattern=[0,2,3,4])
				elif test == 6.5:
					OD.refresh_file_volumes()
					OD.auto_download(num_files=50,pattern=[0,2,3,4])
				elif test == 7:
					OD.auto_download(volume=1000,pattern=[2,4,3,0])
				elif test == 7.5:
					OD.refresh_file_volumes()
					OD.auto_download(download_volume=1000,pattern=[2,4,3,0])
				elif test == 8:
					OD.refresh_file_volumes()
		finally:
			driver.quit()
else:
	import ast
	with open("refs/input.txt","r") as inf:
		inputs = ast.literal_eval(inf.read())
	userId = (inputs["userId"] if "userId" in inputs else "dtsai")
	assert isinstance(userId,str)

	for driver_specs in inputs["drivers"]:
		cprint(("_-"*40+"\n")*2,"magenta")
		driver = util.set_driver_options(util.convert_driver_inputs(driver_specs),silent=False)
		if driver_specs["tests"] == "default":
			complete_tests.one_drive_download_test(driver,userId='dtsai')
			complete_tests.summary_list_check(driver)
			complete_tests.name_consistency(driver)
			complete_tests.list_tab_cross_check(driver)
			complete_tests.total_num_items_check(driver)
			OD.auto_download(num_files=50,pattern=[2,3,2,4,0])
		else:
			funcs_and_params = [util.convert_test_inputs(test,test["name"])
							for test in driver_specs["tests"]]
			for func, params in funcs_and_params:
				if func != None:
					func((driver, True), params, userId)
		driver.quit()
	cprint("\n"*3+("\/"*40+"\n")*6+"\n"*3,"magenta")
	for test_specs in inputs["tests"]:
		cprint(("_-"*40+"\n")*2,"magenta")
		test_name = test_specs["name"]
		func,params = util.convert_test_inputs(test_specs["params"],test_name)
		if func == None:
			continue
		if test_name == "auto download":
			func(None, params, None)
		else:
			printing.new_test_print(test_name)
			if test_specs['drivers'] == "default":
				driver = util.set_driver_options(["chrome"],silent=False)
				try:
					func((driver, False), params, userId)
				finally:
					driver.quit()
			else:
				for driver_specs in test_specs['drivers']:
					print('-'*70)
					driver = util.set_driver_options(util.convert_driver_inputs(driver_specs),silent=False)
					try:
						func((driver, False), params, userId)
					finally:
						driver.quit()
					print()
