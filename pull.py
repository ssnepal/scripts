import os

rootdir = os.getcwd()
count = 1
failed = 0
for folder in os.listdir():
    if os.path.isdir(folder):
        try:
            os.chdir(folder)
            os.system("git pull origin master")
            print(count,"dir completed")
            os.chdir(rootdir)
        except Exception as e:
            failed += 1
            print("Some error occured",count,"folder completed", e)
        else:
            if failed == 0:
                print('All',count,'folder succesfully completed')
            count += 1
