# Intend to generate htmls for rapid UI development in vanilla javascript.


# starting with inputs for forms
# 	Form:
	Form,<endpoint>,<method>,enctype="multipart/form-data"
	datepicker,<keyword>,<key phrase>,required
	timepicker,<keyword>,<key phrase>,min=,max=
	editbox, <keyword>, <key phrase>,required minlength="3" maxlength="15"
	optionbox,<keyword>, <key phrase>,required, option 1, option 2, option 3
	numberbox,<keyword>, <key phrase>,required min="15" max="30" placeholder="18"

# We may eventually want
#	tabs
#	side popups
# At some point you will want to fit multi of these on 1 UI page.

# run:
	python generate-html.py
	# it will then generate off of inputs.csv file data

