import argparse
from translate import GraphParser 
parser = argparse.ArgumentParser()

# Add the arguments to the parser
parser.add_argument("-m", "--mode", help="To specify the mode of the script either i for interactive or empty for file mode") 
parser.add_argument("-f", "--file", help="File to parse in file mode") 

args = parser.parse_args()

def main(file=None):
    if args.mode == "i":
        print("Interactive mode")
        parser = GraphParser()
        parser.interactive_main()
    else:
        print("File mode")
        if args.file:
            file = args.file
        if not file:
            raise ValueError("File not provided")
        parser = GraphParser()
        return parser.main(file)

if __name__ == "__main__":
    main()
    
    