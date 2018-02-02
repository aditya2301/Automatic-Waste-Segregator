import dropbox,os,time


while True:
	os.system("cls")
	time.sleep(10)
	with open("database.txt","r")as f:
		database=f.readlines()
	#print(database)

	dbx=dropbox.Dropbox('jj41foGWJMAAAAAAAAABdqzHTaTtQxJ7DEcKxciKPbYayZ0laFfGepQr_2m9XMxa')
	#dbx.users_get_current_account()
	files=dbx.files_list_folder('/imageFiles').entries

	for i in files:
		#print(i.name)
		if i.name+"\n" not in database and ((i.name).endswith("jpeg")==True or (i.name).endswith("jpg")==True):
			print("downloading file . . "+i.name)
			dbx.files_download_to_file("C:\\Users\\Boudhayan Dev\\Desktop\\dropboxImage\\"+i.name,"/imageFiles/"+i.name,rev=None)
			print("Starting image recognition . . .")
			while os.path.exists(os.getcwd()+"\\"+i.name)==False:
				continue

			os.system("python -m scripts.label_image --graph=tf_files/retrained_graph.pb --image="+i.name)

			print("Updating database and retrieving the category !")
			with open("imageClassifierResult.txt","r")as f:
				data=f.readlines()
				if data[-1]=="\n":
					data=data[-2]
				else:
					data=data[-1]

				temp=data
				name=data.split()
				name=name[0]

				with open("database.txt","a")as d:
						d.write(name+"\n")

			os.system("cls")
			print(temp)


	with open("imageClassifierResult.txt","rb")as f:
		file=f.read()
	dbx.files_upload(file, "/imageFiles/imageClassifierResult.txt", mode=dropbox.files.WriteMode.overwrite)