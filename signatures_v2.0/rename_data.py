import os 

path = "C:/Users/User/Desktop/Desktop/SIGNATURE_v2.0/prepare_data/signatures"

def main():      
    for foldername in os.listdir(path):
        i = 0
        for filename in os.listdir(path + '/' + foldername):
            author = foldername
            new_name = author + '.' + str(i) + '.png'
            current_path = path + '/' + foldername + '/'
            src = current_path + filename
            rf = current_path + new_name
            os.rename(src, rf) 
            i += 1
  
if __name__ == '__main__': 
    main() 