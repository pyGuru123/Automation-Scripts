from docx import Document

doc = Document("test.docx")

replace_dict = dict()
sample = input("Enter sample value : ")
edit = input("Enter edit value : ")

replace_dict['sample'] = sample
replace_dict['edit'] = edit

for key in replace_dict.keys():
	for para in doc.paragraphs:
		if para.text.find(key) >= 0:
			para.text = para.text.replace(key, replace_dict[key])

doc.save("replaced.docx")