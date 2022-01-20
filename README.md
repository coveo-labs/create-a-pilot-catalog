This example shows how you (could) prepare for a Pilot/POC project with an ECommerce catalog.

# Getting Started
Get the data.

## Prepare your index
You can start by using this guide: [Coveo101Commerce](https://github.com/coveo/Coveo101Commerce/tree/master/_Setup).


## Settings
All the settings for the scripts are in `settings.json`. And `EXAMPLE_settings.json` is available.

# Get the data
## 1. Examine the data.
How is the data structured. Does it already contain JSON? Or do you need to transform it into JSON?

### Consume directly JSON
When you already have JSON files, you can proceed to the next step.

### Transform into JSON
In the [example](1. getData.py) you will see that we transform from CSV to JSON.
The example here contained 2 files: one with Products, and one with Attributes. During the above process we combine the 2 into a single JSON.

#### Specific for Endeca Dump data
Endeca has .DAT (flat files, single line content) dump files available. We could index those (will take a long time to transform from that format to JSON first!!!!).
Their files look like:
```
articleLifecycleStatus|60
baseUnitOfMeasure|EA
```
Metadata name + value.
`EOR` specifies a new record.

From endeca to JSON:
[endeca getData](ENDECA_1_getData.py) transforms Endeca export files into JSON files. It checkes for a specific key in one of the columns, if it is found the associate JSON is updated.

From JSON to batch files:
[endeca createPages](ENDECA_2_createPages.py) creates the JSON for the Push/Stream API. It also loads the Taxonomy tree from Endeca for Catalog lookup.


## 2. Create the JSON for the Fields API
You probably have a lot of custom fields. Using the [script](2. createFieldsJSON.py) you can create a `fields.json` file. The contents of the file can be used to push them to your index using [api](https://platform.cloud.coveo.com/docs?urls.primaryName=Field#/Fields/rest_organizations_paramId_indexes_fields_batch_create_post).

** Warning: remove the `Body` mapping on your source (it overrides the quickview) **


## 3. Process the data to JSON for the Push/Stream API
Using [script](3. createBatchFiles.py) will format the JSON for our index and push them into the `batch` directory.
Adjust the file accordingly.
By default all metadata in the json is formatted like `p_nameofthefield`. All metadata is also added to the quickview of the document.


## 4. Push the content to the index
Once the batches are created. Use [script](4. pushBatches.py) to push the content to the index.

# Create the UI
Clonse this repo: You can start by using this guide: [Coveo101Commerce](https://github.com/coveo/Coveo101Commerce/tree/master/_Setup).

## Make changes
Create your API keys and put them in `next.config.js`. Make sure that all fields are also listed in this file.

## Test locally
Now test locally using:
```cmd
npm install
npm run dev
```

## Change your serverless.yml
Save this:
```yml
generic[YOURNAME]StoreApp:
  component: "@sls-next/serverless-component"
  inputs:
    name:
      defaultLambda: [YOURNAME]-store-default
      apiLambda: [YOURNAME]-store-api
    bucketName: [YOURNAME]-commerce-store-assets-dev

```

in directory: `Coveo101Commerce`.
Rename `[YOURNAME]` to your own `Name`.

## Deploy
Test locally first:
`npm install serverless`
then:
`node node_modules\serverless\bin\serverless.js`

Copy the URL for testing.
