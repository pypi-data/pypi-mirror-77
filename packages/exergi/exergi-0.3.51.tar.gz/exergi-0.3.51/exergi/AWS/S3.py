""" This module defines all exergi functions within the AWS.S3 module"""

def exportFileToS3(obj,bucket: str,key: str) -> None:
    """ This module exports a pandas.DataFrame to specified bucket/key. 

    Keyword Arguments:
        - obj       - Python object to be exported
        - bucket    - S3 export bucket,no trailing / like "stage-data-scientist"
        - key       - S3 export key, no leading "/". String should end with the
                      desired file format. "public/.../example.csv". 
                      Currently supported fileformats are
                        - .csv
                            - pandas.DataFrame()
                        - .xlsx
                            - pandas.DataFrame()
                        - .pkl
                            - pandas.DataFrame()
                        - .h5
                            - pandas.DataFrame()
                        - .npy
                            - numpy (arrays)
    Returns:
        None (Maybe confirmation should be returned in future versions)
    """

    import boto3
    import io
    import pickle
    import os
    import pandas as pd
    import numpy as np
    import tempfile
    import json

    from pandas import ExcelWriter

    # Connect to S3
    s3client = boto3.client("s3")
    s3resource = boto3.resource("s3")   

    # Extra file name, file format and export object type
    _, fileFormat = os.path.splitext(key)
    objClass = obj.__class__.__module__.split(".")[0]
    raiseString = f"Object class {objClass} not supported for {fileFormat} export. - "

    # Comma separated files 
    if fileFormat == ".csv":
        if objClass == "pandas":
            buffer = io.StringIO()
            obj.to_csv(buffer,index=False)    
            s3resource.Object(bucket, key).put(Body=buffer.getvalue()) # pylint: disable=no-member
        else:
            raise Exception(raiseString)

    # Excel files 
    elif fileFormat == ".xlsx":
        if objClass == "pandas":
            with io.BytesIO() as output:
                with ExcelWriter(output) as writer: # pylint: disable=abstract-class-instantiated
                    obj.to_excel(writer)
                data = output.getvalue()
                s3resource.Object(bucket, key).put(Body=data) # pylint: disable=no-member
        else:
            raise Exception(raiseString)

    # Pickle files 
    elif fileFormat == ".pkl":
    
        if objClass == "pandas":
            serializedMyData = pickle.dumps(obj)
            s3resource.Object(bucket, key).put(Body=serializedMyData) # pylint: disable=no-member
        else:
            raise Exception(raiseString)
                
    # HDF5 files 
    elif fileFormat == ".h5":
        if objClass == "pandas":
            with tempfile.NamedTemporaryFile(suffix=".h5") as fp:
                hdf = pd.HDFStore(fp.name)
                hdf.put("/data/d1", obj, format='table', data_columns=True)
                hdf.close()
                fp.seek(0)
                s3resource.Object(bucket, key).put(Body=fp.read()) # pylint: disable=no-member
        else:
            raise Exception(raiseString)

    # npy files 
    elif fileFormat == ".npy":
        if objClass == "numpy":
            with tempfile.TemporaryFile()  as fp:
                np.save(fp,obj) 
                fp.seek(0)
                s3resource.Object(bucket, key).put(Body=fp.read()) # pylint: disable=no-member
        else:
            raise Exception(raiseString)

    
    elif fileFormat == ".npz":

        # If fileFormat = .npz, each column in provided pandas DataFrame will 
        # be exported as one numpy array for each column, compressed to as one 
        # "key-value pair" numpy zip file

        if objClass == "pandas":
            with tempfile.TemporaryFile()  as fp:
                np.savez(fp,**obj.to_dict())
                fp.seek(0)
                s3resource.Object(bucket, key).put(Body=fp.read()) # pylint: disable=no-member
        else:
            raise Exception(raiseString)

    else:
        raise Exception(raiseString)

def importFileFromS3(bucket: str, key: str, objClass: str ="pandas", **kwargs):
    """ This module imports a pandas.DataFrame from specified bucket/key. 

    Arguments:
        - bucket    -   S3 export bucket, no trailing / - "stage-data-scientist"
        - key       -   S3 export key, no leading / . String should end with the
                        desired file format like "public/.../example.csv". 
                        Currently supported fileformats is:
                            - .csv
                                - pandas.DataFrame()
                            - .xlsx
                                - pandas.DataFrame()
                            - .pkl
                                - pandas.DataFrame()
                            - .h5
                                - pandas.DataFrame()
                            - .npy
                                - numpy (array)
                            - .npz
                                - numpy-zip (arrays)        
        - objClass  -   String explaining what object type file should be loaded 
                        as (default = "pandas")
    Keyword Arguments:
        - **kwargs  -   Keyword arguments import function. Import function 
                        varies for each file format: 
                            - .csv  = pd.read_csv()
                            - .xlsx = pd.read_excel()
                            - .pkl  = pd.read_pickle()
                            - .npz  = np.loads()
    Returns:
        - obj       -   Imported 
    """

    import boto3
    import io
    import os
    import pandas as pd
    import numpy as np
    import tempfile

    # Connect to S3
    s3client = boto3.client("s3")

    # Extra file name, file format and export object type
    _, fileFormat = os.path.splitext(key)
    raiseString = "Object class {} not supported for {} import. - ".format(objClass,fileFormat)

    # Get raw data from S3
    S3obj = s3client.get_object(Bucket=bucket,Key=key)
    S3data = S3obj["Body"].read()

    # CSV files 
    if fileFormat == ".csv":
        if objClass == "pandas":
            obj = pd.read_csv(io.BytesIO(S3data),**kwargs)
        else:
            raise Exception(raiseString)

    # Excel files 
    elif fileFormat == ".xlsx":
        if objClass == "pandas":
            obj = pd.read_excel(io.BytesIO(S3data), **kwargs)
        else:
            raise Exception(raiseString)

    # Pickle files 
    elif fileFormat == ".pkl":
        if objClass == "pandas":
            obj = pd.read_pickle(io.BytesIO(S3data), **kwargs)   
        else:
            raise Exception(raiseString)
    
    # HDF5 files 
    elif fileFormat == ".h5":
        if objClass == "pandas":
            with tempfile.NamedTemporaryFile()  as fp:
                s3client.download_fileobj(Bucket=bucket, Key=key,Fileobj=fp)
                fp.seek(0)
                obj = pd.read_hdf(fp.name,"/data/d1")
        else:
            raise Exception(raiseString)

    # npy files 
    elif fileFormat == ".npy":
        if objClass == "numpy":
            with tempfile.NamedTemporaryFile()  as fp:
                s3client.download_fileobj(Bucket=bucket, Key=key,Fileobj=fp)
                fp.seek(0)
                obj = np.load(fp.name)
        else:
            raise Exception(raiseString)

    # npz files 
    elif fileFormat == ".npz":
        if objClass == "numpy":
            with tempfile.NamedTemporaryFile()  as fp:
                s3client.download_fileobj(Bucket=bucket, Key=key,Fileobj=fp)
                fp.seek(0)
                obj = np.load(fp.name)
        else:
            raise Exception(raiseString)
    else:
        raise Exception(raiseString)
    return obj

def listFilesInPath(bucket,prefix,dropSubFolders=True,
                    removePrefix=True,subsetExt=None, removeExt=False,):
    """ List all files (sorted) in the specified bucket and prefix
    
    Arguments:
        - bucket [str]          -   S3 bucket where path i located,
                                    no trailing "/" like "stage-data-scientist"
        - prefix [str]          -   S3 prefix where files should be listed, "/". 
        - dropSubFolders [bool] -   Switch if files in subfolders should 
                                    be dropped (default = True)
        - removePrefix [bool]   -   Switch if strings in listOfFiles should 
                                    have file prefix removed (default = True)
        - subsetExt [str]           String ('.csv','.xlsx',...) to subset file 
                                    extension with. If provided (default = None)
                                    listOfFiles will only return files
                                    with the specified file extension.
        - removeExt [bool]      -   Switch if strings in listOfFiles should 
                                    have file extension ('.csv','.xlsx',...)
                                    removed (default = False)
    Returns:
        - listOfFiles [lst]     -   List of files in bucket-prefix. 
    """
    
    import pandas as pd
    import io
    import boto3
    import os

    # Remove filename from prefix
    if prefix != "":
        prefix = os.path.dirname(prefix)+"/"
        
    # List all keys 
    listOfFiles = []
    for objectSummary in list(boto3.resource("s3").Bucket(bucket).objects.filter(Prefix=prefix))[0:]: # pylint: disable=no-member
        listOfFiles.append(objectSummary.key)
    listOfFiles = [fileName for fileName in listOfFiles if fileName != prefix]
    
    # Drop all files in subfolders
    if dropSubFolders:
        listOfFiles = [fileName for fileName in listOfFiles if (os.path.dirname(fileName) == os.path.dirname(prefix))]
    
    if removePrefix:
        listOfFiles = [fileName.replace(prefix,"") for fileName in listOfFiles]

    # Subset only files ending with provided subsetExt 
    if subsetExt:
        listOfFiles = [fileName for fileName in listOfFiles if subsetExt in fileName]

    # Remove all file extensions 
    if removeExt:
        listOfFiles = [os.path.splitext(fileName)[0] for fileName in listOfFiles]
    
    return sorted(listOfFiles)