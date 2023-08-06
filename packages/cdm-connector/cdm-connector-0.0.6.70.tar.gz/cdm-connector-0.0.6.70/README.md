# skypoint-python-cdm-connector
Python Spark CDM Connector by SkyPoint. 

Apache Spark connector for the Microsoft Azure "Common Data Model". Reading and writing is supported and it is a work in progress. Please file issues for any bugs that you find. 

For more information about the Azure Common Data Model, check out [this page](https://docs.microsoft.com/en-us/common-data-model/data-lake). <br>

We support Azure Data Lake Service (ADLS) and AWS S3 as storage, historical data preservation using snapshots of the schema & data files and usage within PySpark, Azure Functions etc.  

*Upcoming Support for incremental data refresh handling, [CDM 1.1](https://docs.microsoft.com/en-us/common-data-model/cdm-manifest and Google Cloud (Cloud Storage). <br>

## Example

1. Please look into the sample usage file skypoint_python_cdm.py
2. Dynamically add/remove entities, annotations and attributes
3. Pass Reader and Writer object for any storage account you like to write/read data to/from.
4. Check out the below code for basic read and write examples.

```python
# Initialize empty model
m = Model()

# Sample dataframe
df = {"country": ["Brazil", "Russia", "India", "China", "South Africa", "ParaSF"],
       "currentTime": [datetime.now(), datetime.now(), datetime.now(), datetime.now(), datetime.now(), datetime.now()],
       "area": [8.516, 17.10, 3.286, 9.597, 1.221, 2.222],
       "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria", "ParaSF"],
       "population": [200.4, 143.5, 1252, 1357, 52.98, 12.34] }
df = pd.DataFrame(df)

# Generate entity from the dataframe
entity = Model.generate_entity(df, "customEntity")

# Add generated entity to model
m.add_entity(entity)

# Add model level annotation
# Annotation can be added at entity level as well as attribute level
Model.add_annotation("modelJsonAnnotation", "modelJsonAnnotationValue", m)


# Create an ADLSWriter to write into ADLS
writer = ADLSWriter("ACCOUNT_NAME", "ACCOUNT_KEY",
                     "CONTAINER_NAME", "STORAGE_NAME", "DATAFLOW_NAME")    

# Write data as well as model.json in ADLS storage
m.write_to_storage("customEntity", df, writer)
```

## Contributing

This project welcomes contributions and suggestions. 

## References

[Model.json version1 schema](https://github.com/microsoft/CDM/blob/master/docs/schema/modeljsonschema.json)

[A clean implementation for Python Objects from/to model.json file](https://github.com/Azure-Samples/cdm-azure-data-services-integration/blob/master/CDM/python/CdmModel.py)
