
def main():
    file_path = "requirements.txt"

    data_lines = []
    with open(file_path,"r") as f:
        for line in f:
            l = line.split("==")[0]
            data_lines.append(l)
    
    with open("requirements_cleaned.txt","w") as f:
        for line in data_lines:
            f.write(line+"\n")

if __name__=="__main__":
    main()