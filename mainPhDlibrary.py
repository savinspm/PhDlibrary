from argparse import ArgumentParser
import os
import sys
import socket
import time

# ENVIOREMENT VARIABLES
def loadENVIROMENTVARIABLES():
    machine = socket.gethostname()
    print("Estas en la maquina: ", machine)

    if "Savins" in machine or "edu" in machine:
        os.environ["SPM_machine"] = "laptopSavins"
        loadLaptopSavins()
    else:
        os.environ["SPM_machine"] = "bullxual"


def loadLaptopSavins():
    print("Loading MacBookSavins Enviorement Variables")
    os.environ["SPM_SAVINSPHD_PATH"] = "/Users/savins/repositorios/PhDlibrary/PhDlibrary"
    os.environ["SPM_ROOT_PATH"] = "/Users/savins/repositorios/PhDlibrary/PhDlibrary"
    os.environ["SPM_FDA_PATH"] = "/Users/savins/repositorios/PhDlibrary/PhDlibrary/DB/test1"

def loadBullxual():
    print("Loading Bullxual Enviorement Variables")
    os.environ["SPM_SAVINSPHD_PATH"] = "/Users/savins/repositorios/PhDlibrary/PhDlibrary"
    os.environ["SPM_ROOT_PATH"] = "/Users/savins/repositorios/PhDlibrary/PhDlibrary"
    os.environ["SPM_FDA_PATH"] = "/Users/savins/repositorios/PhDlibrary/PhDlibrary/DB/test1"

loadENVIROMENTVARIABLES()

os.environ["savinsPHD_path"] = os.getcwd()

######END
import PhDlibrary


if __name__ == "__main__":
    # ArgumentParser con una descripcion de la aplicacion
    parser = ArgumentParser(description='%(prog)s controla toda la experimentacion de la tesis de Savins.')
    SAVINSList = ["savins", "scp_bull", "scp_polonia"]
    GENERACIONlist = ['generate_FDA_ROCS']
    PROCESSlist = ["process_FDA_ROCS"]
    DataframeList = ["join_dataframe", "sort_csv"]
    DatabaseList = ["splitDatabase"]
    
    optionArgument = SAVINSList + GENERACIONlist + PROCESSlist +DataframeList + DatabaseList 
    parser.add_argument("function", nargs="?", choices=optionArgument)
    
    args, sub_args = parser.parse_known_args()
        
    ##########################
    ## GENERATION
    #########################
    if args.function == "generate_FDA_ROCS":
        PhDlibrary.Generation.generate_FDA_ROCS()
    #########################
    ## PROCESS
    #########################
    elif args.function == "procesar_FDA_ROCS":
        parser = ArgumentParser(description="Procesa los resultados de FDA obtenidos por OptiPharm.")
        parser.add_argument('-ipath', required=True,help='Directorio de entrada')
        args = parser.parse_args(sub_args)
        PhDlibrary.Process.procesar_FDA_ROCS(args.ipath)
    
    ##########################
    ## DATAFRAME
    ##########################
    elif args.function == "join_dataframe":
        parser = ArgumentParser(description="Une experimentos en un unico archivo.")
        parser.add_argument('-csvs',nargs='+',help='csv que se quieren combinar')
        args = parser.parse_args(sub_args)
        PhDlibrary.Dataframe.join_dataframe(args.csvs)
    elif args.function == "sort_csv":
        parser = ArgumentParser(description="Ordena un csv mediante una columna.")
        parser.add_argument('-csvs',nargs='+',help='csv que se quieren combinar')
        parser.add_argument('-by', required=True,help='columna por la que se ordena')
        parser.add_argument('-asc', required=True,type=int, help='orden ascendente')
        args = parser.parse_args(sub_args)
        PhDlibrary.Dataframe.sort_dataframe(args.csvs, args.by, args.asc)

    ##########################
    ## DATABASE
    ##########################
    elif args.function == "splitDatabase":
        parser = ArgumentParser(description="Divide una base de datos en tantos archivos como moleculas tenga la base de datos.")
        parser.add_argument('-input', required=True,help='Directorio de entrada')
        parser.add_argument('-output', required=True,help='Directorio de entrada')
        args = parser.parse_args(sub_args)
        PhDlibrary.Database.splitDatabase(args.input, args.output)
        
    else:
        print("\nGENERATION methods:")
        for item in GENERACIONlist:
            print("\t", item)
        print("\nPROCESS methods: ")
        for item in PROCESSlist:
            print("\t", item)
        print("\nDataframeList methods: ")
        for item in DataframeList:
            print("\t", item)
        print("\nDataBase methods: ")
        for item in DatabaseList:
            print("\t", item)  
 