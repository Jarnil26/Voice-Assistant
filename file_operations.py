import os

def search_and_open_file(drive, file_name):
    print(f"Searching for '{file_name}' in {drive}...")
    found_files = []
    
    for root, dirs, files in os.walk(drive):
        if file_name in files:
            found_files.append(os.path.join(root, file_name))
    
    if found_files:
        print("\nFile(s) found:")
        for idx, file in enumerate(found_files, start=1):
            print(f"{idx}: {file}")
        print("\nOpening the first found file...")
        os.startfile(found_files[0]) 
    else:
        print("\nFile not found.")

def search_and_delet_file(drive,file_name):
    print(f"Searching for '{file_name}' in {drive}...")
    found_files = []
    
    for root, dirs, files in os.walk(drive):
        if file_name in files:
            found_files.append(os.path.join(root, file_name))
    
    if found_files:
        print("\nFile(s) found:")
        for idx, file in enumerate(found_files, start=1):
            print(f"{idx}: {file}")
        os.remove(found_files[0]) 
        print(f"\n File{found_files[0]} is Deleted..")
    else:
        print("\nFile not found.")

def search_and_open_foldr(folder_name,drive="D:\\"):
    try:
        found_folders = []
        
        for root, dirs, files in os.walk(drive):
            if folder_name in dirs:
                found_folders.append(os.path.join(root, folder_name))
        
        if found_folders:
            first_found_folder = found_folders[0]
            os.startfile(first_found_folder)
            print(f"Opened folder: {first_found_folder}")
        else:
            print(f"Folder '{folder_name}' not found on drive {drive}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
