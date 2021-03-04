# qc_qubosolv_api.ProblemApi

All URIs are relative to *https://annealer.quantum-circle.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**task_post**](ProblemApi.md#task_post) | **POST** /task | Submit a Problem


# **task_post**
> object task_post(body)

Submit a Problem

Submit a Problem to the Solver.

### Example
```python
from __future__ import print_function
import time
import qc_qubosolv_api
from qc_qubosolv_api.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: oauth2
configuration = qc_qubosolv_api.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = qc_qubosolv_api.ProblemApi(qc_qubosolv_api.ApiClient(configuration))
body = qc_qubosolv_api.Task() # Task | Submit a Problem.

try:
    # Submit a Problem
    api_response = api_instance.task_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProblemApi->task_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Task**](Task.md)| Submit a Problem. | 

### Return type

**object**

### Authorization

[oauth2](../README.md#oauth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

