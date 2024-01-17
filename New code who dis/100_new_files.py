import os
import time

def create_text_files(folder_path, num_files):
    for i in range(1, num_files + 1):
        file_name = f"document_{i}.txt"
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, "w") as file:
            file.write(f"This is text document {i}")
        
        print(f"Created {file_name}")

if __name__ == "__main__":
    current_folder = os.path.abspath(os.getcwd())
    num_documents = 100
    
    create_text_files(current_folder, num_documents)
    
    input("Press enter to exit...")
    # Add a sleep to ensure the program waits before exiting
    time.sleep(1)  # Wait for 1 seconds before exiting
