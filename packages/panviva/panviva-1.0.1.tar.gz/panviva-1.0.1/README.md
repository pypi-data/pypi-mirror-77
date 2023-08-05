# toolkit-python-sdk
Wouldn't it be great if you could share information seamlessly? This connector allows you to push your knowledge further and consume a complete list of Panviva's API offerings.  **Content APIs** perform resource related operations , e.g. `document`, `folder`, `file`, `container`, `image`.  **Live APIs** enable real-time communications with online users on our client application.  **Artefact APIs** interact with curated Panviva content, created by the Digital Orchestrator.

For more information, please visit [https://www.panviva.com/support](https://www.panviva.com/support)

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/panviva/toolkit-python-sdk.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/panviva/toolkit-python-sdk.git`)

Then import the package:
```python
import panviva 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import panviva
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import panviva
from panviva.rest import ApiException
from pprint import pprint

# Configure API key authorization: apiKeyHeader
configuration = panviva.Configuration()
configuration.api_key['Ocp-Apim-Subscription-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Ocp-Apim-Subscription-Key'] = 'Bearer'

# create an instance of the API class
api_instance = panviva.OperationsApi(panviva.ApiClient(configuration))
instance = 'instance_example' # str | The instance name as shown on the Panviva Developer Portal.
simplequery = 'simplequery_example' # str | Natural language query string. For example: ```Action Movies```. (Note: Use simplequery OR advancedquery, not both.) (optional)
advancedquery = 'advancedquery_example' # str | Query string written in Lucene query syntax. For example: ```films AND \"a story\"```. (Note: Use simplequery OR advancedquery, not both.) (optional)
filter = 'filter_example' # str | Accepts a Lucene-formatted filter string. Examples: ```category eq 'Mortgages'```, ```panvivaDocumentVersion gt '8'```. (Filterable fields include dateCreated, dateModified, dateDeleted, categoryJson, queryVariationsJson, title, category, primaryQuery, isDeleted, timestamp, panvivaDocumentId, panvivaDocumentVersion, id) (optional)
channel = 'channel_example' # str | Return response for a specific channel, instead of the default (optional)
page_offset = 56 # int | The pagination offset to denote the number of initial search results to skip. For example, pageOffset of 100 and pageLimit of 10 would return records 101-110. (optional)
page_limit = 56 # int | The number of records to return. Must be an integer between 0 and 1000. (optional)
facet = 'facet_example' # str | Accepts a Lucene-formatted facet string. Examples: ```facet=Category,count:10&amp;facet=Rating```. (Facetable fields include metaData/values) (optional)

try:
    # Search Artefacts
    api_response = api_instance.operations_artefact_nls(instance, simplequery=simplequery, advancedquery=advancedquery, filter=filter, channel=channel, page_offset=page_offset, page_limit=page_limit, facet=facet)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OperationsApi->operations_artefact_nls: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://api.panviva.com/v3*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*OperationsApi* | [**operations_artefact_nls**](docs/OperationsApi.md#operations_artefact_nls) | **GET** /{instance}/operations/artefact/nls | Search Artefacts
*OperationsApi* | [**operations_live_csh**](docs/OperationsApi.md#operations_live_csh) | **POST** /{instance}/operations/live/csh | Live CSH
*OperationsApi* | [**operations_live_document**](docs/OperationsApi.md#operations_live_document) | **POST** /{instance}/operations/live/document | Live Document
*OperationsApi* | [**operations_live_search**](docs/OperationsApi.md#operations_live_search) | **POST** /{instance}/operations/live/search | Live Search
*OperationsApi* | [**operations_search**](docs/OperationsApi.md#operations_search) | **GET** /{instance}/operations/search | Search
*ResourcesApi* | [**resources_artefact_by_id**](docs/ResourcesApi.md#resources_artefact_by_id) | **GET** /{instance}/resources/artefact/{id} | Artefact
*ResourcesApi* | [**resources_artefact_categories_get**](docs/ResourcesApi.md#resources_artefact_categories_get) | **GET** /{instance}/resources/artefactcategory | Get Artefact Categories
*ResourcesApi* | [**resources_artefact_category_post**](docs/ResourcesApi.md#resources_artefact_category_post) | **POST** /{instance}/resources/artefactcategory | Create Artefact Category
*ResourcesApi* | [**resources_container_by_id**](docs/ResourcesApi.md#resources_container_by_id) | **GET** /{instance}/resources/container/{id} | Container
*ResourcesApi* | [**resources_document_by_id**](docs/ResourcesApi.md#resources_document_by_id) | **GET** /{instance}/resources/document/{id} | Document
*ResourcesApi* | [**resources_document_by_id_containers**](docs/ResourcesApi.md#resources_document_by_id_containers) | **GET** /{instance}/resources/document/{id}/containers | Document Containers
*ResourcesApi* | [**resources_document_by_id_containers_relationships**](docs/ResourcesApi.md#resources_document_by_id_containers_relationships) | **GET** /{instance}/resources/document/{id}/containers/relationships | Document Container Relationships
*ResourcesApi* | [**resources_document_by_id_translations**](docs/ResourcesApi.md#resources_document_by_id_translations) | **GET** /{instance}/resources/document/{id}/translations | Document Translations
*ResourcesApi* | [**resources_file_by_id**](docs/ResourcesApi.md#resources_file_by_id) | **GET** /{instance}/resources/file/{id} | File
*ResourcesApi* | [**resources_folder_by_id**](docs/ResourcesApi.md#resources_folder_by_id) | **GET** /{instance}/resources/folder/{id} | Folder
*ResourcesApi* | [**resources_folder_by_id_children**](docs/ResourcesApi.md#resources_folder_by_id_children) | **GET** /{instance}/resources/folder/{id}/children | Folder Children
*ResourcesApi* | [**resources_folder_by_id_translations**](docs/ResourcesApi.md#resources_folder_by_id_translations) | **GET** /{instance}/resources/folder/{id}/translations | Folder Translations
*ResourcesApi* | [**resources_folder_root**](docs/ResourcesApi.md#resources_folder_root) | **GET** /{instance}/resources/folder/root | Folder Root
*ResourcesApi* | [**resources_image_by_id**](docs/ResourcesApi.md#resources_image_by_id) | **GET** /{instance}/resources/image/{id} | Image


## Documentation For Models

 - [ArtefactCategory](docs/ArtefactCategory.md)
 - [Category](docs/Category.md)
 - [Channel](docs/Channel.md)
 - [Container](docs/Container.md)
 - [ContainerRelationship](docs/ContainerRelationship.md)
 - [Document](docs/Document.md)
 - [Facet](docs/Facet.md)
 - [Folder](docs/Folder.md)
 - [GetArtefactCategoriesResponse](docs/GetArtefactCategoriesResponse.md)
 - [GetContainerResponse](docs/GetContainerResponse.md)
 - [GetDocumentContainerRelationshipsResponse](docs/GetDocumentContainerRelationshipsResponse.md)
 - [GetDocumentContainersResponse](docs/GetDocumentContainersResponse.md)
 - [GetDocumentResponse](docs/GetDocumentResponse.md)
 - [GetDocumentTranslationsResponse](docs/GetDocumentTranslationsResponse.md)
 - [GetFileResponse](docs/GetFileResponse.md)
 - [GetFolderChildrenResponse](docs/GetFolderChildrenResponse.md)
 - [GetFolderResponse](docs/GetFolderResponse.md)
 - [GetFolderRootResponse](docs/GetFolderRootResponse.md)
 - [GetFolderTranslationsResponse](docs/GetFolderTranslationsResponse.md)
 - [GetImageResponse](docs/GetImageResponse.md)
 - [GetResponseResponse](docs/GetResponseResponse.md)
 - [GetSearchArtefactResponse](docs/GetSearchArtefactResponse.md)
 - [GetSearchResponse](docs/GetSearchResponse.md)
 - [Link](docs/Link.md)
 - [MetaDataValueDetails](docs/MetaDataValueDetails.md)
 - [PostArtefactCategoryRequest](docs/PostArtefactCategoryRequest.md)
 - [PostArtefactCategoryResponse](docs/PostArtefactCategoryResponse.md)
 - [PostLiveCshRequest](docs/PostLiveCshRequest.md)
 - [PostLiveCshResponse](docs/PostLiveCshResponse.md)
 - [PostLiveDocumentRequest](docs/PostLiveDocumentRequest.md)
 - [PostLiveDocumentResponse](docs/PostLiveDocumentResponse.md)
 - [PostLiveSearchRequest](docs/PostLiveSearchRequest.md)
 - [PostLiveSearchResponse](docs/PostLiveSearchResponse.md)
 - [QueryVariation](docs/QueryVariation.md)
 - [Resource](docs/Resource.md)
 - [ResourceSearchResult](docs/ResourceSearchResult.md)
 - [ResponseSection](docs/ResponseSection.md)
 - [ResponseVariation](docs/ResponseVariation.md)
 - [SearchResult](docs/SearchResult.md)
 - [StringInt64NullableKeyValuePair](docs/StringInt64NullableKeyValuePair.md)
 - [Tag](docs/Tag.md)
 - [Training](docs/Training.md)


## Documentation For Authorization


## apiKeyHeader

- **Type**: API key
- **API key parameter name**: Ocp-Apim-Subscription-Key
- **Location**: HTTP header


## Author

support@panviva.com

